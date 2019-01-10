import requests
from sources.Bot import Bot


class LongPollServer(object):

    def __init__(self, user_data):
        self.user_data = user_data
        self.session = requests.Session()
        self.response = None

        self.key = None
        self.server = None
        self.ts = None

        self.event = None

        self.bot = Bot()

        self.access_token = None

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

    def get_data_session(self, access_token):
        self.access_token = access_token
        url_template = 'https://api.vk.com/method/messages.getLongPollServer'

        values = {'access_token': access_token, 'lp_version': '3',
                  'v': self.user_data['Api version']}

        data = requests.get(url_template, params=values).json()['response']

        self.key = data['key']
        self.server = data['server']
        self.ts = data['ts']

    def start_long_poll_server(self):

        url_template = 'https://{server}?act=a_check&key={key}&ts={ts}&wait=20&mode=74&version=3'

        while True:
            self.response = requests.get(url_template.format(
                server=self.server, key=self.key, ts=self.ts)).json()

            try:
                self.event = self.response['updates']
            except KeyError as e:
                print('KEY NOT VALID {0}'.format(e))
                self.get_data_session(self.access_token)
                continue

            if self.event:
                for element in self.event:
                    self.bot.check_event(element, self.access_token)

            self.ts = self.response['ts']
