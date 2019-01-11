from sources.vk import Vk


class Bot(object):
    """
    main bot class
    """

    def __init__(self):
        self._EVENTS = frozenset((4, 5, 8, 9, 80))
        self._MESSAGE_MASK = frozenset((1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 65536, 131072))
        self.vk = Vk()

    def check_event(self, event, access_token):
        """
        checking event of long poll server and to do something

        EVENTS:
        4 - new message
        5 - edit message
        8 - friend has being online
        9 - friend has being offline
        80 - counter has being equal $count
        """

        code_event = event[0]

        if code_event in self._EVENTS:

            if code_event == 4:
                flags_messages = event[2]
                summands = [number for number in self._MESSAGE_MASK if number & flags_messages]
                if 2 not in summands:
                    user_message = self.vk.parse_message(event)
                    response = self.vk.who_is_it(user_id=user_message['user_id'], access_token=access_token)
                    self.vk.send_message(user_id=user_message['user_id'], access_token=access_token, message=response)


            elif code_event == 5:
                pass

            elif code_event == 8:
                # friend online
                response = self.vk.friend_online(event)
                print('friend_online', response)
            elif code_event == 9:
                # friend offline
                response = self.vk.friend_offline(event)
                print('friend_offline', response)
            elif code_event == 80:
                pass
