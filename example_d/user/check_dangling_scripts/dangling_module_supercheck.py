import pdb
#pdb.set_trace()
import sys
#sys.path.append("C:/binance/futures/futures")
#print("in dangling_module line 3")
from binance_d.requestclient import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, funcname, get_radar_list
from binance_d.example_d.user.helpers_scripts.sql import exec_sql
from difflib import SequenceMatcher

def write_line(message, silent="NO"):
    if silent == "NO":
        print(message)

def get_position_size(silent): 
    #input("in get_position_size, pec")
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    result = request_client.get_position()
##### in example_d.trade.get_position.py result is type:<class 'list'>
#i dict: {'entryPrice': '0.0', 'isAutoAddMargin': 'True', 'isolatedMargin': '0.0', 'leverage': '20.0', 'liquidationPrice': '0.0', 'marginType': 'cross', 'markPrice': '0.78346', 'maxQty': '250000.0', 'positionAmt': '0.0', 'positionSide': 'BOTH', 'symbol': 'ADAUSD_PERP', 'unrealizedProfit': '0.0'}
#i dict: {'entryPrice': '0.89230367', 'isAutoAddMargin': 'True', 'isolatedMargin': '0.0', 'leverage': '20.0', 'liquidationPrice': '0.46101131', 'marginType': 'cross', 'markPrice': '0.78346', 'maxQty': '250000.0', 'positionAmt': '97.0', 'positionSide': 'LONG', 'symbol': 'ADAUSD_PERP', 'unrealizedProfit': '-151.02380433'}
#i dict: {'entryPrice': '0.0', 'isAutoAddMargin': 'True', 'isolatedMargin': '0.0', 'leverage': '20.0', 'liquidationPrice': '0.0', 'marginType': 'cross', 'markPrice': '0.78346', 'maxQty': '250000.0', 'positionAmt': '0.0', 'positionSide': 'SHORT', 'symbol': 'ADAUSD_PERP', 'unrealizedProfit': '0.0'}
    my_list = []
    for idx, row in enumerate(result):
        my_dict = create_dict_from_output(row)
        my_list.append(my_dict)
    #print("my_list: " + str(my_list))
    #input("in get_position_size, before for, pec")
    for i in my_list:
        #input("in for loop, pec")
        position_size = i['positionAmt']
        if i['symbol'] == "ADAUSD_PERP" and float(position_size) > 0:
            #print("i dict: " + str(i))
            write_line("---------------ADA position_size: " + str(float(position_size)), silent)
            break
        else:
            #print("symbol: " + i['symbol'])
            nada = 1
    #print("in " + funcname() + ", return position_size: " + str(position_size))
    return int(round(float(position_size),0))

def get_open_orders_dict():
    '''
    returns:
        my_list: list, list of dicts
    '''
    #input("in " + funcname() + ",pec 1")
    #request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    #result = request_client.get_open_orders(symbol="btcusd_200925")
    #print("request.client.get_open_orders")
    #input("in " + funcname() + ",pec 2")
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    result = request_client.get_open_orders(symbol="ADAUSD_PERP")
    #output result is list of dicts:
    # [{"orderId":6182797447,"symbol":"ADAUSD_PERP","pair":"ADAUSD","status":"NEW","clientOrderId":"6VFxtvJFEUWBGMf16V3IFu",
    #   "price":"0.09925","avgPrice":"0","origQty":"1","executedQty":"0","cumBase":"0","timeInForce":"GTC","type":"LIMIT",
    #   "reduceOnly":false,"closePosition":false,"side":"BUY","positionSide":"LONG","stopPrice":"0","workingType":"CONTRACT_PRICE",
    #   "priceProtect":false,"origType":"LIMIT","time":1651362220827,"updateTime":1651362220827}, 
    #  {"orderId":6183249705,"symb
    #print("result: " + str(result))
    #input("in " + funcname() + ",pec 3")
    my_list = []
    for idx, row in enumerate(result):
        #print("data number " + (str(idx)) + " :")
        my_dict = create_dict_from_output(row)
        my_list.append(my_dict)
        #print("my_dict: " + str(my_dict))
    #input("in: " + funcname() + ", my_list: " + str(my_list))
    return my_list
