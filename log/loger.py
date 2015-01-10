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
import sys
import logging

## Setsup a logger for the entire application to use
def configLogger(name):
	logger = logging.basicConfig( 
    stream=sys.stdout, 
    level=logging.INFO, 
    format="%(asctime)s [ %(threadName)s ] [ %(levelname)s ] : %(message)s'", 
    datefmt='%Y-%m-%d %H:%M:%S' 
	) 

	logger = logging.getLogger(name)

	return logger