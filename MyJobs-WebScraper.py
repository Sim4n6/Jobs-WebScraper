import requests
from bs4 import BeautifulSoup
import sys
from urllib import robotparser

def web_scrape(location):
	# get a HTTP response from the URL
	resp = requests.get(url_2_scrape+location)

	# parse it with beautiful soup
	soup = BeautifulSoup(resp.text, 'html.parser')
	print(soup.title.string)
	if soup.title.string != "Python Job Board | Python.org":
		print("please, update the Web scraper.")
		sys.exit()
	print("----")
	for liJob in soup.div.ol.find_all("li"):
		print("Company:", base_url+liJob.h2.a.get('href'), " ", liJob.h2.a.string)


if __name__ == "__main__":

	url_2_scrape = "https://www.python.org/jobs/location/"
	base_url = "https://www.python.org/"

	robot_parser = robotparser.RobotFileParser()
	robot_parser.set_url("https://www.python.org/robots.txt")
	robot_parser.read()
	if robot_parser.can_fetch('*', url_2_scrape+"*"):
		print("You can fetch : " + url_2_scrape)

		#  or maybe "montreal-quebec-canada"
		web_scrape("telecommute")
		web_scrape("montreal-quebec-canada")
	else:
		print("You cannot fetch : " + url_2_scrape + "*")


