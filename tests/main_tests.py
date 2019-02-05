from unittest import TextTestRunner, TestSuite

from tests.test_csv_manip import TestCsvManip
from tests.test_xlsx_manip import TestXlsxManip

if __name__ == '__main__':

	# define a test Suite
	suite = TestSuite()
	suite.addTest(TestCsvManip("test_to_csv"))
	suite.addTest(TestCsvManip("test_from_csv"))
	suite.addTest(TestCsvManip("test_is_csv_exist"))
	suite.addTest(TestCsvManip("test_to_csv_empty"))

	suite.addTest(TestXlsxManip("test_write_job_offer_2_worksheet"))
	suite.addTest(TestXlsxManip("test_create_xlsx_dir"))

	# instantiate the test runner
	runner = TextTestRunner()
	runner.run(suite)
