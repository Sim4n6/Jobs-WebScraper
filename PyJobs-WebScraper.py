import datetime as dt
import logging
import sys

import feedparser

# user modules
from common.Decorators import log_decorator
from common.Xlsx_manip import save_to_xlsx
from common.csv_manip import from_csv, to_csv, is_csv_exist
from web_scrape.web_scrape_board import extract_job_content, web_scrape, is_allowed_by_robot
from web_scrape.web_scrape_feed import extract_job_offer_from_feed, print_feed_infos


@log_decorator
def web_scrape_demo(location, url_2_scrape):
	""" Web scrape the location, extract the job offer urls and then store to xlsx """

	urls = set()
	url = ""
	if is_csv_exist("./saved_jobs/" + "scraped_urls__" + location + ".csv"):
		urls_from_csv = from_csv("./saved_jobs/" + "scraped_urls__" + location + ".csv")
	else:
		urls_from_csv = set()

	job_urls = web_scrape(location, url_2_scrape)

	if url in job_urls and url not in urls_from_csv:
		urls.add(url)

	list_job_offers = extract_job_content(urls)

	for url in urls:
		job_urls.append(url)
	to_csv(job_urls, "scraped_urls__" + location + ".csv")

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
