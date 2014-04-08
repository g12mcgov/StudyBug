# StudyBug 
# Written and Bred by Grant McGovern <-- Written in the Python Language -->

import re 
import datetime 
import sys 
import os # allows us to interact with paths and open the file in a relative location 
import urllib
import urllib2
import socket
import struct 
import fcntl 
import time
from Credentials import * #stores information regarding usernames and passwords 
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 


def main():

	date = getDate() # must make a call to get date and pass into URL to update with day 
	############################################
	### DO NOT CHANGE ###:
	url = "http://zsr.wfu.edu/studyrooms/%s" % date
	PATH = "/Users/grantmcgovern/Desktop/HTMLwrite.txt"
	############################################
	print "Beginning a URL hit..."
	print "URL: " + url + '\n'

	############################################
	### Defines a Test User : Contains username/password
	user1 = User("mcgoga12", "password")
	user2 = User("shellb12", "password1")
	user1.showKeys()
	user2.showKeys()

	print "Total User Count: %d \n" % User.global_count 

	############################################

	IPfetch()
	# studyBug(url)
	htmlFetch(url, PATH)


def htmlFetch(url, PATH): #must also pass in the path to the writeOut() call
	link = url;
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	print "What study room would you like to book? "
	studyroom = "room-" + raw_input('> ')

	availability_even_day = soup.find(id=studyroom).findAll("li", {"class" : "zone even open day"}) #finds if a study room is open or not 
	availability_even_night = soup.find(id=studyroom).findAll("li", {"class" : "zone even open night"})
	availability_odd_day = soup.find(id=studyroom).findAll("li", {"class" : "zone even odd day"})
	availability_odd_night = soup.find(id=studyroom).findAll("li", {"class" : "zone even odd night"})

### Simply to test if availabilities are populating correctly --> If coming back as empties, study rooms are completely booked 
	print availability_even_day
	print availability_even_night
	print availability_odd_day
	print availability_odd_night

	if availability_even_day or availability_odd_day or availability_even_night or availability_odd_night:
		if availability_even_day:
			writeOut(availability_even_day, PATH)
		elif availability_odd_day:
			writeOut(availability_odd_day)
		elif availability_even_night:
			writeOut(availability_even_night)
		elif availability_odd_night:
			writeOut(availability_odd_night)
		print "Study Room %s Available" % studyroom
	else:
		print "Study Room %s Completely Booked" % studyroom

def IPfetch():
	print "Hostname is: " + socket.gethostname()
	print "IP Address is: " + socket.gethostbyname(socket.gethostname())
	print '\n'

	### This function will eventually be used to change the IP address every time it's run

def studyBug(url):
	print "Crawling Site..."
	print "Beginning a URL hit..."
	driver = webdriver.Firefox()
	driver.get(url)
	assert "ZSR" in driver.title
	elem = driver.find_element_by_id("room-203a")

def writeOut(availability, PATH):
	with open(PATH, "wb") as f:
		print availability
		string = str(availability)
		f.write(string)


def getDate():
	date = time.strftime("%Y/%m/%d")
	return date

if __name__ == "__main__":
	main()

