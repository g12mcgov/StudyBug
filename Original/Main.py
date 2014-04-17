# StudyBug 
# Written and Bred by Grant McGovern, Gaurav Sheni, Nate DeHorn <-- Written in the Python Language -->
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
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from collections import OrderedDict

def main():
	try:
		IPfetch() # function to return IP address
		date = getDate() # must make a call to get date and pass into URL to update with day 
		print date

		############################################
		### DO NOT CHANGE ### CONSTANTS ###:
		url = "http://zsr.wfu.edu/studyrooms/%s"  % date # passes in the date string to append to URL 
		studyrooms = ['203a','203b','225','226','227','228','232','675','676','677'] # list of available study rooms in ZSR
		print studyrooms
		############################################
		readIn() # function that reads in data from text file, current a dummy function as users as hard-coded below:

		print "Total User Count: %d \n" % User.global_count # displays the amount of current users 

		############################################
		availabilitylist = [] * 48
		HTML = htmlFetch(url) # grabs the HTML to see if rooms are available using BeautifulSoup
		
		availabilitylist = availability(HTML)
		
		availabilitylist = analyzeList(availabilitylist)
		
		times = availabilitylist.keys()
		for time in times:
			formatted_times = [time.strftime("%I:%M %p")]

		updatedavailabilitylist = formatAvailabilityList(availabilitylist)
		
		studyBug(url ,updatedavailabilitylist) # function that kicks off the Web-Interactivity using Selenium 
		sendEmail(formatted_times)

		print "Crawl Successful."
	except: 
		print "StudyBug Failed."

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

def availability(soup):
	print "What study room would you like to book? "
	studyroom = "room-" + raw_input('> ') # will be taken out, left in right now to work with specific study rooms 

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
		print 'Error, no times available or nothing in availabilitylist'
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
		temp = str(sortedtimes[index][spot: spot + 17].translate(None, ''))
		tosend.insert(index,temp)
	return tosend

def studyBug(url, tosend):
	
	#print xpath1
	if len(tosend)<1:
		"No Times Available"
		return
	print "Crawling Site..."
	driver = webdriver.Chrome(executable_path= '/Users/grantmcgovern/Desktop/chromedriver')
	driver.get(url)
	# this opens up Chrome
	assert "ZSR" in driver.title # this assures that the word ZSR is in the webpage title 
	print tosend
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
	username.send_keys("######") # USERNAME
	password = driver.find_element_by_name("password")
	password.send_keys("######") # PASSWORD
	
	driver.find_element_by_name("submit").click()

	#driver.close()

def writeOut(availability, PATH): # function used to write out to text file 
	time = availability
	with open(PATH, "wb") as f:
		#print availability
		string = str(availability)
		f.write(string)

def readIn():
	with open("credentials.txt", "r") as infile:
    		content = [line.rstrip().split(",") for line in infile]
    		#usernames, passwords = zip(*content) # nifty zip function used to split usernames and passwors into two seperate lists 
    		#print usernames, passwords
			#for username in usernames:
			#print "username: %s" % username
def getDate():
	now = datetime.datetime.now()
	startdate=now.strftime("%Y/%m/%d")
	date = datetime.datetime.strptime(startdate, "%Y/%m/%d")
	endate = date + datetime.timedelta(days=3)
	toreturn = endate.strftime("%Y/%m/%d")
	# Example format = 2014/04/17
	return toreturn

if __name__ == "__main__":
	main()

 