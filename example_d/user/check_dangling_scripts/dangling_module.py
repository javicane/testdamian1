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
from binance_d.example_d.user.common_scripts.get_order_status_module import get_order_status

from binance_d.general_settings import adaperp_decimals

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
            write_line("--------------- in get_position_size, detected current ADAUSD_PERP position_size: " + str(float(position_size)), silent)
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

def check2new(radar, current, open_orders_list, silent):
#      a = sorted(radar_list_open_orders_limit_sell_to_close)
#        b = sorted(current_open_orders_limit_sell_to_close)
    write_line("################### check2new begin", silent)
    order_id_partially_filled_check2 = 0
    flag_partially_filled_local = 0
    flag_expired_local = 0
    flag_possible_database_locked = 0
    nada = 1
    extra_radar_list_open_orders_limit_sell_to_close = [ i for i in radar if i not in current ]
    extra_current_open_orders_limit_sell_to_close = [ i for i in current if i not in radar ]
    if extra_radar_list_open_orders_limit_sell_to_close:
        write_line("....", silent)
        write_line("estas order_id_to_close existen en radar_list pero no existen fisicamente las ordenes venta SELL NEW", silent)
        write_line("significa que fueron filleadas pero no se repitio el pivot y tampoco se hizo update a PNL", silent)
        write_line("debe recrearse el pivot, y update del registro dangling de la base a PNL", silent)
        write_line("Tambien puede ser posible partially filled sell order or expired, check this", silent)
        #write_line('radar_list_open_orders_limit_sell_to_close has: ' + str(a[i:j]), silent)
        write_line('radar_list_open_orders_limit_sell_to_close has: ' + str(extra_radar_list_open_orders_limit_sell_to_close), silent)
        write_line('delete from radar_list where order_id_to_close in ' + str(extra_radar_list_open_orders_limit_sell_to_close).replace("[","").replace("]","") + ';', silent)
        #for order_dangling in a[i:j]:
        for order_dangling in extra_radar_list_open_orders_limit_sell_to_close:
            write_line("+", silent)
            write_line("procesando nueva order_dangling", silent)
            write_line("check if la order esta en partially filled or expired status", silent)
            output_dict = get_order_status(order_dangling)

            write_line("....output_dict['status']: " + str(output_dict['status']), silent)
            #if output_dict['status'] != "FILLED" and output_dict['status'] != "EXPIRED" and output_dict['status'] != 'CANCELED':
            if output_dict['status'] == "PARTIALLY_FILLED":
                flag_partially_filled_local = 1
                order_id_partially_filled_check2 = order_dangling 
                write_line("....detected partially filled", silent)
            elif output_dict['status'] == "EXPIRED":
                write_line("....detected expired", silent)
                flag_expired_local  = 1
            else:
                write_line(".... no partially filled or expired detected", silent)
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
        flag_possible_database_locked = 1
        write_line("....", silent)
        write_line("Possible database locked !!! tratar de hacer un IUD en la db, si esta locked restartear fronted...", silent)
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
    write_line("################### check2new end", silent)
    return flag_partially_filled_local, flag_expired_local, order_id_partially_filled_check2, flag_possible_database_locked

def check_dangling_before_starting_websocket(silent):
    flag_dangling_check1 = 0
    flag_dangling_check2 = 0
    flag_dangling_check3 = 0
    flag_dangling_check4 = 0
    flag_dangling = 0
    flag_partially_filled = 0
    flag_expired = 0
    result_dangling_check1 = ""
    result_dangling_check4 = ""
    order_id_partially_filled_check2 = 0
    buy_partially_filled_order_id_check3 = 0
    flag_possible_database_locked = 0
    #radar_list = get_radar_list()
    write_line("", silent)
     

