# PyJobs-WebScraper
A simple python job offers web scraper using *beautifulsoup4* and *requests* modules in *python3*. 


App functionnalities : 
--------
 - The app web scrapes from www.python.org/jobs offers board based on location.
 - It web scrapes from www.afpy.org/posts/emplois offers.
 - It uses Requests module for handling a simple HTTP get of URLs content.
 - It uses beautifulsoup4 module for parsing html content.
 - It stores the results in XLSX file, thanks to Xlsxwriter module.


INSTALL
----
 Clone the repository from github : 

    $ git clone https://github.com/Sim4n6/PyJobs-WebScraper.git PyJobs-WebScraper
    $ cd PyJobs-WebScraper

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

    $ python3 PyJobs-WebScraper.py

On Windows :

    > python3 PyJobs-WebScraper.py
