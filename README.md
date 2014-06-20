StudyBug
========

An automated web-crawler hosted through Heroku whose purpose is to book study rooms each night at midnight in the Z. Smith Reynold's Library at Wake Forest University, Winston-Salem, NC. This project was built as an academic resource and in no way designed to be malicious. 

It makes use of phantomJS web stack. We first elected to use Selenium webdriver but ran into performance issues since it required a browser to be opened while running. We then switched to phantomJS because it is headless.

Requirements
========

Python 2.7