# check 1
#select sum(size) from get_position =  select sum(size) from radar_list where order_id_to_close !="X" and status ='IN_POSITION' 
    write_line("", silent)
    write_line("check 1, position_size_in_radar_list = current_position_size", silent)
    write_line("(el size de la posicion debe ser igual al size en radar_list de las ordenes que estan IN_POSITION y tienen la orden para close seteada)", silent)
    cantidad_orders_sobrantes_radar_list_check1 = 0
    cantidad_orders_faltantes_radar_list_check1 = 0 
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
        flag_dangling_check1 = 1
        if position_size > position_size_in_radar_list:
            write_line("data faltante | radar_list( sum(size IN_POSITION) ) < sum(size current SELL)", silent)
            #write_line("Possible buy partially_filled, check this", silent)
            write_line("falta registrar algunas current orders SELL en radar_list", silent)
            write_line("posibles causas:", silent)
            write_line("1 - hay orders SELL en radar_list que tienen diferente tamaño que su current (esto lo detecha el check4)", silent)
            write_line("2 - hay buy partially_filled (esto lo detecha check4)", silent)
            write_line("3 - se cocinaron datos (borrado de rows en radar_list) y simplemente hay que hacer SELL orders por la diferencia detectada", silent)
            #write_line("To fix sell manually size: " + str(diff_pos) + " contracts (ideally with gain)", silent)
            #write_line("and cancel the buy partially_filled order_id and delete the row in radar_list", silent)
            #write_line(", or wait until BUY partially_filled have been completed", silent)
            result_dangling_check1 = "posibles causas:"
            result_dangling_check1 += "1 - hay orders SELL en radar_list que tienen diferente tamaño que su current (esto lo detecha el check4) | "
            result_dangling_check1 += "2 - hay buy partially_filled (esto lo detecha check4) | "
            result_dangling_check1 += "3 - se cocinaron datos (borrado de rows en radar_list) y simplemente hay que hacer SELL orders por la diferencia detectada"
            result_dangling_check1 += "4 - se crearon pivots manualmente en modo TAKER y hay desincronizacion"
            result_dangling_check1 += "diferencia detectada: " + str(diff_pos)
            cantidad_orders_faltantes_radar_list_check1 = abs(diff_pos)
        else:
            write_line("data sobrante | (sum(size) orders IN_POSITION > sum(size) orders SELL creadas)", silent)
            write_line("sobran orders IN_POSITION en radar_list respecto de orders BUY current", silent)
            write_line("posibles causas:", silent) 
            write_line("1 - hay sell partially filled or expired", silent) 
            write_line("2 - se cocinaron datos y to fix is necessary to delete from radar_list....no easy to detect what to delete", silent)
            #write_line("to fix is necessary to delete from radar_list....no easy to detect what to delete", silent)
            result_dangling_check1 = "posibles causas:" 
            result_dangling_check1 += "1 - hay sell partially filled or expired | "
            result_dangling_check1 += "2 - se cocinaron datos y to fix is necessary to delete from radar_list....no easy to detect what to delete"
            cantidad_orders_sobrantes_radar_list_check1 = abs(diff_pos) 
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
    write_line("ordenes de venta en radar_list debe ser igual a la ordenes de venta current", silent)
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
        flag_dangling_check2 = 1
        write_line("dangling check2 detected, radar_list_open_orders_limit_sell_to_close are not equal to current_open_orders_limit_sell_to_close", silent)

        write_line("len radar_list_open_orders_limit_sell_to_close: " + str(len(radar_list_open_orders_limit_sell_to_close)), silent) 
        write_line("len current_open_orders_limit_sell_to_close: " + str(len(current_open_orders_limit_sell_to_close)), silent) 
        a = sorted(radar_list_open_orders_limit_sell_to_close)
        b = sorted(current_open_orders_limit_sell_to_close)
        flag_partially_filled, flag_expired, order_id_partially_filled_check2, flag_possible_database_locked = check2new(a, b, open_orders_list, silent)
            
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
        flag_dangling_check3 = 1
        write_line("dangling check3 detected, orders in radar_list waiting for position are not equal to existing orders waiting for position", silent)
        write_line("len orders_in_radar_list wating for position: " + str(len(orders_in_radar_list)), silent) 
        write_line("len  open_orders_waiting_for_position: " + str(len(open_orders_waiting_for_position)), silent) 
        a = sorted(orders_in_radar_list)
        b = sorted(open_orders_waiting_for_position)
        flag_partially_filled, buy_partially_filled_order_id_check3 = check3new(a, b, open_orders_list, silent)
       
    #print("flag_partially_filled:", flag_partially_filled)
    flag_dangling_check1_only = 0
    if flag_dangling_check1 == 1 and ( flag_dangling_check2 == 0 and flag_dangling_check3 == 0):
        flag_dangling_check1_only = 1


    # check 4 check drift in original_quantity in radar_list     
    buy_partially_filled_price_check4, sell_partially_filled_price_check4, result_dangling_check4, flag_dangling_check4, sell_partially_filled_order_id_check4, sell_partially_filled_executed_quantity_check4, buy_partially_filled_order_id_check4, buy_partially_filled_executed_quantity_check4 = check4(silent) 
    detect_sell_partially_filled_flag = detect_sell_partially_filled(silent, cantidad_orders_sobrantes_radar_list_check1, order_id_partially_filled_check2, sell_partially_filled_order_id_check4, sell_partially_filled_executed_quantity_check4)
    detect_buy_partially_filled_flag = detect_buy_partially_filled(silent, cantidad_orders_faltantes_radar_list_check1, buy_partially_filled_order_id_check3, buy_partially_filled_order_id_check4, buy_partially_filled_executed_quantity_check4)
    if detect_buy_partially_filled_flag == 1:
       
       sql = "select trigger_price_to_close from radar_list where order_id=" + str(buy_partially_filled_order_id_check3) + ";"
       trigger_price_to_close = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error sql buy_partially_filled")[0]
       result_dangling_check1 += " | TRUE  ( match check3 & check4 )\n" 
       fix_step = "| fix_steps: cancel order_id: " + str(buy_partially_filled_order_id_check3) + ";\n"
       fix_step += "delete from radar_list where order_id=" + str(buy_partially_filled_order_id_check3) + ";\n"
       fix_step += "create sell order ( tpc >= "
       fix_step += str(trigger_price_to_close) + ", size: " + str(int(float(buy_partially_filled_executed_quantity_check4))) + ");\n"
       fix_step += "repeat original deleted pivot with tpp: " + result_dangling_check4
       fix_step += " and tc:" + str(trigger_price_to_close) 
       #print(trigger_price_to_close)
       print(fix_step)
       result_dangling_check1 += fix_step
    return flag_dangling, flag_partially_filled, flag_expired, flag_dangling_check1_only, result_dangling_check1, flag_dangling_check2, flag_dangling_check3, flag_dangling_check4, result_dangling_check4, flag_possible_database_locked

