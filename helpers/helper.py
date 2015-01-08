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
def chunk(seq, size):
        newseq = []
        splitsize = 1.0 / size * len(seq)
        for i in range(size):
                newseq.append(seq[int(round(i*splitsize)):int(round((i+1)*splitsize))])
        return newseq

# Given a string time input, returns a datetime object
def parseTime(string):
	return datetime.datetime.strptime(string, "%I:%M %p")