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


def get_open_orders_dict():
    '''
    returns:
        my_list: list, list of dicts
    '''
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    result = request_client.get_open_orders(symbol="ADAUSD_PERP")
    #output result is list of dicts:
    # [{"orderId":6182797447,"symbol":"ADAUSD_PERP","pair":"ADAUSD","status":"NEW","clientOrderId":"6VFxtvJFEUWBGMf16V3IFu",
    #   "price":"0.09925","avgPrice":"0","origQty":"1","executedQty":"0","cumBase":"0","timeInForce":"GTC","type":"LIMIT",
    #   "reduceOnly":false,"closePosition":false,"side":"BUY","positionSide":"LONG","stopPrice":"0","workingType":"CONTRACT_PRICE",
    #   "priceProtect":false,"origType":"LIMIT","time":1651362220827,"updateTime":1651362220827}, 
    #  {"orderId":6183249705,"symb
    my_list = []
    for idx, row in enumerate(result):
        #print("data number " + (str(idx)) + " :")
        my_dict = create_dict_from_output(row)
        my_list.append(my_dict)
        #print("my_dict: " + str(my_dict))
    #input("in: " + funcname() + ", my_list: " + str(my_list))
    return my_list

def get_open_orders_sell_and_buy_list():
    open_orders_list = get_open_orders_dict()
    #print("open_order_list: ", open_orders_list)
    #sys.exit(66)
    current_orders_sell_list = []
    current_orders_buy_list = []

    current_oco_position_side_short_list = []
    current_oco_position_side_long_list = []
    # example oco de una posicion short con stoploss y takeprofit activado:
    # {'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'web_pjWxSGvrDJXRii5lxHMo', 
    # 'closePosition': 'True', 'cumBase': '0.0', 'executedQty': '0.0', 'orderId': '8074770368', 
    # 'origQty': '0.0', 'origType': 'TAKE_PROFIT_MARKET', 'positionSide': 'SHORT', 'price': '0.0', 
    # 'priceRate': 'None', 'reduceOnly': 'True', 'side': 'BUY', 'status': 'NEW', 'stopPrice': '0.3629', 
    # 'symbol': 'ADAUSD_PERP', 'timeInForce': 'GTE_GTC', 'type': 'TAKE_PROFIT_MARKET', 'updateTime': '1674431579461', 
    # 'workingType': 'MARK_PRICE'}, 
    # {'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'web_pp8TMYfQv58U6D6EB2dQ', 
    # 'closePosition': 'True', 'cumBase': '0.0', 'executedQty': '0.0', 'orderId': '8074770367', 
    # 'origQty': '0.0', 'origType': 'STOP_MARKET', 'positionSide': 'SHORT', 'price': '0.0', 
    # 'priceRate': 'None', 'reduceOnly': 'True', 'side': 'BUY', 'status': 'NEW', 'stopPrice': '0.395', 
    # 'symbol': 'ADAUSD_PERP', 'timeInForce': 'GTE_GTC', 'type': 'STOP_MARKET', 'updateTime': '1674431579456', 
    # 'workingType': 'MARK_PRICE'}, 


    for open_orders_list_dict in open_orders_list:
    # asi se ve una limit sell en open_orders_list
    # open_orders_list   {'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'goto_in_position1653456812156', 
    # 'closePosition': 'False', 'cumBase': '0.0', 'executedQty': '0.0', 'orderId': '6517336318', 'origQty': '1.0', 
    # 'origType': 'LIMIT', 'positionSide': 'LONG', 'price': '0.52274', 'priceRate': 'None', 'reduceOnly': 'True', 
    # 'side': 'SELL', 'status': 'NEW', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 'timeInForce': 'GTC', 'type': 'LIMIT', 
    # 'updateTime': '1653456813337', 'workingType': 'CONTRACT_PRICE'}, 


        side = open_orders_list_dict['side']
        status = open_orders_list_dict['status']
        price = open_orders_list_dict['price']
        size = open_orders_list_dict['origQty']
        orig_type = open_orders_list_dict['origType']
        position_side = open_orders_list_dict['positionSide']
        #print("open_orders_dict side, status:" + str(side) + ", " + str(status))
        if side == "SELL" and status == "NEW" and orig_type == "LIMIT":
            my_dict = dict(order_id_to_close=int(open_orders_list_dict['orderId']), 
                           price=price,
                           size=size)
            current_orders_sell_list.append(my_dict) 
        elif side == "BUY" and status == "NEW" and orig_type == "LIMIT":
            my_dict = dict(order_id=int(open_orders_list_dict['orderId']),
                           price=price,
                           size=size)
            current_orders_buy_list.append(my_dict)
        #elif side == "BUY" and status == "NEW" and orig_type == "TAKE_PROFIT_MARKET" and position_side == "SHORT":
        #elif side == "BUY" and status == "NEW" and orig_type == "STOP_MARKET" and position_side == "SHORT"
    print("current_orders_buy_list:", current_orders_buy_list)
    sys.exit(66)
    return current_orders_sell_list, current_orders_buy_list