def detect_buy_partially_filled(silent, cantidad_orders_faltantes_radar_list_check1, buy_partially_filled_order_id_check3, buy_partially_filled_order_id_check4, buy_partially_filled_executed_quantity_check4):
    #print("type buy_partially_filled_order_id_check3", type(buy_partially_filled_order_id_check3)) int
    #print("type buy_partially_filled_order_id_check4", type(buy_partially_filled_order_id_check4)) str
    detect_buy_partially_filled_flag = 0
    if ( int(cantidad_orders_faltantes_radar_list_check1) > 0 ) and \
       ( int(buy_partially_filled_order_id_check3) != 0 ) and \
       ( int(buy_partially_filled_order_id_check4) != 0 ) and \
       ( int(buy_partially_filled_order_id_check3) == int(buy_partially_filled_order_id_check4) ) and \
       ( float(cantidad_orders_faltantes_radar_list_check1) == float(buy_partially_filled_executed_quantity_check4) ):
        #print("detect_buy_partially_filled TRUE with details")
        write_line("detect_buy_partially_filled TRUE with details", silent)
        detect_buy_partially_filled_flag = 1
    return detect_buy_partially_filled_flag

        
def detect_sell_partially_filled(silent, cantidad_orders_sobrantes_radar_list_check1, order_id_partially_filled_check2, sell_partially_filled_order_id_check4, sell_partially_filled_executed_quantity_check4):
    detect_sell_partially_filled_flag= 0
    if ( int(cantidad_orders_sobrantes_radar_list_check1) > 0 ) and \
       ( int(order_id_partially_filled_check2) != 0 ) and \
       ( int(sell_partially_filled_order_id_check4) != 0 ) and \
       ( int(order_id_partially_filled_check2) == int(sell_partially_filled_order_id_check4) ) and \
       ( float(cantidad_orders_sobrantes_radar_list_check1) == float(sell_partially_filled_executed_quantity_check4) ):
        #print("detect_sell_partially_filled TRUE with details")
        write_line("detect_sell_partially_filled TRUE with details", silent)
        detect_sell_partially_filled_flag = 1
    return detect_sell_partially_filled_flag

