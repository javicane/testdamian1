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
from binance_d.example_d.user.helpers_scripts.helpers_module import funcname
from binance_d.example_d.user.process_event_scripts.process_module import process_event

from binance_d.impl.utils.timeservice import get_current_timestamp
from binance_d.example_d.user.helpers_scripts.sql import exec_sql


def update_group_id_frontend(order_id, group_id):
    print("in update_group_id_frontend: ", order_id, group_id)
    result = "ERROR"
    try:

        sql = "update radar_list set group_id='" + str(group_id) + "' "
        sql += " where " 
        sql += "order_id='" + str(order_id) + "';"
        print("sql: ", sql)
        rows_updated = exec_sql(sql = sql, sql_command = "update", error_message = "error in " + str(funcname()))
        result = "OK"
    except:
        result = "ERROR, timestamp: " + str(get_current_timestamp()) + ", "
        result += str(sys.exc_info())
        d = {'result': result, 'order_id': "-"}
        print("except: ", d)
        return d
    
    if result == "OK":
        if rows_updated != 1:
            result = "ERROR_UPDATE_RADAR_LIST, rows_updated: " + str(rows_updated) + ", "  + str(get_current_timestamp())
            d = {'result': result, 'order_id': order_id}
        else:
            result = result + ", timestamp: "  + str(get_current_timestamp())
            d = {'result': result, 'order_id': order_id}
        print("return in update_group_id_frontend", d)
        return d