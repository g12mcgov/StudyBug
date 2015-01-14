#!/usr/bin/python

# Name: StudyBug 
# Author(s): Grant McGovern & Gaurav Sheni
# Date: 16 March 2013
#
# URL: www.github.com/g12mcgov/studybug
#
#

import os
import csv
import sys
import time
import socket
import urllib2
import logging
import operator
import datetime
import ConfigParser
from timeit import Timer 
from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing import Pool 
from collections import OrderedDict
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

sys.path.append('helpers')
sys.path.append('loggings')

## Local Includes ##
from user import User
from schema import XPathSchema
from emailsend import sendEmail
from loggings.loger import configLogger
from helpers.helper import chunk, parseTime

def main():
	# To indicate a new log-block
	logger.info("-------- NEW LOG BLOCK ---------------")
	
	log_start = datetime.datetime.now()
	logger.info(" beginning StudyBug at " + str(log_start))

	global url
	global selenium_timeout

	# Get date 5 days ahead
	date = getDate()

	# Setup our configuration parameters 
	configs = getConfig()
	url = str(configs[0] + date)
	room = "room-" + str(configs[1])
	startTime = str(configs[2])
	endTime = str(configs[3])
	selenium_timeout = int(configs[4])
	email = str(configs[5])
	password = str(configs[6])
	
	# Reads in user info
	rows = readIn()

	# Pulls down HTML
	HTML = htmlFetch(url)
	
	# Discovers available rooms
	rooms = availability(room, HTML, startTime, endTime)

	# Create a threading pool
	if not rooms:
		logger.warning(" no available rooms at all")
		return

	users = matchUsers(rows, rooms)

	for user in users:
		logger.info(" user: " + user.username + " xpaths: " + str(user.xpath))
	
	if not users:
	 	logger.warning(" no rooms for time constraint")
	 	return
	 	
	else:
		logger.info(" total users: " + str(len(users)))
		logger.info(" creating thread pool... ")	
	 	pool = Pool(processes=4)
	 	pool.map(bookRooms, users)

	 	logger.info(" Executed in " + str(datetime.datetime.now() - log_start) + " seconds")

	# Lastly, confirm our reservations
	confirmed_times = confirm(url, room, rows)
	# Send email with our reserved rooms
	sendEmail(confirmed_times, room, email, password, startTime, endTime)

	logger.info("--------------------")

def bookRooms(user):
	logger.info(" " + user.username + " - booking rooms")
	if not user:
		logger.error(" " + user.username + " - NO AVAILABLE TIMES")
	else:
		driver = webdriver.PhantomJS()
		driver.get(url)

		# This is a PhantomJS but remedied by the following method call... should 
		# look into a fix for this.
		driver.set_window_size(2000, 2000)

		wait = WebDriverWait(driver, selenium_timeout)

		if not user.xpath:
			pass
		else:
			success = False

			# Sometimes Selenium will load the page faster than the javascript
			# or sometimes the web page will timeout (most likely due to connection
			# issues). This way, we keep trying, but if we have success, we break out.
			for attempt in range(10):
				for item in user.xpath:
					try:
						logger.info(" " + user.username + " - clicking on individual rooms...")
						logger.info(" " + user.username + " - clicking on " + item['xpath'])
						
						# Xpath looks like this: //*[@id=room-225]/dd[5]
						element = wait.until(EC.presence_of_element_located((By.XPATH, item['xpath'])))
						#element = driver.find_element_by_xpath(str(item['xpath']))
						element.click()

						success = True
						logger.info(" " + user.username + " - successfully clicked on all rooms")		

					except NoSuchElementException:
						logger.error(" " + user.username + "- COULDN'T CLICK ON ELEMENT " + str(item['xpath']))
				try:
					logger.info(" " + user.username + " - clicking on save for user")

					save_box = wait.until(EC.presence_of_element_located((By.XPATH, "id('save')")))
					#driver.find_element_by_xpath("id('save')").click()
					save_box.click()

					logger.info(" " + user.username + " - filling in username ")
					user_name_box = wait.until(EC.presence_of_element_located((By.ID, "username")))
					#user_name_box = driver.find_element_by_id("username")
					user_name_box.send_keys(user.username)

					logger.info(" " + user.username + " - filling in password ")
					password_box = wait.until(EC.presence_of_element_located((By.ID, "password")))
					#password_box = driver.find_element_by_id("password")
					password_box.send_keys(user.key)

					logger.info(" " + user.username + " - clicking on submit ")
					reserve_button = wait.until(EC.presence_of_element_located((By.ID, "submit")))
					#reserve_button = driver.find_element_by_id("submit")
					reserve_button.click()

					if success == True: break

				except NoSuchElementException as err:
					logger.error(" " + user.username + "FAILED")
					logger.error(err)

				except TimeoutException as err:
					logger.error(" " + user.username + "FAILED")
					logger.error(err)

	# Close PhantomJS
	driver.quit()

