from sources.vk import Vk


class Bot(object):
    """
    main bot class
    """

    def __init__(self):
        self._EVENTS = frozenset((4, 5, 8, 9, 80))
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
                # new message
                user_message = self.vk.parse_message(event)

                if user_message:
                    print('parsing =', user_message)
                    self.vk.send_message(user_id=user_message['user_id'], access_token=access_token,
                                         message=user_message['user_message'])
                else:
                    return

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