##########################

def check2new_2(radar, current, open_orders_list, silent):
# checkear que el size de las 
#      a = sorted(radar_list_open_orders_limit_sell_to_close)
#        b = sorted(current_open_orders_limit_sell_to_close)
    print("################### check2new begin")
    nada = 1
    extra_radar_list_open_orders_limit_sell_to_close = [ i for i in radar if i not in current ]
    extra_current_open_orders_limit_sell_to_close = [ i for i in current if i not in radar ]
    if extra_radar_list_open_orders_limit_sell_to_close:
        write_line("....", silent)
        write_line("estas order_id_to_close existen en radar_list pero no existen fisicamente las ordenes venta SELL NEW", silent)
        write_line("significa que fueron filleadas pero no se repitio el pivot y tampoco se hizo update a PNL", silent)
        write_line("debe recrearse el pivot, y update del registro dangling de la base a PNL", silent)
        #write_line('radar_list_open_orders_limit_sell_to_close has: ' + str(a[i:j]), silent)
        write_line('radar_list_open_orders_limit_sell_to_close has: ' + str(extra_radar_list_open_orders_limit_sell_to_close), silent)
        #for order_dangling in a[i:j]:
        for order_dangling in extra_radar_list_open_orders_limit_sell_to_close:
            write_line("+", silent)
            write_line("procesando nueva order_dangling", silent)
            write_line("vamos a comprobar que no haya niguna orden fisica con el order_id de la order_dangling: " + str(order_dangling), silent)
            match_flag = False
            for kk in open_orders_list:
                #print("processing :" + str(kk))
                if order_dangling in kk:
                    write_line("match: " + str(kk), silent)
                    match_flag = True
                    break
                else:
                    #print(".... no match, next")
                    nada = 1
            if not match_flag:
                write_line(".... no existe ninguna orden fisica con el order_id de la order_dangling", silent)
                #write_line(".... seguimos con los siguientos pasos", silent)
            
                write_line("select * from radar_list where order_id_to_close=" + str(order_dangling) + ";", silent)
                sql = "select * from radar_list where order_id_to_close=" + str(order_dangling) + ";"
                entire_row = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error dangling")
                write_line(".... entire_row: " + str(entire_row), silent)

                sql = "select trigger_price_to_put_in_position, original_quantity from radar_list where order_id_to_close=" + str(order_dangling) + ";"
                result = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error dangling")
                write_line(".... trigger_price_to_put_in_position: " + str(result[0]), silent)
                write_line(".... original_quantity: " + str(result[1]), silent)
                write_line(".... .... recrear pivot ATENCION, factor_gain se usara el actual, no el que tenia en radar_list, sino hay que hacer una funcion nueva que setee el que tenia", silent)
                p_price = result[0]
                p_size = result[1]
                write_line("p_price type: " + str(type(p_price)), silent)
                write_line("p_size type: " + str(type(p_size)), silent)
                write_line("update radar_list set order_status='PNL' where order_id_to_close=" + str(order_dangling) + ";", silent)
            else:
                write_line("strange situation, se debe analizar que hacer con este registro", silent)
                write_line("++++++++++++++++++++++++++++++++++++++++++++++++++++++++", silent)
        #if tag in ('insert', 'replace'):
    if extra_current_open_orders_limit_sell_to_close:
        write_line("....", silent)
        write_line("estas limit_sell_order_to_close existen fisicamente como SELL NEW pero no estan en radar_list con status: where order_id_to_close != 0 and order_status = 'IN_POSITION' ", silent)
        write_line("es strange, se deberia hacer un insert, pero se debe analizar", silent)
        #write_line('current_open_orders_limit_sell_to_close has: ' + str(b[k:l]), silent)
        write_line('current_open_orders_limit_sell_to_close has: ' + str(extra_current_open_orders_limit_sell_to_close), silent)
        write_line("vamos a comprobar si existe un row en radar_list where order_id=order_dangling or order_id_to_close=order_dangling", silent)
        #for order_dangling in b[k:l]:
        for order_dangling in extra_current_open_orders_limit_sell_to_close:
            sql = "select * from radar_list where order_id_to_close=" + str(order_dangling) + " or order_id=" + str(order_dangling) + ";"
            write_line("processing sql: " + str(sql), silent)
            result = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error dangling")
            write_line(".... result: " + str(result), silent)
    print("################### check2new end")


