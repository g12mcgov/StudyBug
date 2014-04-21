#!/usr/bin/python

#### Header file that contains Student's usernames and passwords
import datetime 
import sys 

class User:

	global_count = 0 # keeps track of a global count of how many Keys have been used 

	def __init__(self, username, key):
		self.username = username
		self.key = key
		User.global_count += 1

	def showGlobalCount(self):
		print "Number of Keys: %d" % global_count

	def showKeys(self):
		print "username: " + self.username + '\n'
		print "key: " + self.key + '\n'

	def getusername(self):
		return self.username

	def getkey(self):
		return self.key

