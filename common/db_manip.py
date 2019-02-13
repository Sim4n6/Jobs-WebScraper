import sqlite3

from common.Decorators import log_decorator


@log_decorator
def create_db():
	""" create if not exists a database named 'links.db' that receive job_link and its state as integer : 1 scraped """

	conn = sqlite3.connect("links.db")
	cur = conn.cursor()
	cur.execute(""" CREATE TABLE IF NOT EXISTS links (joblink TEXT, state INT)""")
	conn.commit()
	conn.close()


@log_decorator
def delete_db():
	""" delete table links """

	conn = sqlite3.connect("links.db")
	cur = conn.cursor()
	cur.execute(""" DROP TABLE IF EXISTS links """)
	conn.commit()
	conn.close()


@log_decorator
def add_job_link(job_link):
	""" add a job_link to the database with its state """
	if not check_if_exist(job_link):
		conn = sqlite3.connect("links.db")
		cur = conn.cursor()
		cur.execute(""" INSERT INTO links VALUES (?,?) """, (job_link, -1))
		conn.commit()
		conn.close()


@log_decorator
def set_state(job_link, state):
	"""" set a state to job_link if joblink exists in database """

	if check_if_exist(job_link):
		conn = sqlite3.connect("links.db")
		cur = conn.cursor()
		cur.execute(""" UPDATE links SET state=? WHERE joblink=?""", (state, job_link))
		conn.commit()
		conn.close()


def get_state(job_link):
	if check_if_exist(job_link):
		conn = sqlite3.connect("links.db")
		cur = conn.cursor()
		cur.execute(""" SELECT * FROM links WHERE joblink=?""", (job_link, ))
		fetched_one = cur.fetchone()
		conn.close()
		return fetched_one[1]
	else:
		return -1



@log_decorator
def check_if_exist(job_link):
	""" return boolean if joblink exists in links table """

	conn = sqlite3.connect("links.db")
	cur = conn.cursor()
	cur.execute(""" SELECT * FROM links WHERE joblink=? """, (job_link, ))
	fetched_value = cur.fetchone()
	conn.close()
	if fetched_value is None:
		return False
	else:
		return True


@log_decorator
def is_scrarped_job_link(job_link):
	""" Check whether a joblink is in the database and return its state"""
	conn = sqlite3.connect("links.db")
	cur = conn.cursor()
	cur.execute(""" SELECT * FROM links WHERE joblink=? """, (job_link,))
	one_fetched = cur.fetchone()
	conn.close()
	if one_fetched is None:
		return 0
	else:
		return one_fetched[1]


@log_decorator
def count_joblinks():
	""" return number of joblinks in links table """
	conn = sqlite3.connect("links.db")
	cur = conn.cursor()
	cur.execute(""" SELECT * FROM links """)
	fetched_all = cur.fetchall()
	conn.close()
	return len(fetched_all)


@log_decorator
def extract_all_joblinks(state):
	""" extract all joblinks with state arg """
	conn = sqlite3.connect("links.db")
	cur = conn.cursor()
	cur.execute(""" SELECT * FROM links WHERE state=?""", (state, ))
	fetched_all = cur.fetchall()
	conn.close()
	urls = []
	for fetched in fetched_all:
		urls.append(fetched[0])

	return urls