############################
def check2new(radar, current, open_orders_list, silent):
#      a = sorted(radar_list_open_orders_limit_sell_to_close)
#        b = sorted(current_open_orders_limit_sell_to_close)
    print("################### check2new begin")
    nada = 1
    extra_radar_list_open_orders_limit_sell_to_close = [ i for i in radar if i not in current ]
    extra_current_open_orders_limit_sell_to_close = [ i for i in current if i not in radar ]
    if extra_radar_list_open_orders_limit_sell_to_close:
        write_line("....", silent)
        write_line("estas order_id_to_close existen en radar_list pero no existen fisicamente las ordenes venta SELL NEW", silent)
        write_line("significa que fueron filleadas pero no se repitio el pivot y tampoco se hizo update a PNL", silent)
        write_line("debe recrearse el pivot, y update del registro dangling de la base a PNL", silent)
        #write_line('radar_list_open_orders_limit_sell_to_close has: ' + str(a[i:j]), silent)
        write_line('radar_list_open_orders_limit_sell_to_close has: ' + str(extra_radar_list_open_orders_limit_sell_to_close), silent)
        #for order_dangling in a[i:j]:
        for order_dangling in extra_radar_list_open_orders_limit_sell_to_close:
            write_line("+", silent)
            write_line("procesando nueva order_dangling", silent)
            write_line("vamos a comprobar que no haya niguna orden fisica con el order_id de la order_dangling: " + str(order_dangling), silent)
            match_flag = False
            for kk in open_orders_list:
                #print("processing :" + str(kk))
                if order_dangling in kk:
                    write_line("match: " + str(kk), silent)
                    match_flag = True
                    break
                else:
                    #print(".... no match, next")
                    nada = 1
            if not match_flag:
                write_line(".... no existe ninguna orden fisica con el order_id de la order_dangling", silent)
                #write_line(".... seguimos con los siguientos pasos", silent)
            
                write_line("select * from radar_list where order_id_to_close=" + str(order_dangling) + ";", silent)
                sql = "select * from radar_list where order_id_to_close=" + str(order_dangling) + ";"
                entire_row = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error dangling")
                write_line(".... entire_row: " + str(entire_row), silent)

                sql = "select trigger_price_to_put_in_position, original_quantity from radar_list where order_id_to_close=" + str(order_dangling) + ";"
                result = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error dangling")
                write_line(".... trigger_price_to_put_in_position: " + str(result[0]), silent)
                write_line(".... original_quantity: " + str(result[1]), silent)
                write_line(".... .... recrear pivot ATENCION, factor_gain se usara el actual, no el que tenia en radar_list, sino hay que hacer una funcion nueva que setee el que tenia", silent)
                p_price = result[0]
                p_size = result[1]
                write_line("p_price type: " + str(type(p_price)), silent)
                write_line("p_size type: " + str(type(p_size)), silent)
                write_line("update radar_list set order_status='PNL' where order_id_to_close=" + str(order_dangling) + ";", silent)
            else:
                write_line("strange situation, se debe analizar que hacer con este registro", silent)
                write_line("++++++++++++++++++++++++++++++++++++++++++++++++++++++++", silent)
        #if tag in ('insert', 'replace'):
    if extra_current_open_orders_limit_sell_to_close:
        write_line("....", silent)
        write_line("estas limit_sell_order_to_close existen fisicamente como SELL NEW pero no estan en radar_list con status: where order_id_to_close != 0 and order_status = 'IN_POSITION' ", silent)
        write_line("es strange, se deberia hacer un insert, pero se debe analizar", silent)
        #write_line('current_open_orders_limit_sell_to_close has: ' + str(b[k:l]), silent)
        write_line('current_open_orders_limit_sell_to_close has: ' + str(extra_current_open_orders_limit_sell_to_close), silent)
        write_line("vamos a comprobar si existe un row en radar_list where order_id=order_dangling or order_id_to_close=order_dangling", silent)
        #for order_dangling in b[k:l]:
        for order_dangling in extra_current_open_orders_limit_sell_to_close:
            sql = "select * from radar_list where order_id_to_close=" + str(order_dangling) + " or order_id=" + str(order_dangling) + ";"
            write_line("processing sql: " + str(sql), silent)
            result = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error dangling")
            write_line(".... result: " + str(result), silent)
    print("################### check2new end")

