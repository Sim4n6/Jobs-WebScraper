import os
from unittest import TestCase, main

from sources.common.db_manip import create_table_db, add_job_link, is_scrarped_job_link, count_joblinks, delete_table_db,\
	check_if_exist, extract_all_joblinks, set_state, get_state


class TestDBManip(TestCase):

	def setUp(self):
		self.joblink1 = "www.python.org"
		self.joblink2 = "www.python.org/job/"
		self.joblink3 = "www.python.org/job/1000"

	def test_create_db(self):
		create_table_db()
		self.assertTrue(os.path.exists("links.db"))
		delete_table_db()

	def test_add_joblink(self):
		create_table_db()
		add_job_link(self.joblink1)
		self.assertEqual(count_joblinks(), 1)
		delete_table_db()

	def test_count_joblinks(self):
		create_table_db()
		add_job_link(self.joblink1)
		add_job_link(self.joblink2)
		self.assertEqual(count_joblinks(), 2)
		delete_table_db

	def test_is_scraped(self):
		create_table_db()
		add_job_link(self.joblink1)
		set_state(self.joblink1, 1)
		add_job_link(self.joblink2)
		set_state(self.joblink2, 1)
		self.assertTrue(is_scrarped_job_link(self.joblink1) == 1)
		self.assertTrue(is_scrarped_job_link(self.joblink2) == 1)
		self.assertTrue(is_scrarped_job_link(self.joblink3) == 0)
		delete_table_db()

	def test_is_duplicate(self):
		create_table_db()
		add_job_link(self.joblink1)
		set_state(self.joblink1, 1)
		add_job_link(self.joblink1)
		set_state(self.joblink1, 1)
		self.assertEqual(count_joblinks(), 1)
		delete_table_db()

	def test_check_if_exist(self):
		create_table_db()
		self.assertFalse(check_if_exist(self.joblink1))
		add_job_link(self.joblink1)
		self.assertTrue(check_if_exist(self.joblink1))
		delete_table_db()

	def test_extract_all_joblinks(self):
		create_table_db()
		add_job_link(self.joblink1)
		add_job_link(self.joblink2)
		urls = extract_all_joblinks(-1)
		self.assertEqual(len(urls), 2)
		self.assertEqual(urls[0], self.joblink1)
		self.assertEqual(urls[1], self.joblink2)
		delete_table_db()
		create_table_db()
		add_job_link(self.joblink1)
		set_state(self.joblink1, 1)
		add_job_link(self.joblink2)
		set_state(self.joblink2, 0)
		urls = extract_all_joblinks(0)
		self.assertEqual(len(urls), 1)
		self.assertEqual(urls[0], self.joblink2)
		delete_table_db()

	def test_set_get_state(self):
		create_table_db()
		add_job_link(self.joblink1)
		set_state(self.joblink1, 100)
		self.assertEqual(get_state(self.joblink1), 100)
		delete_table_db()


if __name__ == '__main__':
	main()
