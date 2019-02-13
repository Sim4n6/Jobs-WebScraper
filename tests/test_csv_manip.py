import os
from unittest import TestCase, main

from sources.common.csv_manip import to_csv, from_csv, is_csv_exist


class TestCsvManip(TestCase):

	def setUp(self):
		self.urls = ["www.google.fr", "https://www.python.org", "aaa"]

	def test_to_csv_empty(self):
		empty_lst = []
		to_csv(empty_lst, "file_empty.csv")
		self.assertFalse(is_csv_exist("file_empty.csv"))

	def test_to_csv(self):
		to_csv(self.urls, "file.csv")

		lines = []
		with open("file.csv", "r") as csvfile:
			for line in csvfile.readlines():
				lines.append(line)

		self.assertEqual(lines[0].strip(), "www.google.fr")
		self.assertEqual(lines[1].strip(), "https://www.python.org")
		self.assertEqual(lines[2].strip(), "aaa")

	def test_from_csv(self):
		to_csv(self.urls, "file.csv")
		urls_from_csv = from_csv("file.csv")
		self.assertEqual(sorted(self.urls), sorted(urls_from_csv))

	def test_is_csv_exist(self):
		with open("file.csv", "w"):
			self.assertTrue(is_csv_exist("file.csv"))

	def tearDown(self):
		if os.path.exists("file.csv"):
			os.remove("file.csv")

		if os.path.exists("file_empty.csv"):
			os.remove("file_empty.csv")


if __name__ == '__main__':
	main()
