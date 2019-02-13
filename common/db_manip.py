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
def add_job_link(job_link, state):
	""" add a job_link to the database with its state """
	if not check_if_exist(job_link, state):
		conn = sqlite3.connect("links.db")
		cur = conn.cursor()
		cur.execute(""" INSERT OR REPLACE INTO links VALUES (?,?) """, (job_link, state))
		conn.commit()
		conn.close()


@log_decorator
def check_if_exist(job_link, state):
	""" return boolean if joblink/state exists in links table """

	conn = sqlite3.connect("links.db")
	cur = conn.cursor()
	cur.execute(""" SELECT * FROM links WHERE joblink=? and state=?""", (job_link, state))
	fetched_value = cur.fetchone()
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
	return len(fetched_all)
