import logging
import xlsxwriter
import os
import datetime as dt

from Decorators import log_decorator


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
	worksheet.write(row, 0, "Titre", cell_format)
	worksheet.write(row, 1, job_offer.job_title)
	row += 1

	worksheet.write(row, 0, "Url", cell_format)
	worksheet.write(row, 1, job_offer.job_url)
	row += 1

	d_scraped = job_offer.job_scraped
	for key, value in d_scraped.items():
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
