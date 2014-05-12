#!/usr/bin/python

# StudyBug 
# Written and Bred by Grant McGovern, Gaurav Sheni, Nate DeHorn 
# <-- Written in the Python Language --> #
import datetime 
import sys 
import urllib2 # library to work with URLs (helps go out to make the URL hit)
import socket # used to get IP address
import selenium
import operator
import os
from Credentials import * #stores information regarding usernames and passwords 
from Email import *
from bs4 import BeautifulSoup #imports HTML BeautifulSoup only instead of XML
from selenium import webdriver 
from collections import OrderedDict
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

def main():

	for i in range(10):
		try:
			display = Display(visible = 0, size = (800,600))
			display.start()
			date = getDate() # must make a call to get date and pass into URL to update with day 
			### DO NOT CHANGE ### CONSTANTS ###:
			url = "http://zsr.wfu.edu/studyrooms/%s" % date # passes in the date string to append to URL 
			exact_room = raw_input("Please enter the room you would like to book: ")
			room = "room-" + "%s" % exact_room
			availabilitylist = [] * 48
			temp = []
			############################################
			IPfetch() # function to return IP address
			############################################
			HTML_first = htmlFetch(url) # grabs the HTML to see if rooms are available using BeautifulSoup
			availabilitylist_first = availability(room, HTML_first)
			
			userList = readIn() # function that reads in data from text file, current a dummy function as users as hard-coded below:
			
			for user in userList: # loop restricted by # of users
				HTML = htmlFetch(url) # grabs the HTML to see if rooms are available using BeautifulSoup
				availabilitylist = availability(room, HTML)
				if not availabilitylist:
					print "Nothing in the availabilitylist."
					break
				else:
					availabilitylist = analyzeList(availabilitylist)		
					times = availabilitylist.keys()
					updatedavailabilitylist = formatAvailabilityList(availabilitylist)
					studyBug(url ,updatedavailabilitylist, user) # function that kicks off the Web-Interactivity using Selenium 
			
			display.stop()
			
			timelist = []
			for user in userList: # loop restricted by # of users
				timelist.extend(getconfirm(url, timelist, user, room))
			print timelist
			sendEmail("\n".join(timelist))
			print "Task Successful."
			
			break	
			
		except:
			print "Task Failed.", sys.exc_info()[0]

def IPfetch():
	print "Hostname is: " + socket.gethostname() # returns the hostname 
	print "IP Address is: " + socket.gethostbyname(socket.gethostname()) # returns your current IP address
	print '\n'

	### This function will eventually be used to change the IP address every time it's run

def htmlFetch(url): #must also pass in the path to the writeOut() call
	print "Beginning a URL hit..."
	print "URL: " + url + '\n'
	page = urllib2.urlopen(url) # makes the URL hit
	soup = BeautifulSoup(page.read()) # reads in the HTML data from the page 
	return soup

def availability(room, soup):
	studyroom = room
	# each of these options stores the potential for being open or not
	a = []
	for label in soup.find(id=studyroom).select('li.zone label'):
		temp = label.get_text()
		temp = temp.encode('ascii','ignore')
		a.append(temp)
	return a

# Written by Gaurav:
def analyzeList(availabilitylist): #reads in the list of available times (HTML string) to be sorted 
	newdict=dict()
	if not availabilitylist:
		print "Error, no times available or nothing in availabilitylist."
		sys.exit()
	else:
		for index in range(len(availabilitylist)):
			spot1 = availabilitylist[index].find("Room")
			temp = str(availabilitylist[index][spot1 + 9 : spot1 + 19].translate(None, ''))
			checkab = len(temp) - len(temp.lstrip())
			temp = temp[checkab:]
			td1 = datetime.datetime.strptime(temp, '%I:%M %p') 
			newdict[td1] = availabilitylist[index]
	times =  newdict.keys()
	times.sort()
	toreturn = dict((k, v) for k, v in newdict.iteritems() if k in times) # [0:4]
	return toreturn

def formatAvailabilityList(updatedavailabilitylist):
	newlist = OrderedDict(sorted(updatedavailabilitylist.items(), key=operator.itemgetter(0)))
	sortedtimes = newlist.values()
	tosend = [] * 4
	for index in range(len(newlist)):
		spot = sortedtimes[index].find("Room")
		temp = str(sortedtimes[index][spot: spot + 19].translate(None, ''))
		tosend.insert(index,temp)
	tosend.reverse()
	return tosend

