class JobOffer:
	""" Job Offer structure for storing text scraped """

	def __init__(self, job_title, job_descr, restrictions, requirements, company_desc, contact_info, job_url):
		self.job_title = job_title
		self.job_descr = job_descr
		self.restrictions = restrictions
		self.requirements = requirements
		self.company_desc = company_desc
		self.contact_info = contact_info
		self.job_url = job_url

	def __str__(self):
		print("------> ", self.job_title)


