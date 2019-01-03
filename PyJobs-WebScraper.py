from bs4 import BeautifulSoup
from urllib import robotparser
import requests
import xlsxwriter
import sys

# user modules
from JobOffer import JobOffer


def web_scrape(location):
	""" web scrape a url based on the location """

	# get a HTTP response from the URL
	resp = requests.get(url_2_scrape + location)
	if resp.status_code == 200:

		# parse it with beautiful soup
		soup = BeautifulSoup(resp.text, 'html.parser')
		print(">>" + soup.title.string)
		if soup.title.string != "Python Job Board | Python.org":
			print("please, update the Web scraper.")
			sys.exit()

		# extract job offer urls from py job location based board
		job_urls = [base_url + liJob.h2.a.get('href') for liJob in soup.div.ol.find_all("li")]
		print(job_urls)

	return job_urls


def extract_job_content(job_urls):
	""" extract the job offer content and store it in a list """

	list_job_offers = []
	for url in job_urls:

		# HTTP get request for each URL content
		resp = requests.get(url)

		# HTTP get request response of the URL is OK
		if resp.status_code == 200:

			# parse the response content for each url using beautifulsoup
			soup = BeautifulSoup(resp.text, 'html.parser')

			# Title parsing
			d_title, d_company, d_req, d_restr, d_cti, d_job = dict(), dict(), dict(), dict(), dict(), dict()
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

			# Current Job Offer stored in an object
			current_job = JobOffer(d_title, d_job, d_restr, d_req, d_company, d_cti)
			list_job_offers.append(current_job)

	return list_job_offers


def is_allowed_by_robot(base_url, url_2_scrape):
	"""Check whether the robots.txt allows the scraping of the URL using robotparser from urllib """

	robot_parser = robotparser.RobotFileParser()
	robot_parser.set_url(base_url + "/robots.txt")
	robot_parser.read()
	return robot_parser.can_fetch('*', url_2_scrape + "*")


def save_to_xlsx(xlsx_file, list_job_offers):
	""" Save the dictionaries to xlsx file using Xlsx-Writer """

	# Save to excel file
	workbook = xlsxwriter.Workbook(xlsx_file)

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


if __name__ == "__main__":

	base_url = "https://www.python.org"
	url_2_scrape = base_url + "/jobs/location/"

	if is_allowed_by_robot(base_url, url_2_scrape):
		print("You can fetch : " + url_2_scrape)

		# Demo 1 : Web scrape the telecommute, extract the job offer urls and then store to xlsx
		job_urls = web_scrape("telecommute")
		list_job_offers = extract_job_content(job_urls)
		save_to_xlsx("jobs--telecommute.xlsx", list_job_offers)

		# Demo 2 : Web scrape the toronto-ontario-canada, extract the job offer urls and then store to xlsx
		job_urls = web_scrape("toronto-ontario-canada")
		list_job_offers = extract_job_content(job_urls)
		save_to_xlsx("jobs--toronto-ontario-canada.xlsx", list_job_offers)

		# Demo 3 : Web scrape the montreal-quebec-canada, extract the job offer urls and then store the results to xlsx
		job_urls = web_scrape("montreal-quebec-canada")
		list_job_offers = extract_job_content(job_urls)
		save_to_xlsx("jobs--montreal-quebec-canada.xlsx", list_job_offers)

	else:
		print("You cannot fetch : " + url_2_scrape + "*")
