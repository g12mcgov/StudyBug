#!/usr/bin/python

# Name: StudyBug 
# Author(s): Grant McGovern, Gaurav Sheni, Nate Dehorn 
# Date: 16 March 2013
#
# URL: www.github.com/g12mcgov/studybug
#
#

import datetime 
import sys 
import urllib2 # library to work with URLs (helps go out to make the URL hit)
import socket # used to get IP address
import operator
from emailsend import *
from credentials import * #stores information regarding usernames and passwords 
from splinter import Browser
from bs4 import BeautifulSoup 
from collections import OrderedDict
from pyvirtualdisplay import Display

## Changed to CSV instead of TXT 
import csv

def main():
	date = getDate() # must make a call to get date and pass into URL to update with day 
	### DO NOT CHANGE ### CONSTANTS ###:
	url = "http://zsr.wfu.edu/studyrooms/%s" % date # passes in the date string to append to URL 
	room = "room-" + "225" 
	availabilitylist = [] * 48
	temp = []
	
	############################################
	IPfetch() # function to return IP address
	############################################
	
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
			studyBug(url ,updatedavailabilitylist, user) # function that kicks off the Web-Interactivity 
	
	
	timelist = []
	for user in userList: # loop restricted by # of users
		timelist.extend(getconfirm(url, timelist, user, room))
	print timelist
	sortedlist = sorttimes(timelist)
	print sortedlist
	sendEmail("\n".join(sortedlist))
	print "Task Successful."

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
	driver = Browser('phantomjs')
	driver.visit(url)
	# this opens up Chrome
	print "\n".join(tosend) #formatted to look nice
	if len(tosend)<1:
		pass
	else:
		xpath1 = "//label[contains(text(),'%s')]/.." % tosend[0]
		driver.find_by_xpath(xpath1).click()
	if len(tosend)<2:
		pass
	else:
		xpath2 = "//label[contains(text(),'%s')]/.." % tosend[1]
		driver.find_by_xpath(xpath2).click()
	if len(tosend)<3:
		pass
	else:
		xpath3 = "//label[contains(text(),'%s')]/.." % tosend[2]
		driver.find_by_xpath(xpath3).click()
	if len(tosend)<4:
		pass
	else:
		xpath4 = "//label[contains(text(),'%s')]/.." % tosend[3]
		driver.find_by_xpath(xpath4).click()
	
	submit = driver.find_by_id("reserve").click()
	
	driver.find_by_name("username").fill(user_info.getusername())
	print "User: %s" % user_info.getusername()
	driver.find_by_name("password").fill(user_info.getkey())
	#print user_info.getkey()

	driver.find_by_name("submit").click()

	driver.quit() # this closes the browser

def writeOut(availability, PATH): # function used to write out to text file 
	time = availability
	with open(PATH, "wb") as f:
		#print availability
		string = str(availability)
		f.write(string)

def readIn():
	## Contains generated user objects
	userlist = []

	with open("credentials.csv") as csvfile:
		credentials_reader = csv.reader(csvfile, delimiter=',')
		for row in credentials_reader:
			## Check for white space in csv file
			if row:
				userlist.append(User(row[0], row[1]))
			else:
				pass

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
	driver = Browser('phantomjs')
	driver.visit(logurl)

	driver.find_by_name("username").fill(user_info.getusername())
	print "Checking... %s" % user_info.getusername()
	driver.find_by_name("password").fill(user_info.getkey())
	print "Checking... %s" % abs(hash(user_info.getkey())) # uses a cheap hash to mask user password 

	driver.find_by_name("submit").click()
	date = getDate()
	daytclick = driver.visit(url)
	source = driver.html
	soup = BeautifulSoup(source) # reads in the HTML data from the page 
	
	confirmationlist = []
	
	for label in soup.find(id=studyroom).select('li.zone label'):
		temp = label.get_text()
		temp = temp.encode('ascii','ignore')
		confirmationlist.append(temp)
	driver.quit() # this closes the browser
	print confirmationlist
	return confirmationlist

def sorttimes(timelist):
	newdict=dict()
	toreturn = list()
	if not timelist:
		print "Error, nothing to confirm"
		sys.exit()
	else:
		for index in range(len(timelist)):
				spot1 = timelist[index].find("Room")
				temp = str(timelist[index][spot1 + 9 : spot1 + 19].translate(None, ' Reserved'))
				checkab = len(temp) - len(temp.lstrip())
				temp = temp[checkab:]
				print temp
				td1 = datetime.datetime.strptime(temp, '%I:%M%p') 
				newdict[td1] = timelist[index]
	for key in sorted(newdict):
		toreturn.append(newdict[key])
    	return toreturn

if __name__ == "__main__":
	main()

 
