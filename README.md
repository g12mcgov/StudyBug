StudyBug
========

An automated web-crawler hosted through Heroku whose purpose is to book study rooms each night at midnight in the Z. Smith Reynold's Library at Wake Forest University, Winston-Salem, NC. This project was built as an academic resource and in no way designed to be malicious. 

It makes use of phantomJS web stack. We first elected to use Selenium webdriver but ran into performance issues since it required a browser to be opened while running. We then switched to phantomJS because it is headless.

Result
========

When it successfully runs, it sends subscribed users an email with a log of what room(s) it booked and times. Check it out:

![demoPic](http://i1158.photobucket.com/albums/p618/g12mcgov/Screenshot2014-12-30205254.png)

Requirements
========

EasyProcess==0.1.6

PyVirtualDisplay==0.1.5

beautifulsoup4==4.3.2

selenium==2.44.0

splinter==0.7.0

wsgiref==0.1.2

