import requests
from bs4 import BeautifulSoup
import sys
from urllib import robotparser
import xlsxwriter


def web_scrape(location):

	# get a HTTP response from the URL
	resp = requests.get(url_2_scrape+location)

	# parse it with beautiful soup
	soup = BeautifulSoup(resp.text, 'html.parser')
	print(">>" + soup.title.string)
	if soup.title.string != "Python Job Board | Python.org":
		print("please, update the Web scraper.")
		sys.exit()

	# extract <li> of a job general description
	job_urls = []
	for liJob in soup.div.ol.find_all("li"):
		print("Company:", base_url+liJob.h2.a.get('href'), " ", liJob.h2.a.string)
		job_urls.append(base_url+liJob.h2.a.get('href'))
	return job_urls


# extract job content and print it
def extract_job_content(job_url):
	d, d_req, d_restr, d_cti, d_job = dict(), dict(), dict(), dict(), dict()
	for url in job_url:
		resp = requests.get(url)
		if resp.status_code == 200:
			soup = BeautifulSoup(resp.text, 'html.parser')
			print(">>>> Job title: " + soup.find('title').string)
			d["title"] = soup.find('title').string

			req = soup.find('h2', text='Requirements')
			if req:
				for k, p_req in enumerate(req.find_next_siblings('p')):
					print("+ >>>> " + p_req.string)
					d_req["req "+str(k)] = p_req.string

			restr = soup.find('h2', text='Restrictions')
			if restr:
				print("+++++ Restrictions +++++")
				ul = restr.find_next_sibling('ul')
				for k, li in enumerate(ul.find_all('li')):
					print("* --> " + li.text)
					d_restr["restr " + str(k)] = li.text

			cti = soup.find('h2', text='Contact Info')
			if cti:
				print("Contact informations:")
				ul = cti.find_next_sibling('ul')
				for k, li in enumerate(ul.find_all('li')):
					print("* " + li.text)
					d_cti["Contact "+str(k)] = li.text

			job_desc = soup.find('h2', text='Job Description')
			if job_desc:
				print("Job description:")
				for k, p in enumerate(job_desc.find_next_siblings('p')):
					print("- "+p.text)
					d_job["Job descr "+str(k)] = p.text
	return d, d_req, d_restr, d_cti, d_job


if __name__ == "__main__":

	url_2_scrape = "https://www.python.org/jobs/location/"
	base_url = "https://www.python.org"

	# check whether the robots.txt allows the scraping of the url_2_scrape
	robot_parser = robotparser.RobotFileParser()
	robot_parser.set_url(base_url+"/robots.txt")
	robot_parser.read()
	if robot_parser.can_fetch('*', url_2_scrape+"*"):
		print("You can fetch : " + url_2_scrape)
		# or maybe "montreal-quebec-canada"
		print("----")
		job_urls1 = web_scrape("telecommute")

		# or maybe "toronto-ontario-canada"
		print("----")
		job_urls2 = web_scrape("toronto-ontario-canada")
		d, d_req, d_restr, d_cti, d_job = extract_job_content(job_urls2)

		# save to excel file
		workbook = xlsxwriter.Workbook('jobs--toronto-ontario-canada.xlsx')
		worksheet = workbook.add_worksheet("toronto-ontario-canada")

		# personnalisation
		cell_format = workbook.add_format()
		cell_format.set_bold()
		cell_format.set_font_color('red')

		# Title
		worksheet.write(0, 0, "Title", cell_format)
		worksheet.write(0, 1, d["title"])

		# requirements
		row = 1
		for key, value in d_req.items():
			worksheet.write(row, 0, key, cell_format)
			worksheet.write(row, 1, value)
			row += 1

		# restrictions
		for key, value in d_restr.items():
			worksheet.write(row, 0, key, cell_format)
			worksheet.write(row, 1, value)
			row += 1

		# Contact informations
		for key, value in d_cti.items():
			worksheet.write(row, 0, key, cell_format)
			worksheet.write(row, 1, value)
			row += 1

		# job description
		for key, value in d_restr.items():
			worksheet.write(row, 0, key, cell_format)
			worksheet.write(row, 1, value)
			row += 1

		workbook.close()

	else:
		print("You cannot fetch : " + url_2_scrape + "*")





