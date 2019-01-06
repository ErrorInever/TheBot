import os
import csv
import sources.long_poll_server as lp

def main():
	# check data user
	user_data = is_file_init()
	server = lp.Long_Poll_Server(user_data)

	# start auth
	while True:
		if server.auth():
			access_token = input('enter your access token')
			break
		else:
			print('auth False\n')
			continue

	server.get_data_session(access_token)
	
	server.start_long_poll_server()


def is_file_init():
	
	if os.path.exists('files/initialization.csv'):
		user_data = read_csv_file()
	else:
		create_csv_file()
		user_data = read_csv_file()

	return user_data

	
def create_csv_file():
	'''
	creating csv file with user data

	'''
	with open('files/initialization.csv', 'w') as init_file:
		init_writer = csv.writer(init_file, delimiter=',',
								quotechar='|', quoting=csv.QUOTE_MINIMAL)
		
		app_id = input('enter your application id ')
		permission = input('enter permission ')
		api_version = input('enter api version')

		init_writer.writerow(['Application id', app_id])
		init_writer.writerow(['Permission', permission])
		init_writer.writerow(['Api version', api_version])

def read_csv_file():
	'''
	read csv file with user data

	return dictionary:
	user data = {'Aplication id': 'user number id',
				'Permission': 'user number permission',
				'Api version': 'current api version(5.92)'
				}
	'''
	with open('files/initialization.csv', 'r', 
			encoding='utf-8') as init_file:

				user_data = dict(csv.reader(init_file))
				app_id = user_data['Application id']
				permission = user_data['Permission']
				api_version = user_data['Api version']

	return user_data

if __name__ == '__main__':
	main()