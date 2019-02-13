import os
from unittest import TestCase, main

from common.db_manip import create_db, add_job_link, is_scrarped_job_link


class TestDBManip(TestCase):

	def setUp(self):
		self.joblink = "www.python.org"

	def test_create_db(self):
		create_db()
		self.assertTrue(os.path.exists("links.db"))

	def test_add_job_link(self):
		add_job_link(self.joblink, 1)

	def test_is_scraped(self):
		self.assertTrue(is_scrarped_job_link(self.joblink) == 1)


if __name__ == '__main__':
	main()
