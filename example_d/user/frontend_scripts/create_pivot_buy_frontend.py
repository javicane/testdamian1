import sys
import json
#from binance_d.requestclient import RequestClient
#from binance_d.subscriptionclient import SubscriptionClient
#from binance_d import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *


from socket import create_connection
from binance_d.example_d.user.common_scripts.create_orders_module import silent_limit_no_oco_buy_long
from binance_d.example_d.trade.damian_cancel_order import cancel_order_by_id_and_symbol
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, funcname, update_to_in_position, get_trigger_price_to_close, dump_radar_list
from binance_d.example_d.user.helpers_scripts.sql import exec_sql

from binance_d.impl.utils.timeservice import get_current_timestamp 

from binance_d.general_settings import adaperp_decimals

def check_price_and_size(p_price, p_size, output_dict):
    #p_size = 1000
    if ( ( ( float(p_price) - float(output_dict['price']) ) == 0 ) and
         ( ( round(float(p_size)) - round(float(output_dict["origQty"])) ) == 0 ) ):
        print("price and size ok") 
        return "OK" 
    else:
        print("ERROR in " + funcname()) 
        return "ERROR in check_price_and_size"
        

def create_one_pivot(p_price, p_size):
    '''
    return ERROR or output_dict
    '''
    print("in " + funcname())
    # attention, ,"priceProtect":false by default
    clientorderid_value = "new_pivot" + str(get_current_timestamp())
    print("clientorderid_value", clientorderid_value)
    output = silent_limit_no_oco_buy_long(p_price, p_size, p_clientorderid=clientorderid_value )
    #print("output is type: " + str(type(output)))
    output_dict =  create_dict_from_output(output)
    print("output_dict: " + str(output_dict))
    ##output_dict: {'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'new_pivot1669863253721', 'closePosition': 'False', 
    # 'cumBase': '0.0', 'executedQty': '0.0', 'orderId': '7920086440', 'origQty': '1.0', 'origType': 'LIMIT', 
    # 'positionSide': 'LONG', 'price': '0.14981', 'priceRate': 'None', 'reduceOnly': 'False', 'side': 'BUY', 
    # 'status': 'NEW', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 'timeInForce': 'GTC', 'type': 'LIMIT', 
    # 'updateTime': '1669863256587', 'workingType': 'CONTRACT_PRICE'}
    rc = check_price_and_size(p_price, p_size, output_dict) 
    print("in " + funcname() + ", rc: " + str(rc))
    if "ERROR" in rc:
        err = "ERROR in " + funcname() + ", plus " + str(rc)
        print(err)
        return err
    else:
        return output_dict 


def insert_radar_list_new_pivot(output_dict, factor_gain, resize, repeat): 
    print("in insert_radar_list_new_pivot")
    price = output_dict['price']
    order_id = output_dict['orderId']
    order_status = "NEW"
    order_id_to_close = 0
    trigger_price_to_put_in_position = price
    trigger_price_to_close = get_trigger_price_to_close(price, factor_gain)
    original_quantity = output_dict['origQty']
    clientorderid = output_dict['clientOrderId']

    tuple1 = (order_id, order_status, order_id_to_close, trigger_price_to_put_in_position, trigger_price_to_close, original_quantity, clientorderid, resize, factor_gain, repeat)
    sql = "insert into radar_list ( order_id, order_status, order_id_to_close, trigger_price_to_put_in_position,"
    sql += "trigger_price_to_close, original_quantity, clientorderid, resize, factor_gain, repeat ) values " 
    sql += str(tuple1)

    try:
        rows_inserted = exec_sql(sql = sql, sql_command = "insert", error_message = "error in " + str(funcname()))
    except:
        result = "ERROR_INSERT_RADAR_LIST " + str(sys.exc_info())
        print("except in  " + str(funcname()) + " ERROR_INSERT_RADAR_LIST:", result)
        d = {'result': result, 'order_id': order_id, 'order_id_to_close': order_id_to_close, 'clientorderid': clientorderid}
        print(d)
        return d
    
    if rows_inserted != 1:
        result = "ERROR_INSERT_RADAR_LIST"
        print("rows_inserted ERROR:", rows_inserted) 
        d = {'result': result, 'order_id': order_id, 'order_id_to_close': order_id_to_close, 'clientorderid': clientorderid}
        print(d)
        return d
    else:
        result = "insert OK" 
        d = {'result': result, 'order_id': order_id, 'order_id_to_close': order_id_to_close, 'clientorderid': clientorderid}
        print(d)
        return d

