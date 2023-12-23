import sys
import json
#from binance_d.requestclient import RequestClient
#from binance_d.subscriptionclient import SubscriptionClient
#from binance_d import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *


from socket import create_connection
from binance_d.example_d.user.common_scripts.create_orders_module import silent_limit_no_oco_sell_long
from binance_d.example_d.trade.damian_cancel_order import cancel_order_by_id_and_symbol
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, funcname, update_to_in_position, get_trigger_price_to_close, dump_radar_list
from binance_d.example_d.user.helpers_scripts.sql import exec_sql

from binance_d.impl.utils.timeservice import get_current_timestamp 

from binance_d.general_settings import adaperp_decimals
#factor_gain = 1.005

def get_factor_gain():
    factor_gain_config_file = "/home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/config_scripts/factor_gain.json"
    with open(factor_gain_config_file) as conf:
        data_dict = json.load(conf)
    factor_gain = data_dict['factor_gain']
   # print("factor_gain: " + str(factor_gain))
   # print("factor_gain type: " + str(type(factor_gain)))
    return factor_gain


def create_one_pivot(p_price, p_size, factor_gain):
    print("in " + funcname())
    # attention, ,"priceProtect":false by default
    clientorderid_value = "goto_in_position" + str(get_current_timestamp())
    #trigger_price_to_close = get_trigger_price_to_close(p_price, get_factor_gain())
    trigger_price_to_close = get_trigger_price_to_close(p_price, factor_gain)
    output = silent_limit_no_oco_sell_long(trigger_price_to_close, p_size, p_clientorderid=clientorderid_value )
    #print("output is type: " + str(type(output)))
    output_dict =  create_dict_from_output(output)
    '''
        output_dict = {'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'goto_in_position1657246327455', 
                       'closePosition': 'False', 'cumBase': '0.0', 'executedQty': '0.0', 'orderId': '7009365869', 
                       'origQty': '6.0', 'origType': 'LIMIT', 'positionSide': 'LONG', 'price': '0.8', 'priceRate': 'None', 
                       'reduceOnly': 'True', 'side': 'SELL', 'status': 'NEW', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 
                       'timeInForce': 'GTC', 'type': 'LIMIT', 'updateTime': '1657246333602', 'workingType': 'CONTRACT_PRICE'}
    '''
    print("output_dict: " + str(output_dict))
    return output_dict 

def insert_radar_list_new_pivot_sell_order(trigger_price_to_put_in_position, repeat, resize, output_dict, factor_gain):
    print("in insert_radar_list_new_pivot_sell_order: ", trigger_price_to_put_in_position, repeat, resize, output_dict, factor_gain)
    clientorderid_value = output_dict['clientOrderId']
    order_id_to_close = output_dict['orderId']
    order_id = "666" + str(order_id_to_close)
    trigger_price_to_close = output_dict['price']
    p_size = output_dict['origQty']

    sql = "insert into radar_list ( order_id, order_status, order_id_to_close, trigger_price_to_put_in_position,"
    sql += "trigger_price_to_close, original_quantity, clientorderid, repeat, resize, factor_gain ) values (" 
    sql += order_id + ", "
    sql += "'IN_POSITION', "
    sql += order_id_to_close + ", "
    sql += str(trigger_price_to_put_in_position) + ", "
    sql += str(trigger_price_to_close) + ", "
    sql += str(p_size) + ", " 
    sql += "'" + clientorderid_value + "', "
    sql += "'" + repeat + "', "
    sql +=  str(resize) + ", "
    sql +=  str(factor_gain) + ");"
    print("")
    print("sql: ", sql)
    rows_inserted = exec_sql(sql = sql, sql_command = "insert", error_message = "error in " + str(funcname()))
    if rows_inserted != 1:
        result = "ERROR_INSERT_RADAR_LIST"
        err = "ERROR in " + funcname() + ", aborting"
        print(err)
        raise 
    else:
        result = "OK"
        result += ", insert OK: " + sql  
        d = {'result': result, 'order_id': order_id, 'order_id_to_close': order_id_to_close, 'clientorderid': clientorderid_value}
        print(d)

def exec_transaction_pivot(p_price, p_size, factor_gain):
    print("in " + funcname() + " args p_price, p_size, factor_gain: " + str(p_price) + ", " + str(p_size) + ", factor_gain: " + str(factor_gain))
    err = ""
    try:
        print("call create_one_pivot(" + str(p_price) + ", " + str(p_size) + ")")
        rc = create_one_pivot(p_price, p_size, factor_gain)
        if "ERROR" in rc:
            err = "ERROR in " + funcname() + ", plus " + str(rc)
            print(err)
        else:
            output_dict = rc
            '''
            output_dict = {'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'goto_in_position1657246327455', 
                       'closePosition': 'False', 'cumBase': '0.0', 'executedQty': '0.0', 'orderId': '7009365869', 
                       'origQty': '6.0', 'origType': 'LIMIT', 'positionSide': 'LONG', 'price': '0.8', 'priceRate': 'None', 
                       'reduceOnly': 'True', 'side': 'SELL', 'status': 'NEW', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 
                       'timeInForce': 'GTC', 'type': 'LIMIT', 'updateTime': '1657246333602', 'workingType': 'CONTRACT_PRICE'}
            '''
            trigger_price_to_put_in_position = p_price
            repeat = 'Y'
            resize = p_size  

            #input("continue to execute insert_radar_list_new_pivot_sell_order, pec")
            insert_radar_list_new_pivot_sell_order(trigger_price_to_put_in_position, repeat, resize, output_dict, factor_gain)
            return "OK" 
    except:
        err = "except in " + funcname() + ", " + str(sys.exc_info())
        print(err)
        raise
    finally:
        if "ERROR" in err:
            print("transaction_pivot failed : " + err)
            raise

def create_multiple_pivots(distance_percentage, initial_price, pivots_number, size, factor_gain):
    distance = 1 + (distance_percentage/100)
    price = initial_price
    for counter_pivots in range(1, pivots_number + 1):
        price = round(price, adaperp_decimals)
        price = round(price * distance, adaperp_decimals)
        print("pivot number : " + str(counter_pivots) + ", price: " + str(price) + ", distance_percentage: " + str(distance_percentage) + ", size: " + str(size))
        #input("pec")
        exec_transaction_pivot(p_price=price, p_size=size, factor_gain=factor_gain)
        #input("next pivot, pec")
        

if __name__ == "__main__":
    distance_percentage = 0.125
    distance_percentage = 0.0625
    distance_percentage = 0.12
    distance_percentage = 0.06
    #distance_percentage = 0.0625/2
    factor_gain = (distance_percentage / 100 ) + 1
    #distance_percentage = 0.25
    #####
    # poner el tp del pivot inferior mas cercano
    initial_price = 0.31395
    pivots_number = 1    
    size = 1 
    #input("in main in " + funcname())
    create_multiple_pivots(distance_percentage, initial_price, pivots_number, size, factor_gain)   
