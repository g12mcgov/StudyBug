# StudyBug 
# Written and Bred by Grant McGovern <-- Written in the Python Language -->

import re # library that allows us to work wit Regular Expressions (Regex) --> will be used later to parse 
import datetime 
import sys 
import os # allows us to interact with paths and open the file in a relative location 
import urllib2 # library to work with URLs (helps go out to make the URL hit)
import socket # used to get IP address
import struct 
import fcntl 
import time
from selenium.webdriver.support import expected_conditions as EC
from Queue import Queue
from Credentials import * #stores information regarding usernames and passwords 
from bs4 import BeautifulSoup #imports HTML BeautifulSoup only instead of XML
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 


def main():

	IPfetch() # function to return IP address
	date = getDate() # must make a call to get date and pass into URL to update with day 
	############################################
	### DO NOT CHANGE ### CONSTANTS ###:
	url = "http://zsr.wfu.edu/studyrooms/2014/04/10" #% date # passes in the date string to append to URL 
	PATH = "/Users/grantmcgovern/Desktop/HTMLwrite.txt"
	studyrooms = ['203a','203b','225','226','227','228','232','675','676','677'] # list of available study rooms in ZSR
	############################################
	priority_queue = Queue(len(studyrooms)) #creates a Queue of Study rooms, the length of available study rooms
	############################################

	for room in studyrooms:
		priority_queue.put(room)

	while not priority_queue.empty():
		print priority_queue.get()


	### Defines a Test User : Contains username/password
	
	readIn() # function that reads in data from text file, current a dummy function as users as hard-coded below:

	user1 = User("mcgoga12", "password")
	user2 = User("shellb12", "password1")
	# user1.showKeys() # shows the username and password for user1
	# user2.showKeys() # shows the username and password for user2

	print "Total User Count: %d \n" % User.global_count # displays the amount of current users 

	############################################
	availabilitylist = [] * 48

	HTML = htmlFetch(url, PATH) # grabs the HTML to see if rooms are available using BeautifulSoup
	analyzeList(availabilitylist)
	studyroom = getStudyRoom()
	print studyroom
	availabilitylist = availability(HTML, studyroom)
	reserve(url, studyroom) # function that kicks off the Web-Interactivity using Selenium 

def analyzeList(availabilitylist):
	if availabilitylist: # check to see if the list is even populated 
		for shit in availabilitylist:
			print shit
	

def htmlFetch(url, PATH): #must also pass in the path to the writeOut() call
	print "Beginning a URL hit..."
	print "URL: " + url + '\n'
	# time.sleep(1) # will take out when done... just simulating a hit right now
	link = url;
	page = urllib2.urlopen(url) # makes the URL hit
	soup = BeautifulSoup(page.read()) # reads in the HTML data from the page 
	return soup

def availability(soup, studyroom):

	availabilityList = [] * 48 # number of half-hours in a day 

	 # will be taken out, left in right now to work with specific study rooms 

### zsr.wfu.edu/studyrooms is staggered in the following way:
	# availability is marked by the 4 following options.
	# each of these options stores the potential for being open or not

	availability_even_day = soup.find(id=studyroom).findAll("li", {"class" : "zone even open day"}) 
	availability_even_night = soup.find(id=studyroom).findAll("li", {"class" : "zone even open night"})
	availability_odd_day = soup.find(id=studyroom).findAll("li", {"class" : "zone odd open day"})
	availability_odd_night = soup.find(id=studyroom).findAll("li", {"class" : "zone odd open night"})
	
	# not necessary:
	for label in soup.find(id=studyroom).select('li.zone label'):
		print label.get_text()

### Simply to test if availabilities are populating correctly --> If coming back as empties, study rooms are completely booked 
	'''
	print availability_even_day
	print availability_even_night
	print availability_odd_day
	print availability_odd_night
	'''
#########################################################

	# if there exists ANY study room that is open, proceed to check individually 
	if availability_even_day or availability_odd_day or availability_even_night or availability_odd_night:
		if availability_odd_day: # if availability_even_day is the room open, then say so using writeOut()
			availabilityList.insert(0, availability_odd_day)
		
		if availability_even_day: # if availability_odd_day is the room open, then say so using writeOut()
			availabilityList.insert(1, availability_even_day)
		
		if availability_odd_night: # if availability_even_night is the room open, then say so using writeOut()
			availabilityList.insert(2, availability_odd_night)
		
		if availability_even_night:
			availabilityList.insert(3, availability_even_night) # if availability_odd_night is the room open, then say so using writeOut()
		
		print "Study Room %s Available" % studyroom
	
		return availabilityList

	else: # otherwise if no Study Room is available, then print out that the specific study room is completely booked 
		print "Study Room %s Completely Booked" % studyroom

def IPfetch():
	print "Hostname is: " + socket.gethostname() # returns the hostname 
	print "IP Address is: " + socket.gethostbyname(socket.gethostname()) # returns your current IP address
	print '\n'

	### This function will eventually be used to change the IP address every time it's run

def reserve(url, studyroom):
	print "Crawling Site..."
	driver = webdriver.Chrome(executable_path="/Users/grantmcgovern/Dropbox/Developer/Projects/StudyBug/chromedriver")
	driver.get(url)
	assert "ZSR" in driver.title # this assures that the word ZSR is in the webpage title (simply checks to make sure we'lre in the right spot)
	#studyroom.replace("room-","",1)
	studyroom_copy = studyroom
	elem = driver.find_element_by_id(studyroom_copy)# % studyroom #looks for the HTML element for the specific study room

def writeOut(availability, PATH): # function used to write out to text file 
	time = availability
	with open(PATH, "wb") as f:
		string = str(availability)
		f.write(string)

def readIn():
	with open("credentials.txt", "r") as infile:
    		content = [line.rstrip().split(",") for line in infile]
    		usernames, passwords = zip(*content) # nifty zip function used to split usernames and passwors into two seperate lists 
    		#print usernames, passwords
			#for username in usernames:
			#print "username: %s" % username

def getDate():
	date = time.strftime("%Y/%m/%d")
	return date

def getStudyRoom():
	print "What study room would you like to book? "
	studyroom = "room-" + raw_input('> ')
	return studyroom


if __name__ == "__main__":
	main()

