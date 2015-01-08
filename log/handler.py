# Name: StudyBug 
# File: /StudyBug/logging/logHandler.py
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

class LogHandler:
	def __init__(self):
		self.LOG_FILE = '/logs/studybug.log'
		self.logger = logging.getLogger('studyBugLogger')

	# Takes in a statement to log
	def log(self, statement):
		self.logger.debug(statement)
