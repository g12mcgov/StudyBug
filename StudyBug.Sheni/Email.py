#!/usr/bin/python

# This file is simply designed to contain the email:
import smtplib
import time
import datetime

def sendEmail(formatted_times):
	now = datetime.datetime.now()
	startdate=now.strftime("%m/%d/%Y")
	date = datetime.datetime.strptime(startdate, "%m/%d/%Y")
	endate = date + datetime.timedelta(days=4)
	newdate = endate.strftime("%m/%d/%Y")

	length = len(formatted_times)

	gmail_user = "mcgoga12@wfu.edu"
	gmail_password = "#######" #secret key 

	FROM = gmail_user
	TO = ['mcgoga12@wfu.edu']
	SUBJECT = "StudyBug - Study Rooms for %s" % newdate
	TEXT = """
This is an automated email from StudyBug.

We wanted to let you know that the following studyroom times were booked for %s:

%s

Thank You, 

StudyBug 

-----------------------------------------------------------------------------------------------
Developed with Love by Grant McGovern, Gaurav Sheni, & Nate DeHorn 
-----------------------------------------------------------------------------------------------

Check out the project page!: https://github.com/g12mcgov/StudyBug

""" % (newdate, formatted_times) #"\n".join(formatted_times)  

	message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
	""" %(FROM, ",".join(TO), SUBJECT, TEXT)

	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(gmail_user,gmail_password)
		server.sendmail(FROM, TO, message)
		#server.quit()
		server.close()
	except:
		print "Failed to send mail."
