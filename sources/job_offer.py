class JobOffer:
	""" Job Offer structure for storing text scraped """

	def __init__(self, job_title, job_scraped, job_url):
		self.job_title = job_title
		self.job_scraped = job_scraped
		self.job_url = job_url

	def __str__(self):
		print("------> ", self.job_title)
