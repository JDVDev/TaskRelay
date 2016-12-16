import requests

class RequestsWrapper():
    """Wrapper used for unit testing"""
	@staticmethod
	def get(url):
		return requests.get(url, verify = False)
