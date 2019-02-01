from bs4 import BeautifulSoup
from urllib import robotparser, parse
import datetime as dt
import logging
import pprint
import requests
import sys
import feedparser

# user modules
from JobOffer import JobOffer
from Decorators import duration_decorator, log_decorator
from csv_manip import from_csv, to_csv
from Xlsx_manip import save_to_xlsx


@duration_decorator
@log_decorator
def extract_job_content_feed_url(feed_url_job):
	""" Web scrape a url from feed """

	# get a HTTP response from the URL
	resp = requests.get(feed_url_job)

	if resp.status_code == 200:
		soup = BeautifulSoup(resp.text, 'html.parser')

		d_scraped = dict()
		title = soup.find('h1').text
		descr = soup.find('article')
		if descr:
			d_scraped["desc"] = descr.text
		else:
			d_scraped["desc"] = ""
		d_scraped["res"] = ""
		d_scraped["req"] = ""
		comp = soup.find('aside')
		if comp:
			d_scraped["comp"] = comp.find('h2').text
		else:
			d_scraped["comp"] = ""
		d_scraped["contact"] = soup.find('aside').text
		url_s = feed_url_job
		return JobOffer(title, d_scraped, url_s)

	else:
		logging.warning("A get URL did not been reached")


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


@log_decorator
def web_scrape_demo(location, url_2_scrape):
	""" Web scrape the location, extract the job offer urls and then store to xlsx """

	urls_from_csv = from_csv("scraped_urls__" + location + ".csv")
	urls = set()
	url = ""
	job_urls = web_scrape(location, url_2_scrape)
	if url in job_urls and url not in urls_from_csv:
		urls.add(url)

	list_job_offers = extract_job_content(urls)

	# FIXME in case urls contain something it need to be added to csv , try it now
	for url in urls:
		job_urls.append(url)
	to_csv(job_urls, "scraped_urls__" + location + ".csv")

	save_to_xlsx("jobs--" + str(dt.date.today()) + "__" + location + ".xlsx", list_job_offers)


@log_decorator
def print_feed_infos(feed_parsed):
	""" print feed informations to stdout """

	print(">>", feed_parsed.feed.title, feed_parsed.feed.link)
	print("lang:", feed_parsed.feed.language, "version:", feed_parsed.version)
	print("Number of entries can be parsed : ", len(feed_parsed.entries))


@log_decorator
def extract_job_offer_from_feed(feed_parsed):

	# don't web scrape twice
	urls_from_csv = from_csv("scraped_urls__" + "afpy" + ".csv")
	urls = set()
	for entry in feed_parsed.entries:
		if entry.link not in urls_from_csv:
			urls.add(entry.link)

	list_job_offers = set()
	print("Number of entries will be parsed : ", len(urls))
	for url in urls:
		current_job = extract_job_content_feed_url(url)
		list_job_offers.add(current_job)

	# to csv
	# FIXME in case of urls var contains a url, check now
	for url in urls:
		urls_from_csv.append(url)
	to_csv(urls_from_csv, "scraped_urls__" + "afpy" + ".csv")

	return list_job_offers


@log_decorator
def feedparser_demo():
	# feed parsing
	feed_url = "https://www.afpy.org/feed/emplois/rss.xml"
	feed_parsed = feedparser.parse(feed_url)

	# print feed informations to stdout
	print_feed_infos(feed_parsed)

	# store feed infos of entries to xlsx
	lst_job_offers = extract_job_offer_from_feed(feed_parsed)

	# save to xlsx file
	save_to_xlsx("jobs--" + str(dt.date.today()) + "__afpy" + ".xlsx", lst_job_offers)


if __name__ == "__main__":

	url_2_scrape = "https://www.python.org/jobs/location/"

	logging.basicConfig(filename='journal.log', filemode='w', level=logging.INFO)
	logging.info("The app " + str(sys.argv[0]) + " started at " + str(dt.datetime.now()))

	if is_allowed_by_robot(url_2_scrape):
		print("You can fetch : " + url_2_scrape)

		# Demo 1 : Web scrape the "telecommute", extract the job offer urls and then store to xlsx
		web_scrape_demo("telecommute", url_2_scrape)

		# Demo 2 : Web scrape the toronto-ontario-canada, extract the job offer urls and then store to xlsx
		web_scrape_demo("toronto-ontario-canada", url_2_scrape)

		# Demo 3 : Web scrape the montreal-quebec-canada, extract the job offer urls and then store the results to xlsx
		web_scrape_demo("montreal-quebec-canada", url_2_scrape)

	else:
		print("You cannot fetch : " + url_2_scrape + "*")

	# Demo 4 : Feed parsing RSS of afpy.org
	feedparser_demo()
