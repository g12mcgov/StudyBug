# Name: StudyBug 
# File: /StudyBug/schema.py
#
# Author(s): Grant McGovern
# Date: Tue 6 Jan 2015 
#
# URL: www.github.com/g12mcgov/studybug
#
# ~ Provides a class to store xpath schemas, matching
#	each xpath value (i.e., dd[4], dd[5], etc...)
#	with the correct timestamp. ~
#

class XPathSchema:
	def __init__(self):
		self.schema = {
			'8:00 AM': 1, 
			'8:30 AM': 2, 
			'9:00 AM': 3, 
			'9:30 AM': 4, 
			'10:00 AM': 5, 
			'10:30 AM': 6, 
			'11:00 AM': 7, 
			'11:30 AM': 8, 
			'12:00 PM': 9, 
			'12:30 PM': 10, 
			'1:00 PM': 11, 
			'1:30 PM': 12, 
			'2:00 PM': 13, 
			'2:30 PM': 14, 
			'3:00 PM': 15, 
			'3:30 PM': 16, 
			'4:00 PM': 17, 
			'4:30 PM': 18, 
			'5:00 PM': 19, 
			'5:30 PM': 20, 
			'6:00 PM': 21, 
			'6:30 PM': 22, 
			'7:00 PM': 23, 
			'7:30 PM': 24, 
			'8:00 PM': 25, 
			'8:30 PM': 26, 
			'9:00 PM': 27, 
			'9:30 PM': 28, 
			'10:00 PM': 29, 
			'10:30 PM': 30, 
			'11:00 PM': 31, 
			'11:30 PM': 32
		}

	def getXpath(self, req):
		return self.schema[req]