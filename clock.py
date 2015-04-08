# Name: StudyBug 
# File: /StudyBug/clock.py
#
# Author(s): Grant McGovern
# Date: Tue 6 Jan 2015 
#
# URL: www.github.com/g12mcgov/studybug
#
# ~ Heroku add-on Scheduler is a "best-guess" scheduler
# 	this means, it doesn't always run at the precise time.
#	as a patch, we can use the APScheduler module and
#	leverage it against Heroku's "clock" type process. ~
#
import sys
import logging

logging.basicConfig()

sys.path.append('main')

#from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.scheduler import Scheduler
from main import main

#sched = BlockingScheduler()
sched = Scheduler()

# Executes every night at 5:00am UTC time | 12:00am (midnight) Winston-Salem, NC time
#@sched.scheduled_job('cron', hour=9, minute=12, misfire_grace_time=20)
def job():
	print "In here"
	main()
    
sched.add_job(job, 'cron', hour=9, minute=17, misfire_grace_time=20)
sched.start()

# DEBUG 
# if __name__ == '__main__':
#   pass 
while True:
	pass