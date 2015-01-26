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

sys.path.append('main')

from main import main
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
#@sched.scheduled_job('interval', minutes=1)
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17, minute=25)
def scheduled_job():
	main()
    
sched.start()

# DEBUG 
# while __name__ == '__main__':
#   pass