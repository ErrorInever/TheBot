import requests




class Long_Poll_Server(object):

	def __init__(self, user_data):
		self.user_data = user_data
		self.session = requests.Session()
		self.response = None

	def auth(self):
		api_auth_url = 'https://oauth.vk.com/authorize'
		reddirect_url = 'https://oauth.vk.com/blank.html'
		display = 'page'
		response_type = 'token'
		temp_url = '{0}?client_id={1}&display={2}&redirect_uri={3}&scope={4}&response_type={5}&v={6}'

		auth_url = temp_url.format(api_auth_url, self.user_data['Application id'], 
									display, reddirect_url, self.user_data['Permission'], 
										response_type, self.user_data['Api version'])

		self.response = self.session.get(auth_url)
		status_code = self.response.status_code

		if status_code == requests.codes.ok:
			print(self.response.url)
			return True
		else:
			return False
