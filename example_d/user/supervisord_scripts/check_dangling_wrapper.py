import sys
import os
import logging

sys.path.append('/home/damian/.local/lib/python3.8/site-packages/')

from binance_d.example_d.user.check_dangling_scripts.dangling_module import check_dangling_before_starting_websocket 

check_dangling_before_starting_websocket("NO") 