def check_dangling_before_starting_websocket(silent):
    flag_dangling = 0
    #radar_list = get_radar_list()
    write_line("", silent)
     

# check 1
#select sum(size) from get_position =  select sum(size) from radar_list where order_id_to_close !="X" and status ='IN_POSITION' 
    write_line("", silent)
    write_line("check 1, position_size_in_radar_list = current_position_size", silent)
    write_line("(el size de la posicion debe ser igual al size en radar_list de las ordenes que estan IN_POSITION y tienen la orden para close seteada)", silent)
    sql = "select ifnull(sum(original_quantity), 0) from radar_list where order_id_to_close != 0 and order_status = 'IN_POSITION'" 
    position_size_in_radar_list = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error dangling check 1")[0]
    write_line("position_size_in_radar_list: " + str(position_size_in_radar_list), silent)
    position_size = get_position_size(silent)
    write_line("current_position_size: " + str(position_size), silent)
    #print("position_size is type: " + str(type(position_size)))
    diff_pos = position_size_in_radar_list - position_size
    write_line("diff pos:" + str(diff_pos), silent)
    if position_size != position_size_in_radar_list:
        write_line("dangling check1 detected, position_size: " + str(position_size), silent)
        flag_dangling = 1
        if position_size > position_size_in_radar_list:
            write_line("radar_list: data faltante2636 - (tiene menos orders IN_POSITION con order de venta creada)", silent)
            write_line("tiene menos orders IN_POSITION con orden de venta creada que la realidad", silent)
            write_line("To fix sell manually size: " + str(diff_pos) + " contracts (ideally with gain)", silent)
        else:
            write_line("RADAR_LIST tiene data sobrante (orders IN_POSITION con order de venta creada)", silent)
            write_line("to fix is necessary to delete from radar_list....no easy to detect what to delete", silent)
    else:
        write_line("dangling check1 ok", silent)


