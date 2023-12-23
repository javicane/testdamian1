import sys
from xml.etree.ElementPath import prepare_predicate
from binance_d.example_d.user.helpers_scripts.helpers_module import funcname, create_dict_from_output
from binance_d.example_d.user.common_scripts.create_orders_module import silent_limit_no_oco_sell_long
from binance_d.example_d.user.helpers_scripts.sql import exec_sql
from binance_d.impl.utils.timeservice import get_current_timestamp


#rc = process_goto_in_position(event_order_id, radar_list_dict_order_id)
#return rc
def insert_radar_list_new_pivot(order_id, trigger_price_to_put_in_position, trigger_price_to_close, p_size, clientorderid): 
    print("in " + funcname() + ", args order_id, trigger_price_to_put_in_position, trigger_price_to_close, p_size, clientorderid: " + str(order_id) + ", " + str(trigger_price_to_put_in_position) + ", "  + str(trigger_price_to_close) + ", " + str(p_size) + ", " + clientorderid)
    order_status = "NEW"
    order_id_to_close = 0
    original_quantity = p_size 

    tuple1 = (order_id, order_status, order_id_to_close, trigger_price_to_put_in_position, trigger_price_to_close, original_quantity, clientorderid)
    sql = "insert into radar_list ( order_id, order_status, order_id_to_close, trigger_price_to_put_in_position,"
    sql += "trigger_price_to_close, original_quantity, clientorderid ) values " 
    sql += str(tuple1)

    rows_inserted = exec_sql(sql = sql, sql_command = "insert", error_message = "error in " + str(funcname()))
    if rows_inserted != 1:
        err = "ERROR in " + funcname() + ", aborting"
        print(err)
        raise 

def cook_sell(order_id, trigger_price_to_put_in_position, trigger_price_to_close, p_size):
    print("in " + funcname() + ", args order_id, trigger_price_to_put_in_position, trigger_price_to_close, p_size: " + str(order_id) + ", " + str(trigger_price_to_put_in_position) + ", "  + str(trigger_price_to_close) + ", " + str(p_size))
    clientorderid_value = "goto_in_position" + str(get_current_timestamp())
    insert_radar_list_new_pivot(order_id, trigger_price_to_put_in_position, trigger_price_to_close, p_size, clientorderid_value)

    print(".... create limit order to close, call silent_limit_no_oco_sell_long")
    output = silent_limit_no_oco_sell_long(trigger_price_to_close, p_size, p_clientorderid=clientorderid_value)
    print(".... .... output: " + str(output))
    output_dict =  create_dict_from_output(output)
    print(".... .... output_dict: " + str(output_dict))
    print(".... .... output_dict is type: " + str(type(output_dict)))
    #POST LIMIT ,no OCO, SELL, LONG
    #result OK: {"orderId":5370806071,"symbol":"ADAUSD_PERP","pair":"ADAUSD","status":"NEW","clientOrderId":"goto_in_position + timestamp",
    #"price":"100","avgPrice":"0.00000","origQty":"1","executedQty":"0","cumQty":"0","cumBase":"0","timeInForce":"GTC","type":"LIMIT","reduceOnly":true,
    #"closePosition":false,"side":"SELL","positionSide":"LONG","stopPrice":"0","workingType":"CONTRACT_PRICE","priceProtect":false,"origType":"LIMIT","updateTime":1645305366798}
    order_id_to_close = output_dict['orderId']
    
    print(".... .... order_id_to_close: " + str(order_id_to_close))
    sql = "update radar_list set order_status ='IN_POSITION', "
    sql += "order_id_to_close = " + order_id_to_close
    sql += " where order_id ='" + order_id + "' and order_status='NEW'"
    print(".... .... exec_sql with sql: " + str(sql)) 
    result = exec_sql(sql = sql , sql_command = "update", error_message = "update process_goto_in_position")
    if result != 1:
        print(".... .... .... ERROR in " + funcname() + ", result: " + str(result))
        rc = "ERROR in process_goto_in_position exec_sql"
        return rc
        #raise
    else:
        print(".... .... .... OK, 1 row updated") 
        rc = "OK process_goto_in_position" 
        return rc

def call_cook_sell():
    order_id = "6661"
    trigger_price_to_put_in_position = 0.59
    trigger_price_to_close = 0.6
   
    p_size = 24 
    rc = cook_sell(order_id, trigger_price_to_put_in_position, trigger_price_to_close, p_size)

call_cook_sell()