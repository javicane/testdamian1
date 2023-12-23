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

#limit_no_oco_sell_long(0.46946,1)
#limit_no_oco_sell_long(0.8,8)
insert_new_row_in_radar_list = 'Y'
p_price = 0.8  
p_size = 1 

clientorderid_value = "goto_in_position" + str(get_current_timestamp())
output = silent_limit_no_oco_sell_long(p_price, p_size, p_clientorderid=clientorderid_value)
output_dict =  create_dict_from_output(output)
#output_dict:  {'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'goto_in_position1657246327455', 
# 'closePosition': 'False', 'cumBase': '0.0', 'executedQty': '0.0', 'orderId': '7009365869', 
# 'origQty': '6.0', 'origType': 'LIMIT', 'positionSide': 'LONG', 'price': '0.8', 'priceRate': 'None', 
# 'reduceOnly': 'True', 'side': 'SELL', 'status': 'NEW', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 
# 'timeInForce': 'GTC', 'type': 'LIMIT', 'updateTime': '1657246333602', 'workingType': 'CONTRACT_PRICE'}
order_id_to_close = output_dict['orderId']
order_id = "666" + str(order_id_to_close)
print("output_dict: ", output_dict)
sql = "insert into radar_list ( order_id, order_status, order_id_to_close, trigger_price_to_put_in_position,"
sql += "trigger_price_to_close, original_quantity, clientorderid, repeat, resize) values (" 
sql += order_id + ", "
sql += "'IN_POSITION', "
sql += order_id_to_close + ", "
sql += str(p_price) + ", "
sql += str(p_price) + ", "
sql += str(p_size) + ", " 
sql += "'" + clientorderid_value + "', "
sql += "'N', 6);"
print(sql)
#rows_inserted = exec_sql(sql = sql, sql_command = "insert", error_message = "error in " + str(funcname()))
#if rows_inserted != 1:
#    err = "ERROR in " + funcname() + ", aborting"
#    print(err)
#    raise 

#insert into radar_list values (6666666, 'IN_POSITION', 7007282518, 0.58, 0.59, 8, 'goto_in_position7007282518', 'N', 1);
#update radar_list set order_status = 'IN_POSITION', order_id_to_close =6888472335 , clientorderid='goto_in_position6667' where order_id =6887277800;