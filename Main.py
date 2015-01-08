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
import simplejson
import ConfigParser
from timeit import Timer 
from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing import Pool 
from collections import OrderedDict
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

sys.path.append('helpers')

## Local Includes ##
from user import User
from schema import XPathSchema
from emailsend import sendEmail
from helpers.helper import chunk, parseTime

def main():
	# To indicate a new log-block
	logger.info("//NEW LOG BLOCK --------------------")
	
	log_start = datetime.datetime.now()
	logger.info(" Beginning StudyBug at " + str(log_start))

	global url
	global failed

	failed = []

	# Get date 5 days ahead
	date = getDate()
	date = "2015/01/08"

	# Setup our configuration parameters 
	configs = getConfig()
	url = str(configs[0] + date)
	room = "room-" + str(configs[1])
	startTime = str(configs[2])
	endTime = str(configs[3])
	
	# Reads in user info
	rows = readIn()

	# Pulls down HTML
	HTML = htmlFetch(url)
	
	# Discovers available rooms
	rooms = availability(room, HTML, startTime, endTime)

	# Create a threading pool
	if not rooms:
		logging.warning("No available rooms at all")
		return

	users = matchUsers(rows, rooms)
	
	if not users:
	 	logging.warning("No rooms for time constraint")
	 	return
	 	
	else:	
	 	pool = Pool(processes=7)
	 	pool.map(bookRooms, users)

	 	logger.info(" Executed in " + str(datetime.datetime.now() - log_start) + " seconds")

	# Lastly, confirm our reservations
	confirm(url, room, rows)

	logger.info("--------------------")

def bookRooms(user):
	logging.info("Booking rooms for user " + str(user.username))
	if not user:
		logging.error("No available for times for user: " + str(user.username))
	else:
		driver = webdriver.PhantomJS()
		driver.get(url)

		# This is a PhantomJS but remedied by the following method call... should 
		# look into a fix for this.
		driver.set_window_size(2000, 2000)

		if len(user.xpath) > 0:
			for item in user.xpath:
				try:
					# Xpath looks like this: //*[@id=room-225]/dd[5]
					element = driver.find_element_by_xpath(item['xpath'])
					element.click()
				except NoSuchElementException:
					logging.error("Couldn't click on element" + str(item['xpath']))
			try:
				driver.find_element_by_xpath("id('save')").click()

				user_name_box = driver.find_element_by_id("username")
				user_name_box.send_keys(user.username)

				password_box = driver.find_element_by_id("password")
				password_box.send_keys(user.key)

				reserve_button = driver.find_element_by_id("submit")
				reserve_button.click()

			except:
				logging.error("Failed at user " + str(user.username))
				#logging.error()
				#failed.append(item)

	# Close PhantomJS
	driver.quit()

# Will eventually be used to change the IP address every time it's run
def IPfetch():
	hostname = socket.gethostname()
	ip_address = socket.gethostbyname(socket.gethostname())
	
	logging.info("Hostname is: " + hostname)  
	logging.info("IP Address is: " + ip_address) 

	return (hostname, ip_address)

# Extracts HTML from ZSR Website 
def htmlFetch(url): 
	logging.info("Beginning a URL hit on " + url)
	page = urllib2.urlopen(url) 
	soup = BeautifulSoup(page.read())
	
	return soup

# Determines what rooms are available
def availability(room, soup, startTime, endTime):
	schema = XPathSchema()
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

	# Find all rooms on the grid which are open
	blocks = [block for block in soup.find(id=room).select('dd') if "unavailable" not in block.text]

	start = parseTime(startTime)
	end = parseTime(endTime)

	i = 1
	
	for block in blocks:
		status = ' '.join(block.get('class'))
		time = block.find('span', {'class': 'time-slot'}).get_text()

		## Check to make sure room is open 
		if "open" in status:
			## Only assign rooms between the above hours
			if end < parseTime(time) < start:
				pass
			else:
				rooms.append({
					"room": room,
					"status": status,
					"time": time,
					"xpath": "//*[@id='%s']/dd[%i]" % (room, schema.getXpath(time))
					})
		i += 1

	# Just to see how many rooms were available
	if len(rooms) < 1:
		logger.warning(
			"No available time slots for room: " + room + " between " + startTime + " and " + endTime
			)
		logging.warning("Exiting...")
		return 
	else:
		logger.info(" Total available time slots: " + str(len(rooms)))


	# Returns a list of dicts of rooms as such:
	# {'status': u'cell odd open', 'xpath': "id('room-203a')/x:dd[17]", 'room': 'room-225', 'time': u'4:00 PM'} 
	# {'status': u'cell even open', 'xpath': "id('room-203a')/x:dd[18]", 'room': 'room-225', 'time': u'4:30 PM'} 
	return rooms

## Assigns 6 timeslots to each user
def matchUsers(rows, rooms):
	## Check for white space in csv file
	rooms = chunk(rooms, 3)
	
	userdicts = []
	
	for row, room in zip(rows, rooms):
		userdicts.append({
				"username": row[0], 
				"password": row[1], 
				"xpath": room
			})

	# Create a list of users, based on the above dict
	Users = [User(dictionary) for dictionary in userdicts]

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

## Setsup a logger for the entire application to use
def configLogger():
	global logger
	## Make it so that all methods can reach it
	logger = logging.getLogger('studybug')
	handler = logging.FileHandler('log/logs/studybug.log')
	
	formatter = logging.Formatter(
		'%(asctime)s [ %(threadName)s ] [ %(levelname)s ] : %(message)s',
		'%Y-%m-%d %H:%M:%S'
		)
	
	handler.setFormatter(formatter)
	
	logger.addHandler(handler) 
	logger.setLevel(logging.DEBUG) 

	sendToLoggly()

## Sets up config for program
def getConfig():
	config = ConfigParser.RawConfigParser()
	config.readfp(open('config/studybug.cfg'))

	url = config.get('studybug', 'URL')
	room = config.get('studybug', 'ROOM')
	startTime = config.get('studybug', 'START_TIME')
	endTime = config.get('studybug', 'END_TIME')

	return (url, room, startTime, endTime)

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
	logger.info("Confirming...")

	confirmationlist = []

	for row in rows:
		username = row[0]
		password = row[1]

		driver = webdriver.PhantomJS()

		# This is a PhantomJS but remedied by the following method call... should 
		# look into a fix for this.
		driver.set_window_size(2000, 2000)

		driver.get("https://zsr.wfu.edu/studyrooms/login")
		logger.info("Checking user " + username)

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

		# Nasty-ass xpath... no idea why the normal minified one won't work
		logout_button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/ul/li[3]/a")
		logout_button.click()
	
	
		driver.quit()

	# Send email with our reserved rooms
	sendEmail(confirmationlist, room)
	
	return

if __name__ == "__main__":
	configLogger()
	main()
