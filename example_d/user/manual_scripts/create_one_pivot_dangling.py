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



def check_price_and_size(p_price, p_size, output_dict):
    #input(funcname() + ", pec")
    print("output_dict: " + str(output_dict))
    print("status: " + str(output_dict['status']))
    print("price: " + str(output_dict['price']))
    print("origQty: " + str(output_dict['origQty']))
    print("orderId: " + str(output_dict['orderId']))
    #p_price = 10
    if ( ( ( float(p_price) - float(output_dict['price']) ) == 0 ) and
         ( ( round(float(p_size)) - round(float(output_dict["origQty"])) ) == 0 ) ):
        print("price and size ok") 
        return "OK" 
    else:
        print("ERROR in " + funcname()) 
        return "ERROR in check_price_and_size"
        

def create_one_pivot(p_price, p_size, trigger_price_to_close):
    print("in " + funcname())
    # attention, ,"priceProtect":false by default
    #get_current_timestamp
    clientorderid_value = "new_pivot" + str(get_current_timestamp())
    output = silent_limit_no_oco_buy_long(p_price, p_size, p_clientorderid=clientorderid_value )
    #print("output is type: " + str(type(output)))
    output_dict =  create_dict_from_output(output)
   # print("output_dict: " + str(output_dict))
    #print("status: " + str(output_dict['status']))
    #print("price: " + str(output_dict['price']))
    #print("origQty: " + str(output_dict['origQty']))
    #print("orderId: " + str(output_dict['orderId']))
    rc = check_price_and_size(p_price, p_size, output_dict) 
    print("in " + funcname() + ", rc: " + str(rc))
    if "ERROR" in rc:
        err = "ERROR in " + funcname() + ", plus " + str(rc)
        print(err)
        return err
    else:
        return output_dict, trigger_price_to_close


def insert_radar_list_new_pivot(output_dict, trigger_price_to_close, resize, factor_gain): 
    price = output_dict['price']
    order_id = output_dict['orderId']
    order_status = "NEW"
    order_id_to_close = 0
    trigger_price_to_put_in_position = price
    original_quantity = output_dict['origQty']
    clientorderid = output_dict['clientOrderId']

    tuple1 = (order_id, order_status, order_id_to_close, trigger_price_to_put_in_position, trigger_price_to_close, original_quantity, clientorderid, resize, factor_gain)
    sql = "insert into radar_list ( order_id, order_status, order_id_to_close, trigger_price_to_put_in_position,"
    sql += "trigger_price_to_close, original_quantity, clientorderid, resize, factor_gain ) values " 
    sql += str(tuple1)

    rows_inserted = exec_sql(sql = sql, sql_command = "insert", error_message = "error in " + str(funcname()))
    if rows_inserted != 1:
        err = "ERROR in " + funcname() + ", aborting"
        print(err)
        raise 
    

def exec_transaction_pivot(p_price, p_size, trigger_price_to_close, resize, factor_gain):
    print("in " + funcname() + " args p_price, p_size, trigger_price_to_close, resize: " + str(p_price) + ", " + str(p_size) + ", " + str(trigger_price_to_close) + ", resize: " + str(resize) + ", factor_gain: " + str(factor_gain))
    err = ""
    try:
        print("call create_one_pivot(" + str(p_price) + ", " + str(p_size) + ")")
        rc, trigger_price_to_close = create_one_pivot(p_price, p_size, trigger_price_to_close)  
        if "ERROR" in rc:
            err = "ERROR in " + funcname() + ", plus " + str(rc)
            print(err)
        else:
            #next_step_dict = { "name" : insert_radar_list_new_pivot }
            #print("in " + funcname() + ", call:  " + str(next_step_dict['name']))
            #next_step_dict['name'](rc)
            output_dict = rc
            insert_radar_list_new_pivot(output_dict, trigger_price_to_close, resize, factor_gain)
            return "OK" 
    except:
        err = "except in " + funcname() + ", " + str(sys.exc_info())
        print(err)
        raise
    finally:
        if "ERROR" in err:
            print("transaction_pivot failed : " + err)
            raise


if __name__ == "__main__":
    p_price = 0.4570
    p_size = 7 
    trigger_price_to_close = 0.45724
    resize = p_size
    factor_gain = 1.0012
    exec_transaction_pivot(p_price, p_size, trigger_price_to_close, resize, factor_gain)