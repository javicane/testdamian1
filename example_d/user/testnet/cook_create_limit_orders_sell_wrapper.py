import sys
import os
import logging

#ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#sys.path.insert(0, ROOT_DIR + '/../..')
#sys.path.append('/home/damian/.local/lib/python3.8/site-packages/binance_d/')
sys.path.append('/home/damian/.local/lib/python3.8/site-packages/')

from binance_d import RequestClient
from binance_d import SubscriptionClient
from binance_d.constant.test import *
from binance_d.model import *
from binance_d.exception.binanceapiexception import BinanceApiException

from binance_d.base.printobject import *
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, check_existence_radar_list_in_disc, list_pivots_in_radar_list_in_disk, funcname
from binance_d.example_d.user.process_event_scripts.process_module import process_event
from binance_d.example_d.user.manual_scripts.cook_create_limit_orders_sell_module import limit_no_oco_sell_long

limit_no_oco_sell_long(0.6262,3)