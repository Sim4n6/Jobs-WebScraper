import os
from unittest import TestCase

from common.csv_manip import to_csv, from_csv


class TestCsvManip(TestCase):

	def test_saved_jobs_dir_exists(self):
		self.assertTrue(os.path.exists("../saved_jobs/"))

	def test_to_csv(self):
		urls = ["www.google.fr", "https://www.python.org", "aaa"]
		to_csv(urls, "file.csv")

		lines = []
		with open("../saved_jobs/file.csv", "r") as csvfile:
			for line in csvfile.readlines():
				lines.append(line)

		self.assertEqual(lines[0].strip(), "www.google.fr")
		self.assertEqual(lines[1].strip(), "https://www.python.org")
		self.assertEqual(lines[2].strip(), "aaa")

	def test_from_csv(self):
		urls = ("www.google.fr", "https://www.python.org", "aaa")
		urls_from_csv = from_csv("file.csv")
		self.assertEqual(sorted(urls), sorted(urls_from_csv))
