# Name: StudyBug 
# File: /StudyBug/helpers/helper.py
#
# Author(s): Grant McGovern
# Date: Tue 6 Jan 2015 
#
# URL: www.github.com/g12mcgov/studybug
#
# ~ Some handy-dandy helper methods ~
#
#

import datetime

# Returns a list in chunked pieces
# 
# For example:
#
#	>> exList = [[1,2], [3,4], [4,5], [6,7]]
#	
#	>> res = chunk(exList, 2)
#
#	>> [[1,2,3,4], [4,5,6,7]]
#

def chunk(input_list, n):
	return [input_list[x:x+n] for x in range(0, len(input_list), n)]

# Given a string time input, returns a datetime object
def parseTime(string):
	return datetime.datetime.strptime(string, "%I:%M %p")
