![StudyBug](http://i1158.photobucket.com/albums/p618/g12mcgov/Untitleddrawing-1.png)
========

An automated web-crawler hosted through Heroku whose purpose is to book study rooms each night at midnight in the [Z. Smith Reynold's Library](https://zsr.wfu.edu/) at Wake Forest University, Winston-Salem, NC. This project was built as an academic resource and in no way designed to be malicious. 

Architecture
========

StudyBug makes use of the [PhantomJS](http://phantomjs.org/) web stack. PhantomJS can now be piggybacked off of [Selenium](http://www.seleniumhq.org/), which combines the powerful functionality of Selenium with the headless nature of PhantomJS.

One the of the inherit problems with StudyBug V1 was that it was slow because it booked 2-hour blocks one at a time, refreshing the web-driver each time so as to make sure it wasn't booking a room that had been reserved in the time it took to execute the script. As a result, we saw sub-optimal performance, often resulting in random time blocks not being booked.

However, StudyBug V2 books studyrooms much differently. Here's how it works:

  * 1) Scrapes ZSR website for HTML
  * 2) Parses HTML, finding open rooms
  * 3) Divides list of open rooms into chunks of 4
  * 4) Assigns a chunk to each user 
  * 5) Using multiprocessing, creates a pool of "bookRoom()" processes
  * 6) Each process is given an User object with the 4 time slots
  * 7) Each process then opens a PhantomJS webdriver and books the room
  * 8) Checks to see which rooms we reserved 
  * 9) Sends an email with the successfully reserved rooms
  
Depending on the machine running StudyBug, performance is largely bounded by CPU power. This is because the <code>multiprocessing</code> module distributes workload across each core.

Installing:
========

First clone the GitHub repository and <code>cd</code> into the root directory, <code>StudyBug</code>.

To install StudyBug you <b>must</b> have <code>Python 2.7</code> installed.

You also need to install Node.js. 

<b>Mac OS X</b>:
	
	brew install node

<b>Linux</b>:
	
	sudo apt-get install npm
	sudo ln -s /usr/bin/nodejs /usr/bin/node

<b>Windows</b>:
	
