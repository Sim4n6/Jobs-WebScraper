import requests
from bs4 import BeautifulSoup
import sys

url_2_scrape = "https://www.python.org/jobs/location/"
base_url = "https://www.python.org/"


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
	#  or maybe "montreal-quebec-canada"
	web_scrape("telecommute")
	web_scrape("montreal-quebec-canada")
