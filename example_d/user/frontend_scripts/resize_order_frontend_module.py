import sys
#from tkinter import W
from binance_d.requestclient import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *
from binance_d.impl.utils.timeservice import get_current_timestamp
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, funcname
from binance_d.example_d.user.helpers_scripts.sql import exec_sql
from binance_d.example_d.user.common_scripts.create_pivot_module import exec_transaction_pivot

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

def cancel_order_buy(order_id):
    symbol = "ADAUSD_PERP"
    result = "ERROR"
    print("in cancel_order_buy, order_id: ", order_id)
    try:
        output = request_client.cancel_order(symbol=symbol, orderId=str(order_id))
        output_dict =  create_dict_from_output(output)
        #PrintBasic.print_obj(output)
        print("in cancel_order_buy output_dict: ", output_dict)
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
        result += ", delete from radar_list where order_id='" + str(order_id) + "';"
        sql = "delete from radar_list where order_id='" + str(order_id) + "';"

        #print("sql: ", sql)
        rows_deleted = exec_sql(sql = sql, sql_command = "delete", error_message = "error in " + str(funcname()))
        #rows_inserted = 1
        if rows_deleted != 1:
            result = "ERROR_DELETE_RADAR_LIST"
        else:
            result = "OK, 1 row deleted, " + sql

        d = {'result': result, 'order_id': order_id}
        return d

def resize_order_buy_frontend(order_id, new_size):
        result_dict_cancel = {}
        result_dict = {}
        
        try:
            result_dict = get_data(order_id)
            print("result_dict:", result_dict)
        except: 
            print("ERROR except in " + funcname() + " get_data:" + str(sys.exc_info())) 
            result = str(sys.exc_info())
            d = {'result': str(result), 'order_id': order_id, 'new_size': new_size}
            return d
        print("result_dict get_data:", result_dict)
        if result_dict['order_id'] == 'not exists':
            print("order_id not exists")
            result = "order_id not exists"
            d = {'result': str(result), 'order_id': order_id, 'new_size': new_size}
            return d
        try:
            tpp = result_dict['trigger_price_to_put_in_position']
            factor_gain = result_dict['factor_gain']
        except:
            result = str(sys.exc_info())
            d = {'result': str(result), 'order_id': order_id, 'new_size': new_size}
            return d
        if tpp != 0 and factor_gain != 0:
            print("OK executing get_data, continue to cancel_order_buy")    
            try:
                result_dict_cancel = cancel_order_buy(order_id) 
                #d = {'result': result, 'order_id': order_id}
                #result_dict_cancel = {'result': 'ERROR cancel_order_buy', 'order_id': order_id}
                #result_dict_cancel = {'result': 'OK cancel_order_buy', 'order_id': order_id}
                #d = {'result': result, 'order_id': order_id}
                print("result_dict_cancel:", result_dict_cancel)
            except:
                err = "ERROR except in " + funcname() + " cancel_order_buy:" + str(sys.exc_info())
                print(err)
        if "ERROR" in result_dict_cancel['result']:
            result = result_dict_cancel['result']
            d = {'result': str(result), 'order_id': order_id, 'new_size': new_size}
            print("d:", d)
            return d
        else:
            result = "cancel_order_buy OK"
            try:
                print("call exec_transaction_pivot  ")
                result = exec_transaction_pivot(tpp, new_size, factor_gain)
                print("result exec_transaction_pivot:", result)
                #result = "OK call exec_transaction_pivot"
                #raise
                 
            except:
                err = "except exec_transaction_pivot: " + str(sys.exc_info())
                print(err) 
                result = err 
        d = {'result': str(result), 'order_id': order_id, 'new_size': new_size}
        print("hola  d:", d)
        return d

def get_data(order_id):
    symbol = "ADAUSD_PERP"
    result = "ERROR"
    print("in " + funcname() )
    sql = "select order_id, trigger_price_to_put_in_position, factor_gain from radar_list where "
    sql += " order_status in ('NEW') and "
    sql += " order_id='" + str(order_id) + "';"
    res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "query_get_data")
    print("res_sql: ", res_sql)
    if res_sql == []:
        print("res_sql empty")
        res_dict = [{'order_id': "not exists", 'trigger_price_to_put_in_position': 0, 'factor_gain': 0}][0] #convert list of tuples in list of dicts
        #print("in get_data:", res_dict)
        #res_dict: [{'order_id': 7548752963, 'trigger_price_to_put_in_position': 0.44904, 'factor_gain': 1.00125}]
    else:
        res_dict = [{'order_id':a[0], 'trigger_price_to_put_in_position':a[1], 'factor_gain':a[2]} for a in res_sql][0] #convert list of tuples in list of dicts
        print("res_dict:", res_dict)
    #res_dict: [{'order_id': 7548752963, 'trigger_price_to_put_in_position': 0.44904, 'factor_gain': 1.00125}]
    
    return res_dict