# check 2
#select orderid from open_orders where side="SELL" and status ="NEW" = select orderid_to_close from radar_list where order_id_to_close !="X" and status="IN_POSITION"
# ( las ordenes limit SELL para close deben ser igual a las ordenes para close en radar_list)
    #{'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'web_yyNwXy31MI4athKb5Mu0', 'closePosition': 'False', 'cumBase': '0.0', 'executedQty': '0.0',
    # 'orderId': '6197530906', 'origQty': '1.0', 'origType': 'LIMIT', 'positionSide': 'LONG', 'price': '66.0', 'priceRate': 'None', 'reduceOnly': 'True', 
    # 'side': 'SELL', 'status': 'NEW', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 'timeInForce': 'GTC', 'type': 'LIMIT', 'updateTime': '1651719486872', 'workingType': 'CONTRACT_PRICE'}]
    write_line("", silent)
    write_line("check 2, current_open_orders_limit_sell_to_close = radar_list_open_orders_limit_sell_to_close", silent)
    write_line("ordenes de venta en radar_list debe ser igual a la ordenes de venta current")
    open_orders_list = get_open_orders_dict()
    current_open_orders_limit_sell_to_close = []
    for open_orders_list_dict in open_orders_list:
    # asi se ve una limit sell en open_orders_list
    # open_orders_list   {'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'goto_in_position1653456812156', 
    # 'closePosition': 'False', 'cumBase': '0.0', 'executedQty': '0.0', 'orderId': '6517336318', 'origQty': '1.0', 
    # 'origType': 'LIMIT', 'positionSide': 'LONG', 'price': '0.52274', 'priceRate': 'None', 'reduceOnly': 'True', 
    # 'side': 'SELL', 'status': 'NEW', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 'timeInForce': 'GTC', 'type': 'LIMIT', 
    # 'updateTime': '1653456813337', 'workingType': 'CONTRACT_PRICE'}, 

        side = open_orders_list_dict['side']
        status = open_orders_list_dict['status']
        #print("open_orders_dict side, status:" + str(side) + ", " + str(status))
        if side == "SELL" and status == "NEW":
            print(open_orders_list_dict['orderId'])
            current_open_orders_limit_sell_to_close.append(int(open_orders_list_dict['orderId'])) 
    write_line("current_open_orders_limit_sell_to_close: " + str(sorted(current_open_orders_limit_sell_to_close)), silent)

    sql = "select order_id_to_close from radar_list where order_id_to_close != 0 and order_status = 'IN_POSITION'"
    orders_in_radar_list_list_of_tuples = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error dangling check 2")
    # Python code to convert list of tuples into list using list comprehension
    radar_list_open_orders_limit_sell_to_close = [item for t in orders_in_radar_list_list_of_tuples for item in t]
    write_line("radar_list_open_orders_limit_sell_to_close: " + str(sorted(radar_list_open_orders_limit_sell_to_close)), silent)
    if sorted(radar_list_open_orders_limit_sell_to_close) == sorted(current_open_orders_limit_sell_to_close):
        write_line("dangling check2 ok", silent) 
    else:
        flag_dangling = 1
        write_line("dangling check2 detected, radar_list_open_orders_limit_sell_to_close are not equal to current_open_orders_limit_sell_to_close", silent)

        write_line("len radar_list_open_orders_limit_sell_to_close: " + str(len(radar_list_open_orders_limit_sell_to_close)), silent) 
        write_line("len current_open_orders_limit_sell_to_close: " + str(len(current_open_orders_limit_sell_to_close)), silent) 
        a = sorted(radar_list_open_orders_limit_sell_to_close)
        b = sorted(current_open_orders_limit_sell_to_close)
        check2new(a, b, open_orders_list, silent)
        check2new_2(a, b, open_orders_list, silent)
        ''' 
        for tag, i, j, k, l in SequenceMatcher(None, a, b).get_opcodes():
            if tag == 'equal':
                write_line('both have: ' + str(a[i:j]), silent)
            if tag in ('delete', 'replace'):
                write_line("....", silent)
                write_line("estas order_id_to_close estan en radar_list pero su estado fisico no es SELL NEW", silent)
                write_line("esto significa que se ejecutaron pero no se repitio el pivot y tampoco se hizo update a PNL", silent)
                write_line("debe recrearse el pivot, y update del registro dangling de la base a PNL", silent)
                write_line('radar_list_open_orders_limit_sell_to_close has: ' + str(a[i:j]), silent)
                for order_dangling in a[i:j]:
                    write_line("+", silent)
                    write_line("procesando nueva order_dangling", silent)
                    write_line("vamos a comprobar que no haya niguna orden fisica con el order_id de la order_dangling: " + str(order_dangling), silent)
                    match_flag = False
                    for kk in open_orders_list:
                        #print("processing :" + str(kk))
                        if order_dangling in kk:
                            write_line("match: " + str(kk), silent)
                            match_flag = True
                            break
                        else:
                            #print(".... no match, next")
                            nada = 1
                    if not match_flag:
                        write_line(".... no existe ninguna orden fisica con el order_id de la order_dangling", silent)
                        write_line(".... seguimos con los siguientos pasos", silent)
                
                        write_line("select * from radar_list where order_id_to_close=" + str(order_dangling) + ";", silent)
                        sql = "select * from radar_list where order_id_to_close=" + str(order_dangling) + ";"
                        entire_row = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error dangling")
                        write_line(".... entire_row: " + str(entire_row), silent)

                        sql = "select trigger_price_to_put_in_position, original_quantity from radar_list where order_id_to_close=" + str(order_dangling) + ";"
                        result = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error dangling")
                        write_line(".... trigger_price_to_put_in_position: " + str(result[0]), silent)
                        write_line(".... original_quantity: " + str(result[1]), silent)
                        write_line(".... .... recrear pivot ATENCION, factor_gain se usara el actual, no el que tenia en radar_list, sino hay que hacer una funcion nueva que setee el que tenia", silent)
                        p_price = result[0]
                        p_size = result[1]
                        write_line("p_price type: " + str(type(p_price)), silent)
                        write_line("p_size type: " + str(type(p_size)), silent)
                        write_line("update radar_list set order_status='PNL' where order_id_to_close=" + str(order_dangling) + ";", silent)
                    else:
                        write_line("strange situation, se debe analizar que hacer con este registro", silent)
                        write_line("++++++++++++++++++++++++++++++++++++++++++++++++++++++++", silent)
            if tag in ('insert', 'replace'):
                write_line("....", silent)
                write_line("estas limit_sell_order_to_close existen fisicamente como SELL NEW pero no estan en radar_list con status: where order_id_to_close != 0 and order_status = 'IN_POSITION' ", silent)
                write_line("es strange, se deberia hacer un insert, pero se debe analizar", silent)
                write_line('current_open_orders_limit_sell_to_close has: ' + str(b[k:l]), silent)
                write_line("vamos a comprobar si existe un row en radar_list where order_id=order_dangling or order_id_to_close=order_dangling", silent)
                for order_dangling in b[k:l]:
                    sql = "select * from radar_list where order_id_to_close=" + str(order_dangling) + " or order_id=" + str(order_dangling) + ";"
                    write_line("processing sql: " + str(sql), silent)
                    result = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error dangling")
                    write_line(".... result: " + str(result), silent)
        '''         


            
