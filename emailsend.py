#!/usr/bin/python

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
from loggings.loger import configLogger

logger = logging.getLogger('root')

def sendEmail(confirmationList, room, email, password, startTime, endTime):
	print startTime, endTime

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

	FROM = gmail_user
	TO = ['slagswfu@googlegroups.com', 'mcgoga12@wfu.edu']
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


""" % (newdate, length,'\n'.join(confirmed_rooms).replace('Reserved: ', '').encode('utf-8')) 

	message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
	""" %(FROM, ",".join(TO), SUBJECT, TEXT)

	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_password)
		server.sendmail(FROM, TO, message)
		server.close()

		logger.info(" successfully sent mail")
	except SMTPException as err:
		logger.error("ERR: could not send mail")
		logger.error(err)

