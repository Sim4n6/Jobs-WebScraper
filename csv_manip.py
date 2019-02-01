import os
import csv

from Decorators import log_decorator


@log_decorator
def to_csv(set_urls, csvfilename):

	# check directory "saved_jobs" exists
	if os.path.isdir("./saved_jobs"):
		with open("saved_jobs/"+csvfilename, 'w', newline='') as csvfile:
			csv_writer = csv.writer(csvfile, delimiter=' ')
			for url in set_urls:
				csv_writer.writerow([url])


@log_decorator
def from_csv(csvfilename):
	set_urls = set()
	with open("saved_jobs/" + csvfilename, 'r') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=' ')
		for row in csv_reader:
			set_urls.add(*row)
	return set_urls
