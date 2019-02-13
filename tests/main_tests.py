from unittest import TextTestRunner, TestSuite

from tests.test_csv_manip import TestCsvManip
from tests.test_xlsx_manip import TestXlsxManip
from tests.test_db_manip import TestDBManip

if __name__ == '__main__':

	# define a test Suite
	suite = TestSuite()

	# CSV manip module
	suite.addTest(TestCsvManip("test_to_csv"))
	suite.addTest(TestCsvManip("test_from_csv"))
	suite.addTest(TestCsvManip("test_is_csv_exist"))
	suite.addTest(TestCsvManip("test_to_csv_empty"))

	# XLSX manip module
	suite.addTest(TestXlsxManip("test_write_job_offer_2_worksheet"))
	suite.addTest(TestXlsxManip("test_create_xlsx_dir"))

	# DB manip module
	suite.addTest(TestDBManip("test_create_db"))
	suite.addTest(TestDBManip("test_add_joblink"))
	suite.addTest(TestDBManip("test_count_joblinks"))
	suite.addTest(TestDBManip("test_is_scraped"))
	suite.addTest(TestDBManip("test_is_duplicate"))
	suite.addTest(TestDBManip("test_check_if_exist"))
	suite.addTest(TestDBManip("test_extract_all_joblinks"))
	suite.addTest(TestDBManip("test_set_get_state"))

	# instantiate the test runner
	runner = TextTestRunner()
	runner.run(suite)
