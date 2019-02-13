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
def add_job_link(job_link, state):
	""" add a job_link to the database with its state """
	conn = sqlite3.connect("links.db")
	cur = conn.cursor()
	cur.execute(""" INSERT INTO links VALUES (?,?) """, (job_link, state))
	conn.commit()
	conn.close()


@log_decorator
def is_scrarped_job_link(job_link):
	""" Check whether a joblink is in the database and return its state"""
	conn = sqlite3.connect("links.db")
	cur = conn.cursor()
	cur.execute(""" SELECT * FROM links WHERE joblink=? """, (job_link,))
	return cur.fetchone()[1]