###########


# check 3
#select orderid from open_orders where side="BUY" and status ="NEW" = select orderid from radar_list where status="NEW" and order_id_to_close=0" 
# ( las ordenes limit BUY para poner en posicion deben ser iguales a las ordenes en NEW en radar_list y que aun no tengan una orden de close seteada en radar_list)
    ### check 3
    write_line("", silent)
    #write_line("check 3, orders in radar_list waiting for position = current orders waiting for position", silent)
    write_line("check 3, current open orders BUY NEW = radar_list BUY NEW (new_pivot) order_id_to_close=0", silent)
    open_orders_list = get_open_orders_dict()
    open_orders_waiting_for_position = []
    for open_orders_list_dict in open_orders_list:
        side = open_orders_list_dict['side']
        status = open_orders_list_dict['status']
        clientorderid = open_orders_list_dict['clientOrderId']
        #print("open_orders_dict side, status:" + str(side) + ", " + str(status))
        
        # asi se ve una fakeorder
        # my_list: [{'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'fakeorder', 'closePosition': 'False', 'cumBase': '0.0', 
        # 'executedQty': '0.0', 'orderId': '6519186579', 'origQty': '1.0', 'origType': 'LIMIT', 'positionSide': 'LONG', 'price': '0.1', 
        # 'priceRate': 'None', 'reduceOnly': 'False', 'side': 'BUY', 'status': 'NEW', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 
        # 'timeInForce': 'GTC', 'type': 'LIMIT', 'updateTime': '1653470102496', 'workingType': 'CONTRACT_PRICE'},
        if side == "BUY" and status == "NEW" and "fakeorder" not in clientorderid:
            open_orders_waiting_for_position.append(int(open_orders_list_dict['orderId'])) 
    write_line("current open_orders_waiting_for_position: " + str(sorted(open_orders_waiting_for_position)), silent)

    sql = "select order_id from radar_list where order_status = 'NEW' and order_id_to_close = 0"
    orders_in_radar_list_list_of_tuples = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error dangling check 3")
    # Python code to convert list of tuples into list using list comprehension
    orders_in_radar_list = [item for t in orders_in_radar_list_list_of_tuples for item in t]
    #print("orders_in_radar_list_list_of_tuples: " + str(orders_in_radar_list_list_of_tuples))
    #print("converted to list of elements" + str(orders_in_radar_list))
    write_line("orders in radar_list waiting for position: " + str(sorted(orders_in_radar_list)), silent)
    if sorted(orders_in_radar_list) == sorted(open_orders_waiting_for_position):
        write_line("dangling check3 ok", silent) 
    else:
        flag_dangling = 1
        write_line("dangling check3 detected, orders in radar_list waiting for position are not equal to existing orders waiting for position", silent)
        write_line("len orders_in_radar_list wating for position: " + str(len(orders_in_radar_list)), silent) 
        write_line("len  open_orders_waiting_for_position: " + str(len(open_orders_waiting_for_position)), silent) 
        a = sorted(orders_in_radar_list)
        b = sorted(open_orders_waiting_for_position)
        check3new(a, b, open_orders_list, silent)
       
        ''' 
        for tag, i, j, k, l in SequenceMatcher(None, a, b).get_opcodes():
            if tag == 'equal':
                write_line('both have: ' + str(a[i:j]), silent)
            if tag in ('delete', 'replace'):
                write_line("estas order_id estan en radar_list pero su estado fisico no es BUY NEW and != fakeorder ", silent)
                write_line("esto significa que las ordenes se crearon, pero no se hizo update a IN_POSITION", silent)
                write_line('  orders_in_radar_list has: ' + str(a[i:j]), silent)
                for order_dangling in a[i:j]:
                    write_line("+", silent)
                    write_line("procesando nueva order_dangling", silent)
                    write_line("vamos a comprobar que no haya niguna orden fisica con el order_id de la order_dangling: " + str(order_dangling), silent)
                    match_flag = False
                    for kk in open_orders_list:
                        #print("processing :" + str(kk))
                        if order_dangling in kk:
                            write_line("match: " + str(kk), silent)
                            match_flag = True
                            break
                        else:
                            #print(".... no match, next")
                            nada = 1
                    if not match_flag:
                        write_line(".... no existe ninguna orden fisica con el order_id de la order_dangling", silent)
                        write_line(".... seguimos con los siguientos pasos", silent)
                        write_line("podemos borrar el row de la db", silent)
                        write_line("select * from radar_list where order_id=" + str(order_dangling) + ";", silent)
                        write_line("delete from radar_list where order_id=" + str(order_dangling) + ";", silent)
                    else:
                        write_line("strange situation, se debe analizar que hacer con este registro", silent)
                        write_line("++++++++++++++++++++++++++++++++++++++++++++++++++++++++", silent)
            if tag in ('insert', 'replace'):
                write_line("estas order_id estan existen fisicamente como side == BUY and status == NEW and clientorderid != fakeorder , ", silent)
                write_line("pero no estan en radar_list con status: where order_status = 'NEW' and order_id_to_close = 0", silent)
                write_line("es strange, se debe analizar", silent)
                write_line(' open_orders_waiting_for_position has: ' + str(b[k:l]), silent)
                write_line("vamos a comprobar si existe un row en radar_list where order_id=order_dangling or order_id_to_close=order_dangling", silent)
                for order_dangling in b[k:l]:
                    sql = "select * from radar_list where order_id_to_close=" + str(order_dangling) + " or order_id=" + str(order_dangling) + ";"
                    write_line("processing sql: " + str(sql), silent)
                    result = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error dangling")
                    write_line(".... result: " + str(result), silent)
        '''
    return flag_dangling


