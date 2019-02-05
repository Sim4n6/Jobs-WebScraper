import csv
import os

from common.Decorators import log_decorator


@log_decorator
def to_csv(set_urls, csvfilename):
	if set_urls:
		with open(csvfilename, 'w', newline='') as csvfile:
			csv_writer = csv.writer(csvfile, delimiter=' ')
			for url in set_urls:
				csv_writer.writerow([url])


@log_decorator
def from_csv(csvfilename):
	set_urls = set()
	with open(csvfilename, 'r') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=' ')
		for row in csv_reader:
			set_urls.add(*row)
	return set_urls


@log_decorator
def is_csv_exist(csvfilename):
	return os.path.exists(csvfilename)
