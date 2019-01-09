import requests



class Bot(object):
	'''
	main bot class
	'''
	def __init__(self):
		self._MESSAGE_MASK = frozenset((1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 65536, 131072))
		self._EVENTS = frozenset((4, 5, 8, 9, 61, 70, 80))
		self._CONVERRSTATION_MASK = 2000000000


	def check_event(self,event_message):
		'''
		checking event of long poll server and to do something

		EVENTS:
		4 - new message
		5 - edit message
		8 - friend has being online
		9 - friend has being offline
		61 - user is typing
		70 - user call 
		80 - counter has being equal $count 
		'''

		code_event = event_message[0]

		if code_event in self._EVENTS:

			if code_event == 4:
				self.parse_message(event_message)

			elif code_event == 5:
				pass

			elif code_event == 8:
				pass

			elif code_event == 9:
				pass

			elif code_event == 61:
				pass

			elif code_event == 70:
				pass

			else:
				pass
		

	def parse_message(self, event_message):
		'''
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
		'''
		flags_messages = event_message[2]
		#create summands of message mask
		summands = [number for number in self._MESSAGE_MASK if number & flags_messages]
		if 2 not in summands:
			if event_message[3] - self._CONVERRSTATION_MASK < 0:

				user_message = {
					'user_id': None,
					'time': None,
					'user_message': None,
					'attachments': {
						'photo': [],
						'video': [],
						'audio': [],
						'doc' : []
					}
				}
				user_message['user_id'] = event_message[3]
				user_message['user_message'] = event_message[5]
				#attachments of message
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
				# need to implement: stikers, geo map data
				return user_message