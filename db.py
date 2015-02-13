#!/usr/bin/python

# Name: StudyBug 
# File: /StudyBug/db.py
#
# Author(s): Grant McGovern
# Date: Tue 6 Jan 2015 
#
# URL: www.github.com/g12mcgov/studybug
#
# ~ Provides a simple MongoDriver class for interacting with MongoDB ~
#
#

import pymongo 
import logging
import datetime

## Local Includes ##
from loggings.loger import configLogger

logger = logging.getLogger('root')

class MongoDriver:
	def __init__(self, MONGO_HOST):
		self.client = pymongo.MongoClient(MONGO_HOST)
		self.db = self.checkIfConnected()

	# Add an entry to Mongo 
	def addEntry(self, rooms, expected, timeRange, room, todayDate, endDate):
		# Get today's date
		today = datetime.datetime.now().strftime("%m/%d/%Y")
		# Remove the corresponding entry on today's date
		self.cleanDB({"todayDate": today})

		try:
			# Insert our BSON block into Mongo
			self.db.studybug.save({
				"bookings": rooms,
				"expected": expected,
				"timeRange": timeRange, 
				"room": room, 
				"todayDate": todayDate, 
				"endDate": endDate
				})

			logger.info(" successfully inserted (1) row into Mongo")
		except pymongo.errors.OperationFailure as err:
			logger.error(" ERR: Failed to insert into Mongo: " + str(err))

	# Remove our most recent entry to insert the new one 
	def cleanDB(self, query):
		try:
			self.db.studybug.remove(query)
			logger.info(" successfully removed (1) row from Mongo")

		except pymongo.errors.OperationFailure as err:
			logger.error(" ERR: Failed to remove row from Mongo: " + str(err))


	# Call Immediately upon Class Initialization --> Check if Mongo is up and running
	def checkIfConnected(self):
		try:
			db = self.client.heroku_app33177236
			logger.info(" MongoDB connected ")
			return db

		except: 
			logger.error(" ERR: MongoDB connection unresolved ")
		
# Debug 
# if __name__ == "__main__":
# 	host = "mongodb://admin:nantucket@ds041581.mongolab.com:41581/heroku_app33177236"
# 	mongo = MongoDriver(host)