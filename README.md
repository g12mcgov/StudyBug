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
  
Depending on the machine running StudyBug, performance is largely bounded by CPU power. This is because the <code>multiprocessing</code> module distributed workload across each core.

Installing:
========

First clone the GitHub repository and <code>cd</code> into the root directory, <code>StudyBug</code>.

To install StudyBug you <b>must</b> have <code>Python 2.7</code> installed.

You also need to install Node.js. If you're on a mac simply type the following:

<code>brew install node</code>

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

In the <config> directory, open up the <code>studybug.cfg</code> file. It will look like this:

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


Logging
========

StudyBug V2 makes extensive use of logging, making it now easier to track any bugs/failed bookings. Each time the script is run, it generates a log block, tracking the flow of methods throughout the script. An example is attached below:

    2015-01-07 22:41:48 [ MainThread ] [ INFO ] : //NEW LOG BLOCK --------------------
    2015-01-07 22:41:48 [ MainThread ] [ INFO ] :  Beginning StudyBug at 2015-01-07 22:41:48.654414
    2015-01-07 22:41:49 [ MainThread ] [ WARNING ] : No available time slots for room: room-225 between 11:30 AM and 3:00 AM
    2015-01-07 22:41:49 [ MainThread ] [ INFO ] : Confirming...
    2015-01-07 22:41:52 [ MainThread ] [ INFO ] : Checking user mcgoga12
    2015-01-07 22:41:57 [ MainThread ] [ INFO ] : Checking user kleitc13
    2015-01-07 22:42:02 [ MainThread ] [ INFO ] : Checking user diazja13
    2015-01-07 22:42:07 [ MainThread ] [ INFO ] : Checking user keanns13
    2015-01-07 22:42:11 [ MainThread ] [ INFO ] : --------------------

This is a block taken when all the rooms were booked between the designated times. 

These logs are stored in the <code>log/logs</code> directory, under the alias <code>studybug.log</code>.

StudyBug will also soon have feed to [Loggly](https://www.loggly.com/), so we can monitor our logs in the cloud and see specific metrics. This is currently being setup and will be implemented shortly.

Result
========

When StudyBug successfully runs, it sends subscribed users an email with a log of what room(s) it booked and times. Check it out:

![demoPic](http://i1158.photobucket.com/albums/p618/g12mcgov/Screenshot2014-12-30205254.png)

