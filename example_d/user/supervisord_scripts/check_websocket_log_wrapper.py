import sys
import os
import logging

sys.path.append('/home/damian/.local/lib/python3.8/site-packages/')

from binance_d.example_d.user.supervisord_scripts.check_websocket_log_module import check_websocket_log

print("hola")
print("hola1")
print("hola2")
check_websocket_log("NO") 