# PyJobs-WebScraper
A simple job offer web scraper based on location using *beautifulsoup4* and *requests* libs in *python3*. 

### App layout 
It web scrapes from python.org/jobs offers board. 

  
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
    
Install the necessary packages including Flask and Pytest: 
    
    $ pip3 install -r requirements.txt
   
Run
---
On linux :

    $ python PyJobs-WebScraper.py

On Windows :

    > python PyJobs-WebScraper.py
