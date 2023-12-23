import sys
import os
import logging

#ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#sys.path.insert(0, ROOT_DIR + '/../..')
#sys.path.append('/home/damian/.local/lib/python3.8/site-packages/binance_d/')
sys.path.append('/home/damian/.local/lib/python3.8/site-packages/')

#from binance_d import RequestClient
#from binance_d import SubscriptionClient
from binance_d.constant.test import *
from binance_d.model import *
from binance_d.exception.binanceapiexception import BinanceApiException

from binance_d.base.printobject import *
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, check_existence_radar_list_in_disc, list_pivots_in_radar_list_in_disk, funcname
from binance_d.example_d.user.process_event_scripts.process_module import process_event

from binance_d.example_d.user.common_scripts.create_orders_module import silent_limit_no_oco_sell_long
from binance_d.impl.utils.timeservice import get_current_timestamp
from binance_d.example_d.user.helpers_scripts.sql import exec_sql


def resize_pivot_frontend(order_id, resize):
    print("in resize_pivot_frontend: ", order_id, resize)
    result = "ERROR"
    try:
        #raise Exception("zaraza")
        sql = "update radar_list set resize = " + str(resize) + " where " 
        sql += "order_id='" + str(order_id) + "';"
        print("sql: ", sql)
        rows_updated = exec_sql(sql = sql, sql_command = "update", error_message = "error in " + str(funcname()))
        result = "OK"
    except:
        result = "ERROR, timestamp: " + str(get_current_timestamp()) + ", "
        result += str(sys.exc_info())
        d = {'result': result, 'order_id': "-", 'resize:': "-"}
        print("except: ", d)
        return d
    
    if result == "OK":
        if rows_updated != 1:
            result = "ERROR_UPDATE_RADAR_LIST, rows_updated: " + str(rows_updated) + ", "  + str(get_current_timestamp())
            d = {'result': result, 'order_id': order_id, 'resize': resize}
        else:
            result = result + ", timestamp: "  + str(get_current_timestamp())
            d = {'result': result, 'order_id': order_id, 'resize': resize}
        
        return d