def studyBug(url, tosend, user_info):
	if len(tosend)<1:
		"No Times Available"
		return
	print "Crawling Site..."
	driver = webdriver.Chrome(executable_path= '/Users/grantmcgovern/Dropbox/Developer/Projects/StudyBug/StudyBug.Sheni/chromedriver')
	driver.get(url)
	# this opens up Chrome
	assert "ZSR" in driver.title # this assures that the word ZSR is in the webpage title 
	print "\n".join(tosend) #formatted to look nice
	if len(tosend)<1:
		pass
	else:
		mouse = webdriver.ActionChains(driver)
		xpath1 = "//label[contains(text(),'%s')]/.." % tosend[0]
		checkbox1 = driver.find_element_by_xpath(xpath1)
		mouse.move_to_element(checkbox1).click().perform()
	if len(tosend)<2:
		pass
	else:
		xpath2 = "//label[contains(text(),'%s')]/.." % tosend[1]
		mouse = webdriver.ActionChains(driver)
		checkbox2 = driver.find_element_by_xpath(xpath2)
		mouse.move_to_element(checkbox2).click().perform()
	if len(tosend)<3:
		pass
	else:
		xpath3 = "//label[contains(text(),'%s')]/.." % tosend[2]
		mouse = webdriver.ActionChains(driver)
		checkbox3 = driver.find_element_by_xpath(xpath3)
		mouse.move_to_element(checkbox3).click().perform()
	if len(tosend)<4:
		pass
	else:
		xpath4 = "//label[contains(text(),'%s')]/.." % tosend[3]
		mouse = webdriver.ActionChains(driver)
		checkbox4 = driver.find_element_by_xpath(xpath4)
		mouse.move_to_element(checkbox4).click().perform()
	
	submit = driver.find_element_by_id("reserve").click()
	
	username = driver.find_element_by_name("username")
	username.send_keys(user_info.getusername())
	print "User: %s" % user_info.getusername()
	password = driver.find_element_by_name("password")
	password.send_keys(user_info.getkey())
	#print user_info.getkey()

	driver.find_element_by_name("submit").click()

	driver.close() # this closes the browser

def writeOut(availability, PATH): # function used to write out to text file 
	time = availability
	with open(PATH, "wb") as f:
		#print availability
		string = str(availability)
		f.write(string)

def readIn():
	userinfo = []
	with open("credentials.txt") as fp:
		for line in fp:
			userinfo.append(line.rstrip())
	userlist = []
	it = iter(userinfo)
	for x in it:
		temp = User(x, next(it))
		userlist.append(temp)
	#print "Total User Count: %d \n" % User.global_count # displays the amount of current users 
	return userlist

def getDate():
	now = datetime.datetime.now()
	startdate=now.strftime("%Y/%m/%d")
	date = datetime.datetime.strptime(startdate, "%Y/%m/%d")
	endate = date + datetime.timedelta(days=4)
	toreturn = endate.strftime("%Y/%m/%d")
	# Example format = 2014/04/17
	return toreturn

def getconfirm(url, timelist, user_info, studyroom):
	logurl = "https://zsr.wfu.edu/studyrooms/login"
	print "\n"
	print "Confirming..."
	driver = webdriver.Chrome(executable_path= '/Users/grantmcgovern/Dropbox/Developer/Projects/StudyBug/StudyBug.Sheni/chromedriver')
	driver.get(logurl)
	# this opens up Chrome
	assert "ZSR" in driver.title # this assures that the word ZSR is in the webpage title 

	username = driver.find_element_by_name("username")
	username.send_keys(user_info.getusername())
	print "Checking... %s" % user_info.getusername()

	password = driver.find_element_by_name("password")
	password.send_keys(user_info.getkey())
	print "Checking... %s" % abs(hash(user_info.getkey())) # uses a cheap hash to mask user password 

	driver.find_element_by_name("submit").click()
	date = getDate()
	daytclick = driver.get(url)
	source = driver.page_source
	soup = BeautifulSoup(source) # reads in the HTML data from the page 
	
	confirmationlist = []
	
	for label in soup.find(id=studyroom).select('li.zone label'):
		temp = label.get_text()
		temp = temp.encode('ascii','ignore')
		confirmationlist.append(temp)
	driver.close() # this closes the browser
	print confirmationlist
	return confirmationlist

if __name__ == "__main__":
	main()

 
