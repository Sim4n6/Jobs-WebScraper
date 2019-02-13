import datetime as dt
import logging
import sys

import feedparser

# user modules
from sources.common.Decorators import log_decorator
from sources.common.Xlsx_manip import save_to_xlsx
from sources.common.db_manip import create_table_db, add_job_link, extract_all_joblinks, set_state
from sources.web_scrape.web_scrape_board import extract_job_content, web_scrape, is_allowed_by_robot
from sources.web_scrape.web_scrape_feed import extract_job_offer_from_feed, print_feed_infos


@log_decorator
def web_scrape_demo(location, url_2_scrape):
	""" Web scrape the location, extract the job offer urls and then store to xlsx """

	create_table_db()
	job_urls = web_scrape(location, url_2_scrape)
	for url in job_urls:
		add_job_link(url)

	urls_scraped = extract_all_joblinks(1)
	urls_not_scraped = extract_all_joblinks(0)

	urls = set()
	for url in urls_not_scraped:
		if url not in urls_scraped:
			urls.add(url)

	list_job_offers = extract_job_content(urls)
	for url in urls:
		add_job_link(url)
		set_state(url, 1)

	save_to_xlsx("jobs--" + str(dt.date.today()) + "__" + location + ".xlsx", list_job_offers)


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