[See here.](http://blueashes.com/2011/web-development/install-nodejs-on-windows/)

Now, using Node's package manager, <code>npm</code> run:

<code>npm -g install phantomjs</code>


If everything went well, you now need to install the following dependecies. As any good Python programmer would, I suggest creating a virtual environment: (<code>mkvirtualenv studybug</code>) 

    EasyProcess==0.1.6
    PyVirtualDisplay==0.1.5
    StudyBug==0.1a
    beautifulsoup4==4.3.2
    selenium==2.44.0
    simplejson==3.6.5
    wsgiref==0.1.2

To do this, run the following command:

<b>Mac OS X</b>:
  * <code>sudo pip install requirements.txt</code>
  
<b>Linux/Windows</b>:
  * <code>pip install requirements.txt</code>

If all checked out, see below for documentation on how to run it.

Running
=========

In the <code>config</code> directory, open up the <code>studybug.cfg</code> file. It will look like this:

    # Set up basic config for StudyBug
    [studybug]
    ROOM=225
    START_TIME=11:30 AM
    END_TIME=3:00 AM
    URL=http://zsr.wfu.edu/studyrooms/

In this file you can specify what room you would like to book, as well as a <code>START TIME</code> and <code>END TIME</code>. This is the timerange in which you would like to book a studyroom. This was strategically added as a parameter because we don't really care about rooms between certain hours (i.e. between 3:00AM and 11:30AM). 

Lastly, the URL base is defined which should remained <b>unchanged</b>.

To run, simply open up a Terminal and execute:
  * <code>python main.py</code>

Currently, StudyBug is being run as a nightly job via [Heroku](http://www.heroku.com). Heroku is pretty easy to setup and has the advantage that uses <code>git</code> to commit code. Heroku also has a nice Scheduler add-on and awesome logging configurations, making it the best possible choice. 

However, you can use really whatever you like. You could schedule StudyBug via Cron, or even host it on a cloud-service such as Amazon EC2, etc...

If you'd like to deploy your own instance to Heroku, you can do so here:

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)


Logging
========

StudyBug V2 makes extensive use of logging, making it now easier to track any bugs/failed bookings. Each time the script is run, it generates a log block, tracking the flow of methods throughout the script. An example is attached below:

    	2015-01-08 22:21:30 [ MainThread ] [ INFO ] : -------- NEW LOG BLOCK ---------------
		2015-01-08 22:21:30 [ MainThread ] [ INFO ] :  beginning StudyBug at 2015-01-08 22:21:30.858987
		2015-01-08 22:21:30 [ MainThread ] [ INFO ] :  requesting http://zsr.wfu.edu/studyrooms/2015/01/12
		2015-01-08 22:21:32 [ MainThread ] [ INFO ] :  total available time slots: 2
		2015-01-08 22:21:32 [ MainThread ] [ INFO ] :  total users: 4
		2015-01-08 22:21:32 [ MainThread ] [ INFO ] :  creating thread pool... 
		2015-01-08 22:21:32 [ MainThread ] [ INFO ] :  kleitc13 - booking rooms
		2015-01-08 22:21:32 [ MainThread ] [ INFO ] :  mcgoga12 - booking rooms
		2015-01-08 22:21:32 [ MainThread ] [ INFO ] :  diazja13 - booking rooms
		2015-01-08 22:21:32 [ MainThread ] [ INFO ] :  keanns13 - booking rooms
		2015-01-08 22:21:36 [ MainThread ] [ INFO ] :  mcgoga12 - clicking on individual rooms...
		2015-01-08 22:21:36 [ MainThread ] [ INFO ] :  mcgoga12 - clicking on //*[@id='room-225']/dd[18]
		2015-01-08 22:21:36 [ MainThread ] [ INFO ] :  mcgoga12 - successfully clicked on all rooms
		2015-01-08 22:21:36 [ MainThread ] [ INFO ] :  mcgoga12 - clicking on save for user
		2015-01-08 22:21:37 [ MainThread ] [ INFO ] :  diazja13 - clicking on individual rooms...
		2015-01-08 22:21:37 [ MainThread ] [ INFO ] :  diazja13 - clicking on //*[@id='room-225']/dd[24]
		2015-01-08 22:21:37 [ MainThread ] [ INFO ] :  diazja13 - successfully clicked on all rooms
		2015-01-08 22:21:37 [ MainThread ] [ INFO ] :  diazja13 - clicking on save for user
		2015-01-08 22:21:38 [ MainThread ] [ INFO ] :  mcgoga12 - filling in username 
		2015-01-08 22:21:38 [ MainThread ] [ INFO ] :  mcgoga12 - filling in password 
		2015-01-08 22:21:38 [ MainThread ] [ INFO ] :  mcgoga12 - clicking on submit 
		2015-01-08 22:21:41 [ MainThread ] [ INFO ] :  diazja13 - filling in username 
		2015-01-08 22:21:41 [ MainThread ] [ INFO ] :  diazja13 - filling in password 
		2015-01-08 22:21:41 [ MainThread ] [ INFO ] :  diazja13 - clicking on submit 
		2015-01-08 22:21:41 [ MainThread ] [ INFO ] :  Executed in 0:00:11.029330 seconds
		2015-01-08 22:21:41 [ MainThread ] [ INFO ] :  confirming...
		2015-01-08 22:21:45 [ MainThread ] [ INFO ] :  checking user mcgoga12...
		2015-01-08 22:21:47 [ MainThread ] [ INFO ] :  mcgoga12 booked Reserved: Room 225 3:00 PM  
		2015-01-08 22:21:47 [ MainThread ] [ INFO ] :  mcgoga12 booked Reserved: Room 225 3:30 PM  
		2015-01-08 22:21:47 [ MainThread ] [ INFO ] :  mcgoga12 booked Reserved: Room 225 4:00 PM  
		2015-01-08 22:21:47 [ MainThread ] [ INFO ] :  mcgoga12 booked Reserved: Room 225 5:00 PM  
		2015-01-08 22:21:51 [ MainThread ] [ INFO ] :  checking user kleitc13...
		2015-01-08 22:21:55 [ MainThread ] [ INFO ] :  kleitc13 booked Reserved: Room 225 5:30 PM  
		2015-01-08 22:21:55 [ MainThread ] [ INFO ] :  kleitc13 booked Reserved: Room 225 6:00 PM  
		2015-01-08 22:21:55 [ MainThread ] [ INFO ] :  kleitc13 booked Reserved: Room 225 6:30 PM  
		2015-01-08 22:21:55 [ MainThread ] [ INFO ] :  kleitc13 booked Reserved: Room 225 7:00 PM  
		2015-01-08 22:22:02 [ MainThread ] [ INFO ] :  checking user diazja13...
		2015-01-08 22:22:04 [ MainThread ] [ INFO ] :  diazja13 booked Reserved: Room 225 8:00 PM  
		2015-01-08 22:22:04 [ MainThread ] [ INFO ] :  diazja13 booked Reserved: Room 225 8:30 PM  
		2015-01-08 22:22:04 [ MainThread ] [ INFO ] :  diazja13 booked Reserved: Room 225 9:00 PM  
		2015-01-08 22:22:04 [ MainThread ] [ INFO ] :  diazja13 booked Reserved: Room 225 9:30 PM  
		2015-01-08 22:22:08 [ MainThread ] [ INFO ] :  checking user keanns13...
		2015-01-08 22:22:13 [ MainThread ] [ INFO ] :  sending email...
		2015-01-08 22:22:14 [ MainThread ] [ INFO ] :  successfully sent mail
		2015-01-08 22:22:14 [ MainThread ] [ INFO ] : --------------------

This is a block taken when all the rooms were booked between the designated times. 

These logs are stored in the <code>log/logs</code> directory, under the alias <code>studybug.log</code>.

StudyBug will also soon feed to [Loggly](https://www.loggly.com/), so we can monitor our logs in the cloud and see specific metrics. This is currently being setup and will be implemented shortly.

Result
========

When StudyBug successfully runs, it sends subscribed users an email with a log of what room(s) it booked and times. Check it out:

![demoPic](http://i1158.photobucket.com/albums/p618/g12mcgov/Screenshot2015-01-08000615.png)

License
=========

The MIT License (MIT)

Copyright (c) 2014 Grant McGovern, Gaurav Sheni

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

