import json

class JSONWrapper():
    """Wrapper used for unit testing"""
	@staticmethod
	def dumps(message):
		return json.dumps(message)
