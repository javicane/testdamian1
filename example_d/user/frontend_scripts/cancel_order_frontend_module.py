import sys
#from tkinter import W
from binance_d.requestclient import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *
from binance_d.impl.utils.timeservice import get_current_timestamp
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, funcname
from binance_d.example_d.user.helpers_scripts.sql import exec_sql

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

def cancel_order_frontend(order_id):
    symbol = "ADAUSD_PERP"
    result = "ERROR"
    print("in cancel_order_frontend, order_id: ", order_id)
    try:
        output = request_client.cancel_order(symbol=symbol, orderId=str(order_id))
        output_dict =  create_dict_from_output(output)
        #PrintBasic.print_obj(output)
        print("in cancel_order_frontend output_dict: ", output_dict)
        result = "OK"
    except:
        print("except")
        #[Executing] -2011: Unknown order sent.
        result = "ERROR, timestamp: " + str(get_current_timestamp()) + ", "
        result += str(sys.exc_info())
        d = {'result': result, 'order_id': order_id}
        print("except d:", d)
        return d
     
    if result == "OK":
        result += ", delete from radar_list where order_id='" + str(order_id) + "' or order_id_to_close='" + str(order_id) +"';"
        sql = "delete from radar_list where order_id='" + str(order_id) + "' or order_id_to_close='" + str(order_id) +"';"

        #print("sql: ", sql)
        rows_deleted = exec_sql(sql = sql, sql_command = "delete", error_message = "error in " + str(funcname()))
        #rows_inserted = 1
        if rows_deleted != 1:
            result = "ERROR_DELETE_RADAR_LIST"
        else:
            result = "OK, 1 row deleted, " + sql

        d = {'result': result, 'order_id': order_id}
        return d
    #output_dict:  {'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'new_pivot1657398472645', 
    # 'closePosition': 'False', 'cumBase': '0.0', 'executedQty': '0.0', 'orderId': '7025120813', 'origQty': '1.0', 
    # 'origType': 'LIMIT', 'positionSide': 'LONG', 'price': '0.2', 'priceRate': 'None', 'reduceOnly': 'False', 
    # 'side': 'BUY', 'status': 'CANCELED', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 'timeInForce': 'GTC', 
    # 'type': 'LIMIT', 'updateTime': '1657399156019', 'workingType': 'CONTRACT_PRICE'}

########


def cancel_order_bulk_by_price_range_frontend(price_high, price_low):
    symbol = "ADAUSD_PERP"
    result = "ERROR"
    print("in " + funcname() + ", price_high:" + str(price_high) + ", price_low:" + str(price_low))
    sql = "select order_id, order_id_to_close from radar_list where "
    sql += "trigger_price_to_put_in_position <= "
    sql += str(price_high) + " and "
    sql += "trigger_price_to_put_in_position >= " + str(price_low)
    sql += " and order_status in ('NEW', 'IN_POSITION');"
    res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "query_cancel_order_bulk_by_price_range")
    print("res_sql: ", res_sql)
    res_dict = [{'order_id':a[0], 'order_id_to_close':a[1]} for a in res_sql] #convert list of tuples in list of dicts
    print("res_dict:", res_dict)
    #result = res_dict 
    #[{'order_id': 7403100482, 'order_id_to_close': 0}, 
    # {'order_id': 7403100491, 'order_id_to_close': 0}, 
    # {'order_id': 7404534787, 'order_id_to_close': 0}]
    result_acum = ""
    for order_dict in res_dict:
        order_id = order_dict['order_id']
        order_id_to_close = order_dict['order_id_to_close']
        symbol = "ADAUSD_PERP"
        result = "ERROR"
        print("processing order_dict:", order_dict)
        print("order_id: ", order_id)
        print("order_id_to_close: ", order_id_to_close)
        if order_id_to_close == 0:
            print("....order_id_to_close = 0")
            order_id_to_cancel = order_id
           # print("order_id_to_cancel:", order_id_to_cancel)
        else:
            print(".... order_id_to_close != 0")
            order_id_to_cancel = order_id_to_close
            #print("order_id_to_cancel:", order_id_to_cancel)
        print("in " + funcname() + ", order_id_to_cancel: ", order_id_to_cancel)
        try:
            output = request_client.cancel_order(symbol=symbol, orderId=str(order_id_to_cancel))
            output_dict =  create_dict_from_output(output)
            #PrintBasic.print_obj(output)
            print("in " + funcname() + ", request_client.cancel_order output_dict: ", output_dict)
            result = "OK"
            #my_dict = dict(order_id_to_cancel=order_id_to_cancel, result=)
        except:
           # print("except")
            #[Executing] -2011: Unknown order sent.
            result = "ERROR, timestamp: " + str(get_current_timestamp()) + ", "
            result += str(sys.exc_info())
            d = {'result': str(result), 'price_high': price_high, 'price_low': price_low}
            print("except d:", d)
            return d 
        if result == "OK":
            print("OK canceled, deleting")
            sql = "delete from radar_list where order_id='" + str(order_id_to_cancel) + "' or order_id_to_close='" + str(order_id_to_cancel) +"';"
            #print("sql: ", sql)
            rows_deleted = exec_sql(sql = sql, sql_command = "delete", error_message = "error in " + str(funcname()))
            if rows_deleted != 1:
                result = "ERROR_DELETE_RADAR_LIST"
                print(result)
            else:
                print("OK deleted 1 row")
                result_acum += "order_id_to_cancel: " + str(order_id_to_cancel) + ": OK canceled and deleted from radar_list, "
                print("result_acum:", result_acum)
    result = result_acum
    d = {'result': str(result), 'price_high': price_high, 'price_low': price_low}
    print("return d:", d)
    return d
    '''
    try:
        output = request_client.cancel_order(symbol=symbol, orderId=str(order_id))
        output_dict =  create_dict_from_output(output)
        #PrintBasic.print_obj(output)
        print("in cancel_order_frontend output_dict: ", output_dict)
        result = "OK"
    except:
        print("except")
        #[Executing] -2011: Unknown order sent.
        result = "ERROR, timestamp: " + str(get_current_timestamp()) + ", "
        result += str(sys.exc_info())
        d = {'result': result, 'order_id': order_id}
        print("except d:", d)
        return d
    ''' 
    '''
    if result == "OK":
        result += ", delete from radar_list where order_id='" + str(order_id) + "' or order_id_to_close='" + str(order_id) +"';"
        sql = "delete from radar_list where order_id='" + str(order_id) + "' or order_id_to_close='" + str(order_id) +"';"

        #print("sql: ", sql)
        rows_deleted = exec_sql(sql = sql, sql_command = "delete", error_message = "error in " + str(funcname()))
        #rows_inserted = 1
        if rows_deleted != 1:
            result = "ERROR_DELETE_RADAR_LIST"
        else:
            result = "OK, 1 row deleted, " + sql

        d = {'result': result, 'order_id': order_id}
        return d
    #output_dict:  {'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'new_pivot1657398472645', 
    # 'closePosition': 'False', 'cumBase': '0.0', 'executedQty': '0.0', 'orderId': '7025120813', 'origQty': '1.0', 
    # 'origType': 'LIMIT', 'positionSide': 'LONG', 'price': '0.2', 'priceRate': 'None', 'reduceOnly': 'False', 
    # 'side': 'BUY', 'status': 'CANCELED', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 'timeInForce': 'GTC', 
    # 'type': 'LIMIT', 'updateTime': '1657399156019', 'workingType': 'CONTRACT_PRICE'}
    '''
########