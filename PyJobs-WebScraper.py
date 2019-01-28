from bs4 import BeautifulSoup
from urllib import robotparser
import datetime as dt
import logging
import pprint
import requests
import xlsxwriter
import sys
import os
import feedparser

# user modules
from JobOffer import JobOffer


def duration_decorator(func):

	def wrapper(*args, **kwargs):
		t_before = dt.datetime.now()
		output = func(*args, **kwargs)
		delta_t = dt.datetime.now() - t_before
		print(f"Execution duration of {func.__name__} is : {delta_t.seconds} in seconds and {delta_t.microseconds} in microseconds.")
		return output

	return wrapper


def log_decorator(func):
	def wrapper(*args, **kwargs):
		logging.info(f"Call made to {func.__name__}")
		return func(*args, **kwargs)
	return wrapper


@duration_decorator
@log_decorator
def extract_job_content_feed_url(feed_url_job):
	""" Web scrape a url from feed """

	# get a HTTP response from the URL
	resp = requests.get(feed_url_job)

	if resp.status_code == 200:
		soup = BeautifulSoup(resp.text, 'html.parser')

		d_title, d_job, d_restr, d_req, d_company, d_cti, d_url = dict(), dict(), dict(), dict(), dict(), dict(), dict()
		d_title["title"] = soup.find('h1').text
		descr = soup.find('article')
		if descr:
			d_job["desc"] = descr.text
		else:
			d_job["desc"] = ""
		d_restr["res"] = ""
		d_req["req"] = ""
		comp = soup.find('aside').find('h2')
		if comp:
			d_company["comp"] = comp.text
		else:
			d_company["comp"] = ""
		d_cti["contact"] = soup.find('aside').text
		d_url["url"] = feed_url_job
		return JobOffer(d_title, d_job, d_restr, d_req, d_company, d_cti, d_url)

	else:
		logging.warning("A get URL did not been reached")


@log_decorator
def web_scrape(location_rel_path):
	""" Web scrape a url based on the location relative path """

	# get a HTTP response from the URL
	resp = requests.get(url_2_scrape + location_rel_path)
	logging.info("A get request made for URL : " + url_2_scrape + location_rel_path)

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

	list_job_offers = []
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
			d_title, d_company, d_req, d_restr, d_cti, d_job, d_url = dict(), dict(), dict(), dict(), dict(), dict(), dict()
			d_title["title"] = soup.find('title').string

			# Company name parsing
			lst_company = soup.find('h1', class_='listing-company')
			if lst_company:
				span_company = lst_company.find('span', class_='company-name')
				d_company["company"] = span_company.contents[2].strip()

			# Requirements parsing
			req = soup.find('h2', text='Requirements')
			if req:
				for k, p_req in enumerate(req.find_next_siblings('p')):
					if p_req.string is not None:
						d_req["req " + str(k)] = p_req.string
					else:
						d_req["req " + str(k)] = "0"

			# Restrictions parsing
			restr = soup.find('h2', text='Restrictions')
			if restr:
				ul = restr.find_next_sibling('ul')
				for k, li in enumerate(ul.find_all('li')):
					d_restr["restr " + str(k)] = li.text

			# Contact info parsing
			cti = soup.find('h2', text='Contact Info')
			if cti:
				ul = cti.find_next_sibling('ul')
				for k, li in enumerate(ul.find_all('li')):
					d_cti["Contact " + str(k)] = li.text

			# Job description parsing
			job_desc = soup.find('h2', text='Job Description')
			if job_desc:
				for k, p in enumerate(job_desc.find_next_siblings('p')):
					d_job["Job descr " + str(k)] = p.text

			# Job URL
			d_url["Url"] = url

			# Current Job Offer stored in an object
			current_job = JobOffer(d_title, d_job, d_restr, d_req, d_company, d_cti, d_url)
			list_job_offers.append(current_job)

		else:

			# logging the result of the request code
			logging.warning(
				"Request status code " + str(resp.status_code) + " is returned for a get request URL " + url)

	return list_job_offers


