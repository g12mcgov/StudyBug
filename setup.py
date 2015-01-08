#!/usr/local/bin/python

## 
## Created by: Grant McGovern 
## Date: 18 July 2014 
## Purpose: Setup environment for GroupMeCli.
## 

from setuptools import setup, find_packages

## Get our requirements from our .txt file
with open('requirements.txt') as requirements:
	modules = [line.strip('\n') for line in requirements]

setup(name = 'StudyBug',
	version = '0.2a',
	description = 'An automated web-crawler hosted through Heroku whose purpose is to book study rooms each night at midnight in the Z. Smith Reynolds Library at Wake Forest University, Winston-Salem, NC.',
	author = 'Grant McGovern, Gaurav Sheni, & Nate Dehorn',
	author_email = 'mcgoga12@wfu.edu',
	install_requires = modules
)
