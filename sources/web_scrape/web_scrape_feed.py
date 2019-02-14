import logging

import requests
from bs4 import BeautifulSoup

from sources.job_offer import JobOffer
from sources.common.Decorators import log_decorator, duration_decorator
from sources.common.db_manip import create_table_db, add_job_link, extract_all_joblinks, set_state


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

	create_table_db()
	for entry in feed_parsed.entries:
		add_job_link(entry.link)

	urls_scraped = extract_all_joblinks(1)
	urls_not_scraped = extract_all_joblinks(-1)

	urls = set()
	for url in urls_not_scraped:
		if url not in urls_scraped:
			urls.add(url)
	print("Number of entries will be parsed : ", len(urls))

	list_job_offers = set()
	for url in urls:
		current_job = extract_job_content_feed_url(url)
		list_job_offers.add(current_job)

	for url in urls:
		add_job_link(url)
		set_state(url, 1)

	return list_job_offers
