from unittest import TestCase, main
import os

from openpyxl import Workbook
from openpyxl.styles import Font

from common.Xlsx_manip import create_xlsx_dir, write_job_offer_2_worksheet, save_to_xlsx
from job_offer import JobOffer


class TestXlsxManip(TestCase):

	def setUp(self):
		d_scraped = dict()
		d_scraped["R1"] = "text 1"
		d_scraped["R2"] = "text 2"
		self.job_offer = JobOffer("Titre", d_scraped, "https://www.google.com")

	def test_create_xlsx_dir(self):
		create_xlsx_dir("dir_for_xlsx")
		self.assertTrue(os.path.exists("./dir_for_xlsx"))

	def test_write_job_offer_2_worksheet(self):
		create_xlsx_dir("dir_for_xlsx")
		workbook = Workbook()
		worksheet = workbook.create_sheet(f"Sheet_1")
		write_job_offer_2_worksheet(self.job_offer, worksheet, Font(size=15))
		workbook.save("dir_for_xlsx/xlsx_file.xlsx")
		self.assertTrue(os.path.exists("./dir_for_xlsx/xlsx_file.xlsx"))

	def tearDown(self):
		if os.path.exists("./dir_for_xlsx"):
			os.remove("./dir_for_xlsx/xlsx_file.xlsx")
			os.removedirs("./dir_for_xlsx")


if __name__ == '__main__':
	main()
