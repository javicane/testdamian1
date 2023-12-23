import sys
sys.path.append("C:/binance/futures/futures")
from binance_d import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, funcname, get_radar_list
from binance_d.example_d.user.helpers_scripts.sql import exec_sql

def get_position_size(): 
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
            print("i dict: " + str(i))
            print("---------------ADA position_size: " + str(float(position_size)))
            break
        else:
            #print("symbol: " + i['symbol'])
            nada = 1
    print("in " + funcname() + ", return position_size: " + str(position_size))
    return int(round(float(position_size),0))

def get_open_orders_dict():
    '''
    returns:
        my_list: list, list of dicts
    '''
    #input("in " + funcname() + ",pec 1")
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
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

def check_dangling_before_starting_websocket():
    #input("in " + funcname() + ", pec")

    open_orders_list = get_open_orders_dict()
 
    print("")
    print("after get_open_orders_dict")
     
    print("in: " + funcname() + ", open_orders_list: " + str(open_orders_list)) 
    print("")
    position_size = get_position_size()
    print("in: " + funcname() + ", position_size: " + str(position_size))
    print("")
    radar_list = get_radar_list()
    print("in: " + funcname() + ", radar_list: " + str(radar_list))    
    print("")
     
    #sys.exit(66)

    print("")
    print("check 1, position_size_in_radar_list = current_position_size")
# check 1
#select sum(size) from get_position =  select sum(size) from radar_list where order_id_to_close !="X" and status ='IN_POSITION' 
#(el size de la posicion es igual al size en radar_list de las ordenes que estan IN_POSITION y tienen la orden para close seteada)
    sql = "select ifnull(sum(original_quantity), 0) from radar_list where order_id_to_close != 0 and order_status = 'IN_POSITION'" 
    position_size_in_radar_list = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error dangling check 1")[0]
    print("position_size_in_radar_list: " + str(position_size_in_radar_list))
    print("current_position_size: " + str(position_size))
    #print("position_size is type: " + str(type(position_size)))
    diff_pos = position_size_in_radar_list - position_size
    print("diff pos:" + str(diff_pos))
    if position_size != position_size_in_radar_list:
        print("dangling check1 detected, position_size: " + str(position_size))
    else:
        print("dangling check1 ok")
    print("")
    print("check 2, current open_orders_limit_sell_to_close = order_id_to_close in radar_list")
# check 2
#select orderid from open_orders where side="SELL" and status ="NEW" = select orderid_to_close from radar_list where order_id_to_close !="X" and status="IN_POSITION"
# ( las ordenes limit SELL para close deben ser igual a las ordenes para close en radar_list)
    #{'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'web_yyNwXy31MI4athKb5Mu0', 'closePosition': 'False', 'cumBase': '0.0', 'executedQty': '0.0',
    # 'orderId': '6197530906', 'origQty': '1.0', 'origType': 'LIMIT', 'positionSide': 'LONG', 'price': '66.0', 'priceRate': 'None', 'reduceOnly': 'True', 
    # 'side': 'SELL', 'status': 'NEW', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 'timeInForce': 'GTC', 'type': 'LIMIT', 'updateTime': '1651719486872', 'workingType': 'CONTRACT_PRICE'}]
    open_orders_limit_sell_to_close = []
    for open_orders_list_dict in open_orders_list:
        side = open_orders_list_dict['side']
        status = open_orders_list_dict['status']
        #print("open_orders_dict side, status:" + str(side) + ", " + str(status))
        if side == "SELL" and status == "NEW":
            open_orders_limit_sell_to_close.append(int(open_orders_list_dict['orderId'])) 
    print("current open_orders_limit_sell_to_close: ", open_orders_limit_sell_to_close)

    sql = "select order_id_to_close from radar_list where order_id_to_close != 0 and order_status = 'IN_POSITION'"
    orders_in_radar_list_list_of_tuples = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error dangling check 2")
    # Python code to convert list of tuples into list using list comprehension
    orders_in_radar_list = [item for t in orders_in_radar_list_list_of_tuples for item in t]
    #print("orders_in_radar_list_list_of_tuples: " + str(orders_in_radar_list_list_of_tuples))
    #print("converted to list of elements" + str(orders_in_radar_list))
    print("order_id_to_close in radar_list:" + str(orders_in_radar_list))
    if sorted(orders_in_radar_list) == sorted(open_orders_limit_sell_to_close):
        print("dangling check2 ok") 
    else:
        print("dangling check2 detected, orders in radar_list with order_id_close are not equal to existing open orders to close")
    print("")
    print("check 3, orders in radar_list waiting for position = current orders waiting for position")
# check 3
#select orderid from open_orders where side="BUY" and status ="NEW" = select orderid from radar_list where status="NEW" and order_id_to_close=0" 
# ( las ordenes limit BUY para poner en posicion deben ser iguales a las ordenes en NEW en radar_list y que aun no tengan una orden de close seteada en radar_list)
    open_orders_waiting_for_position = []
    for open_orders_list_dict in open_orders_list:
        side = open_orders_list_dict['side']
        status = open_orders_list_dict['status']
        #print("open_orders_dict side, status:" + str(side) + ", " + str(status))
        if side == "BUY" and status == "NEW":
            open_orders_waiting_for_position.append(int(open_orders_list_dict['orderId'])) 
    print("current open_orders_waiting_for_position: ", open_orders_waiting_for_position)        

    sql = "select order_id from radar_list where order_status = 'NEW' and order_id_to_close = 0"
    orders_in_radar_list_list_of_tuples = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error dangling check 3")
    # Python code to convert list of tuples into list using list comprehension
    orders_in_radar_list = [item for t in orders_in_radar_list_list_of_tuples for item in t]
    #print("orders_in_radar_list_list_of_tuples: " + str(orders_in_radar_list_list_of_tuples))
    #print("converted to list of elements" + str(orders_in_radar_list))
    print("orders in radar_list waiting for position:" + str(orders_in_radar_list))
    if sorted(orders_in_radar_list) == sorted(open_orders_waiting_for_position):
        print("dangling check3 ok") 
    else:
        print("dangling check3 detected, orders in radar_list waiting for position are not equal to existing orders waiting for position")
    
