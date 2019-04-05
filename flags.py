import os
import subprocess
import argparse


def run(host):
    directory = os.getcwd()
    folders = os.listdir(directory)
    folders.sort()

    for folder in folders:
        if not folder.startswith('.') and folder != 'flags.py' and not folder.startswith('06'):
            os.chdir(os.path.join(os.getcwd(), folder, 'resources'))
            subprocess.call('python3 script.py {host}'.format(host=host), shell=True)
            os.chdir(directory)


if __name__ == '__main__':
    try:
        ap = argparse.ArgumentParser()
        ap.add_argument("-H", "--host", required=True, help="Your have to set hostname. For example: 192.168.1.79")

        run(**vars(ap.parse_args()))
    except Exception as e:
        print(e.args)
