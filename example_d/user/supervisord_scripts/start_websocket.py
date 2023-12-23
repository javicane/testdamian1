import sys
import os
import logging
import subprocess

sys.path.append('/home/damian/.local/lib/python3.8/site-packages/')


target_dir = "/home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/supervisord_scripts"
target_script_file_name = "matar_ws_colgados.py"
subprocess.run(['python3', target_script_file_name], cwd=target_dir)

target_dir = "/home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user"
target_script_file_name = "websocket_module.py"
subprocess.run(['python3', target_script_file_name], cwd=target_dir)