def check3new(radar, current, open_orders_list, silent):
  #  a = sorted(orders_in_radar_list)
  #  b = sorted(open_orders_waiting_for_position)
    nada = 1
    write_line("################### check3new begin", silent)
    extra_orders_in_radar_list = [ i for i in radar if i not in current ]
    extra_open_orders_waiting_for_position = [ i for i in current if i not in radar ]
    #for tag, i, j, k, l in SequenceMatcher(None, a, b).get_opcodes():
        #if tag in ('delete', 'replace'):
        #if tag in ('delete', 'replace'):
    if extra_orders_in_radar_list:
        write_line("estas order_id estan en radar_list pero su estado fisico no es BUY NEW and != fakeorder ", silent)
        write_line("esto significa que estas orders BUY se fillearon, entraron a posicion pero no se hizo el update en radar_list a IN_POSITION y no se hizo tampoco la orden de venta", silent)
        #write_line('  orders_in_radar_list has: ' + str(a[i:j]), silent)
        write_line('  orders_in_radar_list has: ' + str(extra_orders_in_radar_list), silent)
        #for order_dangling in a[i:j]:
        for order_dangling in extra_orders_in_radar_list:
            write_line("+", silent)
            write_line("procesando nueva order_dangling", silent)
            write_line("vamos a comprobar que no haya niguna orden fisica con el order_id de la order_dangling: " + str(order_dangling), silent)
            match_flag = False
            for kk in open_orders_list:
                #print("processing :" + str(kk))
                if order_dangling in kk:
                    write_line("match: " + str(kk), silent)
                    match_flag = True
                    break
                else:
                    #print(".... no match, next")
                    nada = 1
            if not match_flag:
                write_line(".... no existe ninguna orden fisica con el order_id de la order_dangling", silent)
                #write_line(".... seguimos con los siguientos pasos", silent)
                write_line("podemos borrar el row de la db o ver en trade history cuando entro a posicion, generar la orden de venta, y update en radar_list accordingly", silent)
                write_line("select * from radar_list where order_id=" + str(order_dangling) + ";", silent)
                write_line("delete from radar_list where order_id=" + str(order_dangling) + ";", silent)
            else:
                write_line("strange situation, se debe analizar que hacer con este registro", silent)
                write_line("++++++++++++++++++++++++++++++++++++++++++++++++++++++++", silent)
    #if tag in ('insert', 'replace'):
    if  extra_open_orders_waiting_for_position :
        write_line("estas order_id estan existen fisicamente como side == BUY and status == NEW and clientorderid != fakeorder , ", silent)
        write_line("pero no estan en radar_list con status: where order_status = 'NEW' and order_id_to_close = 0", silent)
        write_line("es strange, se debe analizar", silent)
        #write_line(' open_orders_waiting_for_position has: ' + str(b[k:l]), silent)
        write_line(' open_orders_waiting_for_position has: ' + str(extra_open_orders_waiting_for_position), silent)
        write_line("vamos a comprobar si existe un row en radar_list where order_id=order_dangling or order_id_to_close=order_dangling", silent)
        #for order_dangling in b[k:l]:
        for order_dangling in extra_open_orders_waiting_for_position:
            sql = "select * from radar_list where order_id_to_close=" + str(order_dangling) + " or order_id=" + str(order_dangling) + ";"
            write_line("processing sql: " + str(sql), silent)
            result = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error dangling")
            write_line(".... result: " + str(result), silent)
    write_line("################### check3new end", silent)