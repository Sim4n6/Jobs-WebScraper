import datetime as dt
import logging
import os

from openpyxl import Workbook
from openpyxl.styles import Font, colors

from sources.common.Decorators import log_decorator


@log_decorator
def save_to_xlsx(xlsx_filename, list_job_offers):
	""" Save the dictionaries to xlsx file using Xlsx-Writer """

	logging.info("Xlsx writting started at " + str(dt.datetime.now()) + " to file " + "saved_jobs/" + xlsx_filename)

	# Create directory "saved_jobs" locally
	create_xlsx_dir("saved_jobs")

	# Save to excel file
	workbook = Workbook()

	# personnalisation
	bold_font = Font(color=colors.RED, bold=True)

	for i, job_offer in enumerate(list_job_offers):
		# create a sheet for each job offer
		worksheet = workbook.create_sheet(f"Sheet Offer {str(i)}")

		# write job_offer to worksheet
		write_job_offer_2_worksheet(job_offer, worksheet, bold_font)

	# close workbook
	workbook.save("saved_jobs" + "/" + xlsx_filename)


@log_decorator
def write_job_offer_2_worksheet(job_offer, worksheet, cell_format):
	""" Write job offer object to worksheet """

	worksheet['A1'].font = cell_format
	worksheet.append(["Titre", job_offer.job_title])
	worksheet['A2'].font = cell_format
	worksheet.append(["Url", job_offer.job_url])

	d_scraped = job_offer.job_scraped
	for key, value in d_scraped.items():
		worksheet.append([key, value])


@log_decorator
def create_xlsx_dir(xlsx_dir):
	""" Create a xlsx directory """
	try:
		os.mkdir(xlsx_dir)
		logging.info("Directory " + xlsx_dir + " created.")
	except FileExistsError:
		logging.warning("Directory " + xlsx_dir + " already exists.")