# Will eventually be used to change the IP address every time it's run
def IPfetch():
	hostname = socket.gethostname()
	ip_address = socket.gethostbyname(socket.gethostname())
	
	logger.info(" hostname: " + hostname)  
	logger.info(" IP address: " + ip_address) 

	return (hostname, ip_address)

# Extracts HTML from ZSR Website 
def htmlFetch(url): 
	logger.info(" requesting " + url)
	page = urllib2.urlopen(url) 
	soup = BeautifulSoup(page.read())
	
	return soup

# Determines what rooms are available
def availability(room, soup, startTime, endTime):
	# schema = XPathSchema()
	rooms = []

	# Returns a HTML code block as such:

	# <dd class="cell even open">
 	#	<input id="srr-1-1420839000" name="srr-1-1420839000" type="checkbox" value="Y"/>
 	#	<label for="srr-1-1420839000">
  	#		<span class="room-name">
    #			Room 225
  	#		</span>
  	#		<span class="time-slot">
   	#			4:30 PM
  	#		</span>
 	#	</label>
 	#	<i class="drag-handle">
 	#	</i>
	# </dd>

	# Sometimes BeautifulSoup attempts to find the elements before the page 
	# has completely loaded. This is a hacky way of ensuring the page has been
	# loaded by recursively attempting to accessing content for 2 minutes before
	# timing out.
	for attempt in range(120):
		try:
			# Find all rooms on the grid which are open
			blocks = [block for block in soup.find(id=room).select('dd') if "unavailable" not in block.text]

			if blocks:
				break
			else:
				pass

		except AttributeError as err:
			logger.error("Could not click on element")
			logger.error(err)

		time.sleep(1)


	# Extract our times from the config file
	start = parseTime(startTime)
	end = parseTime(endTime)

	# Get the first element on the grid
	starting_time = parseTime(blocks[0].find('span', {'class': 'time-slot'}).get_text())
	ending_time = parseTime(blocks[-1].find('span', {'class': 'time-slot'}).get_text())

	# If we configured a time later than the last possible one, limit it
	if ending_time < end:
		end = ending_time
	
	# Calculate our starting time point by finding the distance between the two times.
	difference = start - starting_time

	# Breaks up the difference into half-hour blocks
	halfHours = (difference.seconds / 60 / 60)*2

	## Increment i (our XPath index until we hit the startime time)
	i = 1
	while (i != halfHours): i += 1 	
	
	for block in blocks:
		status = ' '.join(block.get('class'))
		time_ = block.find('span', {'class': 'time-slot'}).get_text()

		# Only assign rooms between the above hours
		if start <= parseTime(time_) <= end:
			# Pre-increment by 1, no idea why, but I should find out
			i += 1
			## Check to make sure room is open 
			if "open" in status:
				rooms.append({
					"room": room,
					"status": status,
					"time": time_,
					"xpath": "//*[@id='%s']/dd[%i]" % (room, i) # schema.getXpath(time)
					})
			else:
				pass

	# Just to see how many rooms were available
	if len(rooms) < 1:
		logger.warning(
			" no available time slots for room: " + room + " between " + startTime + " and " + endTime
			)
		logger.warning("Exiting...")
		return 
	else:
		logger.info(" total available time slots: " + str(len(rooms)))


	# Returns a list of dicts of rooms as such:
	# {'status': u'cell odd open', 'xpath': "id('room-203a')/x:dd[17]", 'room': 'room-225', 'time': u'4:00 PM'} 
	# {'status': u'cell even open', 'xpath': "id('room-203a')/x:dd[18]", 'room': 'room-225', 'time': u'4:30 PM'} 
	return rooms

