# StudyBug 
# Written and Bred by Grant McGovern <-- Written in the Python Language -->

import re 
import datetime 
import sys 
import urllib
import urllib2
import socket
import struct 
import fcntl 
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 


def main():

	############################################

	url = "http://zsr.wfu.edu/studyrooms/2014/04/07"
	IPfetch()
	studyBug(url)
	htmlFetch(url)
	setIPAddr('em1', '192.168.0.1')


def htmlFetch(url):
	link = url;
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	availability = soup.fieldset.find(id="room-203a").get_text()
	print availability

def IPfetch():
	print "Hostname is: " + socket.gethostname()
	print "IP Address is: " + socket.gethostbyname(socket.gethostname())
	print '\n'

def studyBug(url):
	print "Beginning a URL hit..."
	driver = webdriver.Firefox()
	driver.get(url)
	assert "ZSR" in driver.title
	elem = driver.find_element_by_id("room-203a")



if __name__ == "__main__":
	main()

