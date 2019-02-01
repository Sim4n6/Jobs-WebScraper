import requests
from bs4 import BeautifulSoup
import logging

from common.Decorators import log_decorator, duration_decorator
from common.csv_manip import from_csv, to_csv
from JobOffer import JobOffer


@log_decorator
def print_feed_infos(feed_parsed):
	""" print feed informations to stdout """

	print(">>", feed_parsed.feed.title, feed_parsed.feed.link)
	print("lang:", feed_parsed.feed.language, "version:", feed_parsed.version)
	print("Number of entries can be parsed : ", len(feed_parsed.entries))


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