## Assigns 4 timeslots to each user
def matchUsers(rows, rooms):
	## Check for white space in csv file
	rooms = chunk(rooms, 4)

	for room in rooms:
		logger.info('\n')
		logger.info(room)
	
	userdicts = []

	#for row, room in map(None, rows, rooms):
	for row, room in zip(rows, rooms):
		userdicts.append({
				"username": row[0], 
				"password": row[1], 
				"xpath": room
			})

	# Create a list of users, based on the above dict
	Users = [User(dictionary) for dictionary in userdicts]

	for user in Users:
		if user.xpath:
			logger.info(" assigned " + str(len(user.xpath)) + " chunks to " + user.username)
		else:
			logger.info(" did not assign any chunks to " + user.username)

	return Users

## Calculates next available date (5 days ahead) 
def getDate():
	now = datetime.datetime.now()
	startdate = now.strftime("%Y/%m/%d")
	
	date = datetime.datetime.strptime(startdate, "%Y/%m/%d")
	endate = date + datetime.timedelta(days=4)
	
	formattedTime = endate.strftime("%Y/%m/%d")
	
	# Example format = 2014/04/17
	return formattedTime

## Read in user credentials from config file and create user Objects
def readIn():

	with open("credentials/credentials.csv") as csvfile:
		credentials_reader = csv.reader(csvfile, delimiter=',')
		rows = [row for row in credentials_reader]
	
	# Returns the rows of the credentials csv file:
	# 
	# [
	#	mcgoga12, changeme
	#	guarav12, changeme1
	#	ben1234, changeme2
	# ]
	#		
	return rows

## Sets up config for program
def getConfig():
	config = ConfigParser.RawConfigParser()
	config.readfp(open('config/studybug.cfg'))

	url = config.get('studybug', 'URL')
	room = config.get('studybug', 'ROOM')
	startTime = config.get('studybug', 'START_TIME')
	endTime = config.get('studybug', 'END_TIME')
	selenium_timeout = config.get('studybug', 'SELENIUM_TIMEOUT')
	email = config.get('studybug', 'EMAIL')
	password = config.get('studybug', 'PASSWORD')

	return (url, room, startTime, endTime, selenium_timeout, email, password)

## Sends log data to Loggly via their API
def sendToLoggly():
	log_data = "PLAINTEXT=" + urllib2.quote(simplejson.dumps(
	{
	   'hoover':'beaver',
	   'ice':{
	        'ice':'baby'
	   }
	}))
	urllib2.urlopen("https://logs-01.loggly.com/inputs/65f419af-5bdb-489d-97b2-dd4883dad10a/tag/python/", log_data)

## Individually logs into each user account and confirms their reservation
def confirm(url, room, rows):
	logger.info(" confirming...")

	confirmationlist = []

	for row in rows:
		username = row[0]
		password = row[1]

		driver = webdriver.PhantomJS()

		# This is a PhantomJS but remedied by the following method call... should 
		# look into a fix for this.
		driver.set_window_size(2000, 2000)

		driver.get("https://zsr.wfu.edu/studyrooms/login")
		logger.info(" checking user " + username + "...")

		username_box = driver.find_element_by_name("username")
		username_box.send_keys(username)
		
		password_box = driver.find_element_by_name("password")
		password_box.send_keys(password)
		
		driver.find_element_by_name("submit").click()

		driver.get(url)

		html = driver.page_source
		soup = BeautifulSoup(html) 
	
		#confirmationlist = [reservation for reservation in soup.find(id=room).select('dd') if "current" in reservation.text]

		for reservation in soup.find(id=room).select('dd'):
			class_name = ' '.join(reservation.get('class'))
			# Checks to see if WE in fact reserved that room
			if "current_user_reservations" in class_name:
				confirmationlist.append(reservation.get_text())
				logger.info(" " + username + " booked " + reservation.get_text())

		# Nasty-ass xpath... no idea why the normal minified one won't work
		logout_button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/ul/li[3]/a")
		logout_button.click()
	
	
		driver.quit()
	
	return confirmationlist

if __name__ == "__main__":
	# Declare our root logger
	logger = configLogger("root")
	main()
