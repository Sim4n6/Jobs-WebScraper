from bs4 import BeautifulSoup
from urllib import robotparser, parse
import requests
import logging
import pprint
import sys

from Decorators import log_decorator, duration_decorator
from JobOffer import JobOffer


@log_decorator
def web_scrape(location_rel_path, url_2_scrape):
	""" Web scrape a url based on the location relative path """

	# get a HTTP response from the URL
	resp = requests.get(url_2_scrape + location_rel_path)
	logging.info("A get request made for URL : " + url_2_scrape + location_rel_path)

	job_urls = []
	if resp.status_code == 200:

		# logging the result of the request code
		logging.info("Request status code " + str(
			resp.status_code) + " is returned for a get request URL " + url_2_scrape + location_rel_path)

		# parse it with beautiful soup
		soup = BeautifulSoup(resp.text, 'html.parser')
		print(">>" + soup.title.string)
		if soup.title.string != "Python Job Board | Python.org":
			logging.warning("Please, update the web scraper.")
			sys.exit()

		# extract job offer urls from py job location based board
		main_url = parse.urlsplit(url_2_scrape).scheme + "://" + parse.urlsplit(url_2_scrape).netloc
		job_urls = [main_url + li_job.h2.a.get('href') for li_job in soup.div.ol.find_all("li")]

		# pretty printing of the
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(str(len(job_urls)) + " urls will be scraped.")
		pp.pprint(job_urls)

	else:
		logging.warning("Request status code " + str(
			resp.status_code) + " is returned for a get request URL " + url_2_scrape + location_rel_path)

	return job_urls


@duration_decorator
@log_decorator
def extract_job_content(job_urls):
	""" Extract the job offer content and store it in a list """

	list_job_offers = set()
	for url in job_urls:

		# HTTP get request for each URL content
		resp = requests.get(url)

		# HTTP get request response of the URL is OK
		if resp.status_code == 200:

			# logging the result of the request code
			logging.info("Request status code " + str(resp.status_code) + " is returned for a get request URL " + url)

			# parse the response content for each url using beautifulsoup
			soup = BeautifulSoup(resp.text, 'html.parser')

			#
			logging.info("Started parsing " + url)

			# Title parsing
			d_scraped = dict()
			title = soup.find('title').string

			# Company name parsing
			lst_company = soup.find('h1', class_='listing-company')
			if lst_company:
				span_company = lst_company.find('span', class_='company-name')
				d_scraped["company"] = span_company.contents[2].strip()

			# Requirements parsing
			req = soup.find('h2', text='Requirements')
			if req:
				for k, p_req in enumerate(req.find_next_siblings('p')):
					if p_req.string is not None:
						d_scraped["req " + str(k)] = p_req.string
					else:
						d_scraped["req " + str(k)] = ""

			# Restrictions parsing
			restr = soup.find('h2', text='Restrictions')
			if restr:
				ul = restr.find_next_sibling('ul')
				for k, li in enumerate(ul.find_all('li')):
					d_scraped["restr " + str(k)] = li.text

			# Contact info parsing
			cti = soup.find('h2', text='Contact Info')
			if cti:
				ul = cti.find_next_sibling('ul')
				for k, li in enumerate(ul.find_all('li')):
					d_scraped["Contact " + str(k)] = li.text

			# Job description parsing
			job_desc = soup.find('h2', text='Job Description')
			if job_desc:
				for k, p in enumerate(job_desc.find_next_siblings('p')):
					d_scraped["Job descr " + str(k)] = p.text

			# Current Job Offer stored in an object
			current_job = JobOffer(title, d_scraped,  url)
			list_job_offers.add(current_job)

		else:

			# logging the result of the request code
			logging.warning(
				"Request status code " + str(resp.status_code) + " is returned for a get request URL " + url)

	return list_job_offers


@log_decorator
def is_allowed_by_robot(url_2_scrape):
	"""Check whether the robots.txt allows the scraping of the URL using robotparser from urllib """

	# get the network location or base url
	url_parsed = parse.urlsplit(url_2_scrape)
	base_url = parse.urlsplit(url_2_scrape).scheme + "://" + url_parsed.netloc

	# check robots.txt
	robot_parser = robotparser.RobotFileParser()
	robot_parser.set_url(base_url + "/robots.txt")
	robot_parser.read()
	logging.info("Robots.txt is read from " + base_url + "/robots.txt")

	is_allowed = robot_parser.can_fetch('*', url_2_scrape + "*")
	if is_allowed:
		logging.info("It is allowed to web scrape " + url_2_scrape)
	else:
		logging.warning("It is not allowed to web scrape " + url_2_scrape)

	return is_allowed

