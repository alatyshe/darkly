import os
import subprocess
import sys


def run(host_name):
    directory = os.getcwd()
    folders = os.listdir(directory)
    folders.sort()

    for folder in folders:
        if not folder.startswith('.') and folder != 'flags.py' and not folder.startswith('06'):
            os.chdir(os.path.join(os.getcwd(), folder, 'resources'))
            subprocess.call('python3 script.py {host}'.format(host=host_name), shell=True)
            os.chdir(directory)


if __name__ == '__main__':
    try:
        host_name = sys.argv[1]
        run(host_name=host_name)
    except Exception as e:
        print(e.args)
