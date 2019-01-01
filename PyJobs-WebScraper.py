import requests
from bs4 import BeautifulSoup
import sys
from urllib import robotparser


def web_scrape(location):

	# get a HTTP response from the URL
	resp = requests.get(url_2_scrape+location)

	# parse it with beautiful soup
	soup = BeautifulSoup(resp.text, 'html.parser')
	print(">>" + soup.title.string)
	if soup.title.string != "Python Job Board | Python.org":
		print("please, update the Web scraper.")
		sys.exit()

	# extract <li> of a job general description
	job_urls = []
	for liJob in soup.div.ol.find_all("li"):
		print("Company:", base_url+liJob.h2.a.get('href'), " ", liJob.h2.a.string)
		job_urls.append(base_url+liJob.h2.a.get('href'))
	return job_urls


# extract job content and print it
def extract_job_content(job_url):
	for url in job_url:
		resp = requests.get(url)
		if resp.status_code == 200:
			soup = BeautifulSoup(resp.text, 'html.parser')
			print(">>>> Job title: " + soup.find('title').string)
			#for req in soup.find('h2', text='Requirements').next_siblings():
			#	print("+ >>>> " + req.string)


if __name__ == "__main__":

	url_2_scrape = "https://www.python.org/jobs/location/"
	base_url = "https://www.python.org"

	robot_parser = robotparser.RobotFileParser()
	robot_parser.set_url(base_url+"/robots.txt")
	robot_parser.read()
	if robot_parser.can_fetch('*', url_2_scrape+"*"):
		print("You can fetch : " + url_2_scrape)

		# or maybe "montreal-quebec-canada"
		print("----")
		job_urls1 = web_scrape("telecommute")

		# or maybe "toronto-ontario-canada"
		print("----")
		job_urls2 = web_scrape("toronto-ontario-canada")
		extract_job_content(job_urls2)
	else:
		print("You cannot fetch : " + url_2_scrape + "*")


