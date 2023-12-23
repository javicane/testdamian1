import sys
import signal
sys.path.append('/home/damian/.local/lib/python3.8/site-packages/')
import os
import subprocess

#os.system("python3 /home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/React_Django/project1/manage.py runserver")
def run_server():
    try:
        subprocess.run(['python3', '/home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/React_Django/project1/manage.py', 'runserver'])
    except KeyboardInterrupt:
        print("damian Server has been stopped.")

if __name__ == "__main__":
    run_server()
