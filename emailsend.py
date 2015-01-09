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

import smtplib
import time
import logging
import datetime
from smtplib import SMTPException
from log.log import configLogger

logger = logging.getLogger('root')

def sendEmail(confirmationList, room, email, password):
	logger.info(" sending email...")
	now = datetime.datetime.now()
	
	startdate = now.strftime("%m/%d/%Y")
	date = datetime.datetime.strptime(startdate, "%m/%d/%Y")
	
	endate = date + datetime.timedelta(days=4)
	newdate = endate.strftime("%m/%d/%Y")

	length = len(confirmationList)

<<<<<<< HEAD
	gmail_user = email
	gmail_password = password
=======
	gmail_user = "studybugauto@gmail.com"
	gmail_password = "******" #secret key 
>>>>>>> 131ecb95ed420e3df4fc64740056728d598c2ec2

	FROM = gmail_user
	TO = ['mcgoga12@wfu.edu']
	SUBJECT = "StudyBug - Study Rooms for %s (%s)" % (newdate, room)
	TEXT = """
This is an automated email from StudyBug.

We wanted to let you know that the following studyroom times were booked for %s:

%s

Thank You, 

StudyBug 

-----------------------------------------------------------------------------------------------
Developed by Grant McGovern & Gaurav Sheni
-----------------------------------------------------------------------------------------------

Check out the project page!: https://github.com/g12mcgov/StudyBug

~ a grantmcgovern build ~	

""" % (newdate, '\n'.join(confirmationList).replace('Reserved: ', '').encode('utf-8')) 

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

