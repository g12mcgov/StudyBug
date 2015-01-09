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

class LoggingHandler:
	def __init__(self):
		self.LOG_FILE = '/logs/studybug.log'
		self.logger = logging.getLogger('studyBugLogger')
		
		self.logger.basicConfig(
			filename=self.LOG_FILE,
			level=logging.DEBUG
			)

	# Takes in a statement to log
	def log(self, statement):
		self.logger.debug(statement)
