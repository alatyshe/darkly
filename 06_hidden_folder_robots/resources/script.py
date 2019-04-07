import requests
from bs4 import BeautifulSoup
import sys


def get_content(url):
	with open('content.txt', 'a+') as f:
		for link in BeautifulSoup(requests.get(url=url).text, 'html.parser').find_all('a'):
			print("FUCK ")
			if link.get('href') == 'README':
				content = requests.get(url=url+'/'+link.get('href')).content.decode('utf-8').strip()
				print("FUCK ", content)
				f.write(content+'\n')
			if not link.get('href').startswith('../'):
				get_content(url+'/'+link.get('href'))


def check_host_name(host_name):
	return requests.get('http://'+host_name+'/.hidden/').status_code == 200


if __name__ == "__main__":
	try:
		host_name = sys.argv[1]
		if check_host_name(host_name):
			get_content('http://'+host_name+'/.hidden/')
		else:
			raise Exception('Incorrect host name')
	except Exception as e:
		print(e.args)
