#!/usr/bin/python

# Name: StudyBug 
# File: /StudyBug/logging/log.py
#
# Author(s): Grant McGovern
# Date: Tue 6 Jan 2015 
#
# URL: www.github.com/g12mcgov/studybug
#
# ~ Setups a logging class to wrap python's built-in logger ~
#
#

import logging

## Setsup a logger for the entire application to use
def configLogger(name):
	## Make it so that all methods can reach it
	logger = logging.getLogger(name)
	#handler = logging.FileHandler('log/logs/studybug.log')
	handler = logging.StreamHandler()
	
	formatter = logging.Formatter(
		'%(asctime)s [ %(threadName)s ] [ %(levelname)s ] : %(message)s',
		'%Y-%m-%d %H:%M:%S'
		)
	
	handler.setFormatter(formatter)
	
	logger.addHandler(handler) 
	logger.setLevel(logging.DEBUG) 

	# sendToLoggly()
	return logger