@log_decorator
def is_allowed_by_robot(base_url, url_2_scrape):
	"""Check whether the robots.txt allows the scraping of the URL using robotparser from urllib """

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
def save_to_xlsx(xlsx_filename, list_job_offers):
	""" Save the dictionaries to xlsx file using Xlsx-Writer """

	logging.info("Xlsx writting started at " + str(dt.datetime.now()) + " to file " + "saved_jobs/" + xlsx_filename)

	# Create directory "saved_jobs" locally
	create_xlsx_dir("saved_jobs")

	# Save to excel file
	workbook = xlsxwriter.Workbook("saved_jobs" + "/" + xlsx_filename)

	# personnalisation
	cell_format = workbook.add_format()
	cell_format.set_bold()
	cell_format.set_font_color('red')

	for i, job_offer in enumerate(list_job_offers):
		# create a sheet for each job offer
		worksheet = workbook.add_worksheet(f"Sheet Offer {str(i)}")

		# write job_offer to worksheet
		write_job_offer_2_worksheet(job_offer, worksheet, cell_format)

	# close workbook
	workbook.close()


@log_decorator
def write_job_offer_2_worksheet(job_offer, worksheet, cell_format):
	""" Write job offer object to worksheet """

	# for each attribute of job_offer obj write the K,V to worksheet
	row = 0
	job_offer_attribs = vars(job_offer)
	for V_attrib in job_offer_attribs.values():
		for key, value in V_attrib.items():
			worksheet.write(row, 0, key, cell_format)
			worksheet.write(row, 1, value)
			row += 1


@log_decorator
def create_xlsx_dir(xlsx_dir):
	""" Create a xlsx directory """
	try:
		os.mkdir(xlsx_dir)
		logging.info("Directory " + xlsx_dir + " created.")
	except FileExistsError:
		logging.warning("Directory " + xlsx_dir + " already exists.")


@log_decorator
def web_scrape_demo(location):
	""" Web scrape the location, extract the job offer urls and then store to xlsx """

	job_urls = web_scrape(location)
	list_job_offers = extract_job_content(job_urls)
	save_to_xlsx("jobs--" + str(dt.date.today()) + "__" + location + ".xlsx", list_job_offers)


@log_decorator
def print_feed_infos(feed_parsed):
	""" print feed informations to stdout """

	print(">>", feed_parsed.feed.title, feed_parsed.feed.link)
	print("lang:", feed_parsed.feed.language, "version:", feed_parsed.version)
	print("Number of entries to be parsed : ", len(feed_parsed.entries))


@log_decorator
def extract_job_offer_from_feed(feed_parsed):

	list_job_offers = []
	for entry in feed_parsed.entries:
		current_job = extract_job_content_feed_url(entry.link)
		list_job_offers.append(current_job)

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

	main_url = "https://www.python.org"
	url_2_scrape = main_url + "/jobs/location/"

	logging.basicConfig(filename='journal.log', filemode='w', level=logging.INFO)
	logging.info("The app " + str(sys.argv[0]) + " started at " + str(dt.datetime.now()))

	if is_allowed_by_robot(main_url, url_2_scrape):
		print("You can fetch : " + url_2_scrape)

		# Demo 1 : Web scrape the "telecommute", extract the job offer urls and then store to xlsx
		web_scrape_demo("telecommute")

		# Demo 2 : Web scrape the toronto-ontario-canada, extract the job offer urls and then store to xlsx
		web_scrape_demo("toronto-ontario-canada")

		# Demo 3 : Web scrape the montreal-quebec-canada, extract the job offer urls and then store the results to xlsx
		web_scrape_demo("montreal-quebec-canada")

	else:
		print("You cannot fetch : " + url_2_scrape + "*")

	# Demo 4 : Feed parsing RSS of afpy.org
	feedparser_demo()
