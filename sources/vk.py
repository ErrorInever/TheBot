import requests
import uuid


class Vk(object):

    def __init__(self):
        self._PLATFORMS = frozenset((1, 2, 3, 4, 5, 6, 7))
        self._CONVERRSTATION_MASK = 2000000000

        self._URL_TEMPLATE = 'https://api.vk.com/method/'
        self._API_VERSION = '5.92'

    def parse_message(self, event_message):
        """
        creating dictionary of data of message

        args -> list
        structure of list: [4, ts, message flag, user_id, unixtime, message text, {'attachments title': ' ... '}]

        return -> dictionary:
        {
        'user_id': id_user,
        'time': 'time',
        'user_message': 'text message',
        'attachments': {'photo': [id, ...], 'video': [id, ...], 'audio': [id, ...], 'doc': [id, ...]}
        }
        """
        if event_message[3] - self._CONVERRSTATION_MASK < 0:

            user_message = {'user_id': event_message[3], 'time': '2222', 'user_message': event_message[5],
                            'attachments': {
                                'photo': [],
                                'video': [],
                                'audio': [],
                                'doc': []
                                }}
                # attachments of message
            media = event_message[7:]
            media = media[0]
            index_attach = 1
            media_type = 'attach1_type'

            while media_type in media.keys():
                media_type = media['attach{index}_type'.format(index=index_attach)]

                if media_type == 'photo':
                    user_message['attachments']['photo'].append(media['attach{index}'.format(index=index_attach)])

                elif media_type == 'video':
                    user_message['attachments']['video'].append(media['attach{index}'.format(index=index_attach)])

                elif media_type == 'audio':
                    user_message['attachments']['audio'].append(media['attach{index}'.format(index=index_attach)])

                elif media_type == 'doc':
                    user_message['attachments']['doc'].append(media['attach{index}'.format(index=index_attach)])

                index_attach += 1
                media_type = 'attach{index}_type'.format(index=index_attach)
            return user_message

    def friend_online(self, event):
        """
        check user platform who became online

        args -> list
        structure of list: [8, -(id), platform, unixtime]

        platforms:
        1 - mobile
        2 - iphone
        3 - ipad
        4 - android
        5 - wphone
        6 - windows
        7 - web

        return -> dictionary
        """

        data = {'user_id': event[1] * (-1), 'platform': None, 'time': None}

        platform = event[2]

        if platform in self._PLATFORMS:

            if platform == 1:
                data['platform'] = 'mobile'
            elif platform == 2:
                data['platform'] = 'iphone'
            elif platform == 3:
                data['platform'] = 'ipad'
            elif platform == 4:
                data['platform'] = 'android'
            elif platform == 5:
                data['platform'] = 'wphone'
            elif platform == 6:
                data['platform'] = 'windows'
            elif platform == 7:
                data['platform'] = 'website'

        return data

    @staticmethod
    def friend_offline(event):
        """
        check user log out method
        args -> list
        structure: [9, -(id), 0 or 1 (1 - timeout, 0 - user log out, unix_time]
        return -> dictionary
        """

        data = {'user_id': event[1] * (-1), 'method': None, 'time': None}

        value = event[2]

        if value:
            data['method'] = 'timeout'
        else:
            data['method'] = 'log out'

        return data


    def send_message(self, *, user_id, access_token, message=None, attachment=None, sticker_id=None):
        """
        sending message to user
        """
        data = {'user_id': user_id, 'random_id': uuid.uuid4().int >> 32, 'access_token': access_token, 'v': self._API_VERSION}

        if message is not None:
            data['message'] = message
        if attachment is not None:
            data['attachment'] = attachment
        if sticker_id is not None:
            data['sticker_id'] = sticker_id

        response = requests.get(self._URL_TEMPLATE + 'messages.send', params=data).json()
        return response


    def who_is_it(self, *, user_id, access_token):
        """
        get info of user
        """
        print('user_id=', user_id)
        response = requests.get(self._URL_TEMPLATE + 'users.get', 
            params={'user_ids': user_id, 'fields': ['is_friend'],'access_token': access_token, 'v': self._API_VERSION}).json()['response'][0]
        data = {'user_id': response['id'],
                'first_name': response['first_name'],
                'last_name': response['last_name'],
                'is_closed': response['is_closed'],
        }
        if response['is_friend'] == 1: 
            data['is_friend'] = 'True'
        else:
            data['is_friend'] = 'False'



        text = 'Target - id[{id}]\nName - {f_name} {l_name}\nIs friend? - {friend}\nPage is closed? - {close}'.format(id=data['user_id'],
        	f_name=data['first_name'], l_name=data['last_name'], friend=data['is_friend'], close=data['is_closed'])

        return text