def exec_transaction_pivot(p_price, p_size, factor_gain, resize, repeat):
    print("in " + funcname() + " args p_price, p_size, factor_gain: " + str(p_price) + ", " + str(p_size) + ", " + str(factor_gain))
    err = ""
    d = ""
    #custom_trigger_price_to_close = get_trigger_price_to_close(p_price, factor_gain)
    #print("custom_trigger_price_to_close:", custom_trigger_price_to_close)
    #sys.exit(66)
    try:
        print("call create_one_pivot(" + str(p_price) + ", " + str(p_size) + ")")
        rc = create_one_pivot(p_price, p_size)
        # example output can be ERROR or output_dict
        #rc: {'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'new_pivot1669863253721', 'closePosition': 'False', 
        # 'cumBase': '0.0', 'executedQty': '0.0', 'orderId': '7920086440', 'origQty': '1.0', 'origType': 'LIMIT', 
        # 'positionSide': 'LONG', 'price': '0.14981', 'priceRate': 'None', 'reduceOnly': 'False', 'side': 'BUY', 
        # 'status': 'NEW', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 'timeInForce': 'GTC', 'type': 'LIMIT', 
        # 'updateTime': '1669863256587', 'workingType': 'CONTRACT_PRICE'}
        if "ERROR" in rc:
            err += "ERROR in " + funcname() + ", plus " + str(rc)
            print(err)
            d = dict(result=err, order_id=666, order_id_to_close=777, price_to_put_in_position=1, price_close=1 )
            print("transaction_pivot failed d", d)
            return d 
        else:
            output_dict = rc
            order_id = output_dict['orderId']
            order_id_to_close = 0
            price = output_dict['price']
            trigger_price_to_close = get_trigger_price_to_close(price, factor_gain)

            '''
            order_id_to_close = output_dict['order_id_to_close']
            client_order_id = output_dict['clientOrderId']
            order_status = "NEW"
            order_id_to_close = 0
            trigger_price_to_put_in_position = price
            trigger_price_to_close = get_trigger_price_to_close(price, factor_gain)
            original_quantity = output_dict['origQty']
            clientorderid = output_dict['clientOrderId']
            resize = original_quantity
            '''

            print("create_one_pivot OK", rc)
            result = insert_radar_list_new_pivot(output_dict, factor_gain, resize, repeat)
            # example in exec_transaction_pivot, result from insert_radar_list_new_pivot {'result': 'ERROR_INSERT_RADAR_LIST', 'order_id': '7925738883', 
            # 'order_id_to_close': 0, 'clientorderid': 'new_pivot1670067931108'}
            # the key "result" can be "ERROR_INSERT_RADAR_LIST" or "insert OK"
            print("")
            print("in " + funcname() + ", result from insert_radar_list_new_pivot", result)
            if "ERROR" in result['result']:
                message = result['result']
                d = dict(result=message, order_id=order_id, order_id_to_close=order_id_to_close, price_to_put_in_position=price, price_close=trigger_price_to_close)
                print("transaction_pivot failed d", d)
                return d 
                #sys.exit(66)
            else:
                print("transaction_pivot OK d", d)
                return output_dict
    except:
        err = "except in " + funcname() + ", " + str(sys.exc_info())
        print(err)
        message = err
        #d = dict(result=err, order_id=666, order_id_to_close=777, price_to_put_in_position=1, price_close=1 )
        d = dict(result=message, order_id="", order_id_to_close="", price_to_put_in_position="", price_close="" )
        return d 

def create_multiple_pivots(up_down, distance_percentage, initial_price, pivots_number, size, factor_gain, resize, repeat, price_tpos, price_tclose):
    print("in create_multiple_pivots distance_percentage", distance_percentage)
    print("in create_multiple_pivots initial_price", initial_price)
    print("in create_multiple_pivots factor_gain", factor_gain)
    print("in create_multiple_pivots up_down", up_down)
    distance = 1 - (distance_percentage/100)
    print("in create_multiple_pivots distance", distance)
    price = initial_price
    if up_down != "CUSTOM":
        for counter_pivots in range(1, pivots_number + 1):
            price = round(price * distance, adaperp_decimals)
            print("pivot number : " + str(counter_pivots) + ", price: " + str(price) + ", distance_percentage: " + str(distance_percentage) + ", size: " + str(size))
            result_dict = exec_transaction_pivot(price, size, factor_gain, resize, repeat)
            # returns a dict
            result_dict['result'] = "OK"
            result_dict['price_close'] = get_trigger_price_to_close(price, factor_gain)
            print("OK result_dict from exec_transaction_pivot:", result_dict)
            return result_dict
    elif up_down == "CUSTOM":
        price = price_tpos
        print("custom pivot: " + ", price_tpos: " + str(price) + ", factor_gain: " + str(factor_gain) + ", size: " + str(size))
        result_dict = exec_transaction_pivot(price_tpos, size, factor_gain, resize, repeat)
        # returns a dict
        result_dict['result'] = "OK"
        result_dict['price_close'] = price_tclose
        print("OK result_dict from exec_transaction_pivot custom:", result_dict)
        return result_dict
        
        
def create_pivot_buy_frontend(up_down, price, size, repeat, resize, factor_gain, price_tpos, price_tclose):
    distance_percentage = round((factor_gain - 1 )*100, adaperp_decimals)
    pivots_number = 1       
    if up_down == "DOWN":
        initial_price = price
    elif up_down == "UP":
        initial_price = round(price*factor_gain, adaperp_decimals) 
    elif up_down == "CUSTOM":
        initial_price = price
        print("in create_pivot_buy_frontend custom factor_gain", factor_gain)
        print("in create_pivot_buy_frontend custom price_tpos", price_tpos)
        print("in create_pivot_buy_frontend custom price_tclose", price_tclose)
    print("initial_price:", initial_price)
    result_dict = create_multiple_pivots(up_down, distance_percentage, initial_price, pivots_number, size, factor_gain, resize, repeat, price_tpos, price_tclose)   
    print("result_dict in create_pivot_buy_frontend", result_dict)
    return result_dict
