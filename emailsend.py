#!/usr/bin/python

# This file is simply designed to contain the email:
import smtplib
import time
import logging
import datetime
from smtplib import SMTPException

def sendEmail(confirmationList, room):
	now = datetime.datetime.now()
	
	startdate = now.strftime("%m/%d/%Y")
	date = datetime.datetime.strptime(startdate, "%m/%d/%Y")
	
	endate = date + datetime.timedelta(days=4)
	newdate = endate.strftime("%m/%d/%Y")

	length = len(confirmationList)

	gmail_user = "studybugauto@gmail.com"
	gmail_password = "grantmcgovern1" #secret key 

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
	except SMTPException as err:
		logging.error("ERR: Could not send mail")
		logging.error(err)

