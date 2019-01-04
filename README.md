# PyJobs-WebScraper
A simple job offer web scraper based on location using *beautifulsoup4* and *requests* libs in *python3*. 


App functionnalities : 
--------
 - The app web scrapes from python.org/jobs offers board based on location.
 - It uses Requests lib for handling a simple HTTP get of URLs.
 - It uses beautifulsoup4 for parsing html content.
 - It stores the results in XLSX file, thanks to Xlsxwriter module.

TODOS : 
-------
 - [x] add logging capabilities.
 - [ ] make a recursive web scraping 
 - [ ] measure and print the duration of the web scraping
 - [ ] scrape other websites.

INSTALL
----
 Clone the repository from github : 

    $ git clone https://github.com/Sim4n6/PyJobs-WebScraper.git PyJob-WebScraper
    $ cd PyJob-WebScraper

Create a virtual environnement on linux : 

    $ python3 -m venv venv
    $ source venv/bin/activate
    
Create a virtual environnement on windows :

    $ python3 -m venv venv
    $ venv\Scripts\activate.bat
    
Install the necessary packages: 
    
    $ pip3 install -r requirements.txt
   
Run
---
On linux :

    $ python PyJobs-WebScraper.py

On Windows :

    > python PyJobs-WebScraper.py