def check4(silent):
    sell_partially_filled_order_id_check4 = 0
    sell_partially_filled_executed_quantity_check4 = 0
    buy_partially_filled_order_id_check4 = 0
    buy_partially_filled_executed_quantity_check4 = 0
    buy_partially_filled_price_check4 = 0
    sell_partially_filled_price_check4 = 0
    result_dangling_check4 = ""
    flag_dangling_check4 = 0
    write_line("check4", silent)
    sql = "select order_id, original_quantity from radar_list where order_status = 'NEW' and order_id_to_close = 0"
    orders_in_radar_list_list_of_tuples = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error dangling check 3")
    #print("orders_in_radar_list_list_of_tuples", orders_in_radar_list_list_of_tuples)
    # Python code to convert list of tuples into list using list comprehension
    orders_in_radar_list_buy_dict = {}
    for item_tuple in orders_in_radar_list_list_of_tuples:
        my_key = str(item_tuple[0])
        orders_in_radar_list_buy_dict[my_key] = item_tuple[1] 
    write_line("orders_in_radar_list_buy_dict:" + str(orders_in_radar_list_buy_dict), silent)
    write_line("", silent)

    sql = "select order_id_to_close, original_quantity from radar_list where order_status = 'IN_POSITION' and order_id_to_close != 0"
    orders_in_radar_list_list_of_tuples = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error dangling check 3")
    # Python code to convert list of tuples into list using list comprehension
    orders_in_radar_list_sell_dict = {}
    for item_tuple in orders_in_radar_list_list_of_tuples:
        #my_dict = dict(order_id=item_tuple[0], size=item_tuple[1])
        my_key = str(item_tuple[0])
        orders_in_radar_list_sell_dict[my_key] = item_tuple[1] 
    write_line("orders_in_radar_list_sell_dict:" + str(orders_in_radar_list_sell_dict), silent)

    
    
    open_orders_list = get_open_orders_dict()
   # current_open_orders_limit_sell_to_close = []
    total_sell_current = 0
    dangling = 0
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
        #print("")
        if side == "SELL" and status == "NEW":
            total_sell_current = total_sell_current + round(float(open_orders_list_dict['origQty']))
            #print("SELL orderid, size", open_orders_list_dict['orderId'], open_orders_list_dict['origQty'] )
            order_id_current = open_orders_list_dict['orderId']
            if order_id_current in orders_in_radar_list_sell_dict.keys():
                #print(".... exists in radar_list")
                #print(".... in radar_list size", orders_in_radar_list_sell_dict[str(order_id_current)])
                size_in_radar_list = round(float(orders_in_radar_list_sell_dict[str(order_id_current)]))
                size_current = round(float(open_orders_list_dict['origQty']))
                #print(".... .... size_current", size_current)
                #print(".... .... size_in_radar_list", size_in_radar_list)
                if size_in_radar_list == size_current:
                    nada = 1
                    #print(".... .... .... no drift in size")
                    #write_line(".... .... .... no drift in size", silent)
                else:
                    #print("SELL orderid, size", open_orders_list_dict['orderId'], open_orders_list_dict['origQty'] )
                    write_line("SELL orderid, size: " + str(open_orders_list_dict['orderId']) + ", " + str(open_orders_list_dict['origQty'] ), silent)
                    size_in_radar_list = round(float(orders_in_radar_list_sell_dict[str(order_id_current)]))
                    size_current = round(float(open_orders_list_dict['origQty']))
                    dangling = 1
                    #print("DRIFT", silent)
                    write_line("DRIFT", silent)
            else:
                #print("SELL orderid, size", open_orders_list_dict['orderId'], open_orders_list_dict['origQty'] )
                write_line("SELL orderid, size: " + str(open_orders_list_dict['orderId']) + ", " + str(open_orders_list_dict['origQty'] ), silent)
                dangling = 1
                write_line(".... Not exists in radar_list !!!! !!!! !!!!", silent)
                #print(".... Not exists in radar_list !!!! !!!! !!!!", silent)
        elif side == "BUY" and status == "NEW":
            #print("BUY orderid, size", open_orders_list_dict['orderId'], open_orders_list_dict['origQty'] )
            order_id_current = open_orders_list_dict['orderId']
            if order_id_current in orders_in_radar_list_buy_dict.keys():
                #print(".... exists")
                #print(".... in radar_list size", orders_in_radar_list_buy_dict[str(order_id_current)])
                size_in_radar_list = round(float(orders_in_radar_list_buy_dict[str(order_id_current)]))
                size_current = round(float(open_orders_list_dict['origQty']))
                #print(".... .... size_current", size_current)
                #print(".... .... size_in_radar_list", size_in_radar_list)
                if size_in_radar_list == size_current:
                    #print(".... .... .... no drift")
                    nada = 1
                else:
                    #print("BUY orderid, size", open_orders_list_dict['orderId'], open_orders_list_dict['origQty'] )
                    write_line("BUY orderid, size: " + str(open_orders_list_dict['orderId']) + ", " + str(open_orders_list_dict['origQty'] ), silent)
                    dangling = 1
                    write_line("DRIFT !!!", silent) 
                    #print("DRIFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFT")
            else:
                #print("BUY orderid, size", open_orders_list_dict['orderId'], open_orders_list_dict['origQty'] )
                write_line("BUY orderid, size: " + str(open_orders_list_dict['orderId']) + ", " + str(open_orders_list_dict['origQty'] ), silent)
                dangling = 1
                write_line(".... Not exists in radar_list !!!! !!!! !!!!", silent)
        else:
            #print("side extraño:", side, status)
            write_line("side extraño:" + str(side) + "," + str(status), silent)
            dangling = 1
            write_line(open_orders_list_dict, silent)
             
            result_dangling_check4 = str(side) + "," + str(status)
            if status == 'PARTIALLY_FILLED':
                executed_quantity = open_orders_list_dict['executedQty']
                order_id_partially_filled = open_orders_list_dict['orderId']
                price = open_orders_list_dict['price']
                result_dangling_check4 = str(side) + "," + str(status) + ", order_id:" + str(order_id_partially_filled) + ", exctdQty:" + str(executed_quantity) + ", price:" + str(price)
                if side == "SELL":
                    sell_partially_filled_price_check4 = price 
                    sell_partially_filled_order_id_check4 = order_id_partially_filled
                    sell_partially_filled_executed_quantity_check4 = executed_quantity
                elif side == "BUY":
                    #side extraño:BUY,PARTIALLY_FILLED
                    #open_orders_list_dict = {'activatePrice': 'None', 'avgPrice': '0.47207', 'clientOrderId': 'new_pivot1663371778003', 
                    # 'closePosition': 'False', 'cumBase': '190.64969178', 'executedQty': '9.0', 'orderId': '7554245184', 
                    # 'origQty': '10.0', 'origType': 'LIMIT', 'positionSide': 'LONG', 'price': '0.47207', 'priceRate': 'None', 
                    # 'reduceOnly': 'False', 'side': 'BUY', 'status': 'PARTIALLY_FILLED', 'stopPrice': '0.0', 
                    # 'symbol': 'ADAUSD_PERP', 'timeInForce': 'GTC', 'type': 'LIMIT', 'updateTime': '1663373850306', 
                    # 'workingType': 'CONTRACT_PRICE'}
                    buy_partially_filled_price_check4 = price 
                    buy_partially_filled_order_id_check4 = order_id_partially_filled
                    buy_partially_filled_executed_quantity_check4 = executed_quantity

    #print("total_sell_current", total_sell_current)
    if dangling == 1:
        write_line("check4 dangling detected", silent)
        flag_dangling_check4 = 1
    elif dangling == 0:
        write_line("dangling check4 OK", silent)
    return buy_partially_filled_price_check4, sell_partially_filled_price_check4, result_dangling_check4, flag_dangling_check4, sell_partially_filled_order_id_check4, sell_partially_filled_executed_quantity_check4, buy_partially_filled_order_id_check4, buy_partially_filled_executed_quantity_check4 

def check3new(radar, current, open_orders_list, silent):
    buy_partially_filled_order_id_check3 = 0
  #  a = sorted(orders_in_radar_list)
  #  b = sorted(open_orders_waiting_for_position)
    flag_partially_filled_local = 0
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
        write_line("Posible partially filled buy order", silent)
        #write_line('  orders_in_radar_list has: ' + str(a[i:j]), silent)
        write_line('  orders_in_radar_list has: ' + str(extra_orders_in_radar_list), silent)
        #for order_dangling in a[i:j]:
        for order_dangling in extra_orders_in_radar_list:
            write_line("+", silent)
            write_line("procesando nueva order_dangling", silent)
            write_line("check if la order esta en partially filled status", silent)
            output_dict = get_order_status(order_dangling)

            write_line("....output_dict['status']: " + str(output_dict['status']), silent)
            if output_dict['status'] != "FILLED" and output_dict['status'] != 'CANCELED':
                write_line("....detected partially filled", silent)
                flag_partially_filled_local = 1
                buy_partially_filled_order_id_check3 = order_dangling
            else:
                write_line(".... no partially filled detected", silent)
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
    return flag_partially_filled_local, buy_partially_filled_order_id_check3