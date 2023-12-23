import sys
import os
import logging

#ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#sys.path.insert(0, ROOT_DIR + '/../..')
#sys.path.append('/home/damian/.local/lib/python3.8/site-packages/binance_d/')
sys.path.append('/home/damian/.local/lib/python3.8/site-packages/')

#from binance_d.requestclient import RequestClient
#from binance_d.subscriptionclient import SubscriptionClient
#from binance_d.constant.test import *
#from binance_d.model import *
#from binance_d.exception.binanceapiexception import BinanceApiException

#from binance_d.base.printobject import *
#from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, check_existence_radar_list_in_disc, list_pivots_in_radar_list_in_disk, funcname
#from binance_d.example_d.user.process_event_scripts.process_module import process_event
from binance_d.example_d.user.dangling_module_supercheck import check_dangling_before_starting_websocket 

check_dangling_before_starting_websocket("NO") 