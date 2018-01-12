import requests
class FixerAPI(object):
	"""docstring for network"""
	baseApi = 'https://api.fixer.io/'
	# https://api.fixer.io/latest?base=EUR&symbols=EGP
	def getExchangeRate(self,base,currency,date=''):
		# print("network loading...")
		# initialization url query params
		payload = {'base':base,'symbols':currency}
		url = self.baseApi
		if date:
			url+=date
		else:
			url+='latest'

		try:
			response = requests.get(url,params=payload)
		except requests.exceptions.RequestException as e:
			print("Error")
			print(e)
			exit()

		if response.ok:
			return response.json()
		else:
			res = response.json()
			if res['error']:
				print(res['error'])
			exit()