def get_close_orders_from_radar_list():
    sql = "select order_id_to_close, trigger_price_to_close, original_quantity from radar_list where order_id_to_close != 0 and order_status = 'IN_POSITION'"
    res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error dangling check 2")
   # print("res_sql: ", res_sql)
    res_list = [{'order_id_to_close':a[0], 'price_close':a[1],'size':a[2]} for a in res_sql] #convert list of tuples in list of dicts
    #print(res_list)
    return res_list

def check_close_order(order_id_to_close):
    current_orders_sell_list, current_orders_buy_list = get_open_orders_sell_and_buy_list()
    #print("sell_list: ", current_orders_sell_list)
    flag_exists = False
    for sell_dict in current_orders_sell_list:
        if order_id_to_close == sell_dict['order_id_to_close']:
            #price = sell_dict['price']
            #size = sell_dict['size']
            found_sell = sell_dict
            flag_exists = True
        else:
            #print("ERROR close_order not exists")
            nada = 1
    if flag_exists:
            print("OK exists close_order [ order_id, price, size ]: ", found_sell)
    else:
            print("ERROR close_order not exists")

def check_diff():
    current_orders_sell_list, current_orders_buy_list = get_open_orders_sell_and_buy_list()
    close_orders_radar_list = get_close_orders_from_radar_list()
    print("current_orders_buy_list:", current_orders_buy_list)
    print("")
    print("close_orders_radar_list: ", close_orders_radar_list)
    print("")
    print("current_orders_sell_list: ", current_orders_sell_list)
    print("check if orders in radar_list exists in current")

    flag_found = False
    for radar_list_dict in close_orders_radar_list:
        flag_found = False
        #print("")
        #print("analyze radar_list_dict: ", radar_list_dict)
        for current_dict in current_orders_sell_list:
            if current_dict['order_id_to_close'] == radar_list_dict['order_id_to_close']:
                flag_found = True
        if flag_found: 
           #print(".... found")
           nada = 1
        else:
            print(".... NOT FOUND in current_orders_sell_list: ", radar_list_dict)
            #input("pec 1")
    if flag_found:
        print("OK")

    input("pec")
    print("check if current sell orders exists in radar_list")
    for current_dict in current_orders_sell_list:
        #print("")
        #print("analyze current_dict: ", current_dict)
        flag_found = False
        for radar_list_dict in close_orders_radar_list:
            #print(".... radar_list_dict: ", radar_list_dict)
            if current_dict['order_id_to_close'] == radar_list_dict['order_id_to_close']:
                #print(current_dict['price'])
                #print(radar_list_dict['price_close'])
                flag_found = True
                if ( str(current_dict['price']) != str(radar_list_dict['price_close']) ) or (float(current_dict['size']) != float(radar_list_dict['size'])):
                    #print("ok price")
                    print("................................")
                    print("current: ", current_dict)
                    print("radar_list: ", radar_list_dict)
                    print("................................")

                else:
                    nada = 1
        if flag_found: 
           # print(".... found")
           nada = 1
        else:
            print(".... NOT FOUND in radar_list: ", current_dict)
        
    
check_diff()
#get_close_order_dict_from_radar_list()
print(".....................................")
#check_close_order(7903203997)
#check_close_order(7067306470)
#check_close_order(7056831891)
