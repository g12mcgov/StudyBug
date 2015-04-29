#!/usr/bin/python
# -*- coding: utf-8 -*-

# Name: StudyBug 
# File: /StudyBug/emailsend.py
#
# Author(s): Grant McGovern
# Date: Tue 6 Jan 2015 
#
# URL: www.github.com/g12mcgov/studybug
#
# ~ Setups the email template and functionality ~
#
#

import sys
import smtplib
import time
import logging
import datetime
from smtplib import SMTPException

sys.path.append('loggings')

## Local Includes ## 
from db import MongoDriver
from loggings.loger import configLogger

logger = logging.getLogger('root')

# TODO: Change to a dict of args 
# I hate passing this many arguments 
def sendEmail(confirmationList, room, email, password, startTime, endTime, expectedTime, MONGO_HOST, MONGO_PORT):
	logger.info(" sending email...")
	now = datetime.datetime.now()
	
	startdate = now.strftime("%m/%d/%Y")
	date = datetime.datetime.strptime(startdate, "%m/%d/%Y")
	
	endate = date + datetime.timedelta(days=4)
	newdate = endate.strftime("%m/%d/%Y")

	day_name = endate.strftime("%A")

	length = len(confirmationList)

	gmail_user = email
	gmail_password = password

	if confirmationList:
		confirmed_rooms = confirmationList
	else:
		confirmed_rooms = ""

	# Consruct a formatted list to insert into Mongo as such:
	#
	# Room 203A 10:00 AM  
	# Room 203A 10:30 AM  
	# Room 203A 11:00 AM  
	# Room 203A 11:30 AM  
	# Room 203A 12:00 PM  
	# Room 203A 12:30 PM  
	# Room 203A 1:00 PM  
	# Room 203A 1:30 PM  
	# Room 203A 2:00 PM  
	# Room 203A 2:30 PM  
	# Room 203A 3:00 PM  
	# Room 203A 3:30 PM  
	# Room 203A 4:00 PM  
	# ...
	# ...
	# ...
	#

	original_rooms = [item.replace('Reserved: ', '').encode('utf-8') for item in confirmationList]

	mongo = MongoDriver(MONGO_HOST)

	todayDate = now.strftime("%m/%d/%Y")

	# If the length of our booked room list is equal to that of what we expected
	# then we can simply form a range such as '10:00 AM - 11:00 PM'
	if len(original_rooms)-1 == expectedTime:
		formatted_rooms = original_rooms[0] + 'to ' + original_rooms[-1]
		# Now add our rooms
		#
		# When we insert into Mongo, we want to store the following (example) BSON entry:
		# 
		# {
		# 	"_id" : ObjectId("54d42be2414771257e62a3b8"),
		# 	"bookings" : [
		# 		"Room 203A 10:00 AM  ",
		# 		"Room 203A 10:30 AM  ",
		# 		"Room 203A 11:00 AM  ",
		# 		"Room 203A 11:30 AM  ",
		#		...
		# 	],
		# 	"expected" : 27,
		# 	"timeRange" : [
		# 		"Room 203A 10:00 AM  ",
		# 		"Room 203A 10:30 AM  ",
		# 		"Room 203A 11:00 AM  ",
		# 		"Room 203A 11:30 AM  ",
		# 		 ...
		# 	],
		# 	"room" : "room-203a", 
		# 	"todays_date": "02/06/2015",
		# 	"fivedays_ahead": "02/11/2015"
		# }
		# 
		#
		mongo.addEntry(original_rooms, expectedTime, formatted_rooms, room, todayDate, newdate)
	else:
		mongo.addEntry(original_rooms, expectedTime, original_rooms, room, todayDate, newdate)

	#print list('\n'.join(confirmed_rooms).replace('Reserved: ', '').encode('utf-8'))
	email = constructEmailBody(gmail_user, day_name, newdate, length, original_rooms)

	message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
	""" % (email[0], ",".join(email[1]), email[2], email[3])

	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_password)
		server.sendmail(email[0], email[1], message)
		server.close()

		logger.info(" successfully sent mail")
	except SMTPException as err:
		logger.error("ERR: could not send mail")
		logger.error(err)

def constructEmailBody(gmail_user, day_name, newdate, length, rooms):
	if "to" in rooms:
		body = rooms
	else:
		body = '\n'.join(rooms)

	FROM = gmail_user
	TO = ['mcgoga12@wfu.edu']
	SUBJECT = "PIKE Study Rooms for %s, %s" % (day_name, newdate)
	TEXT = """
This is an automated email from StudyBug.

The following studyroom times were booked for %s:

(%s time slots total)

%s

Thanks, 

StudyBug 

-----------------------------------------------------------------------------------------------
~ a grantmcgovern build ~	
-----------------------------------------------------------------------------------------------

Check out the project page at: https://github.com/g12mcgov/StudyBug


""" % (newdate, length, body)
	
	return (FROM, TO, SUBJECT, TEXT)

