import sys
from binance_d.example_d.user.helpers_scripts.helpers_module import funcname, get_radar_list, create_dict_from_output
from binance_d.example_d.user.common_scripts.create_orders_module import silent_limit_no_oco_sell_long
from binance_d.example_d.user.common_scripts.create_pivot_module import exec_transaction_pivot
from binance_d.example_d.user.helpers_scripts.sql import exec_sql


def process_event(event_dict):
    '''
    event_dict esta modelado en model.orderupdate.py

    '''
#event_dict: {'activationPrice': 'None', 'asksNotional': '1134.13422041', 'avgPrice': '0.0', 'bidsNotional': '0.0', 'callbackRate': 'None', 
#'clientOrderId': 'damian', 'commissionAmount': 'None', 'commissionAsset': 'None', 'cumulativeFilledQty': '0.0', 'eventTime': '1652726042036', 
#'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'CANCELED', 'isClosePosition': 'False', 'isMarkerSide': 'False', 'isReduceOnly': 'False', 
#'lastFilledPrice': '0.0', 'lastFilledQty': '0.0', 'orderId': '6436496462', 'orderStatus': 'CANCELED', 'orderTradeTime': '1652726042029', 
#'origQty': '1.0', 'positionSide': 'LONG', 'price': '0.1', 'realizedprofit': '0.0', 'side': 'BUY', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP',
# 'timeInForce': 'GTC', 'tradeID': '0', 'transactionTime': '1652726042029', 'type': 'LIMIT', 'workingType': 'CONTRACT_PRICE'}
    #nombre reales de eventos:
    #"x":"NEW",                  // Execution Type
    #"X":"NEW",                  // Order Status
    print("in process_event arg event_dict:" + str(event_dict))
    
    if event_dict['clientOrderId'] == "damian":
        print("in process_event DETECTED FAKE ORDER")
        rc = "DETECTED FAKE ORDER"
        return rc
    else:
        print("in process_event NOT FAKE ORDER DETECTED, BEGIN")
        event_execution_type = event_dict['executionType']
        event_order_status = event_dict['orderStatus']
        event_order_id = event_dict['orderId']
        event_rp = event_dict['realizedprofit']  #realized profit of the trade, is != 0 when an order which was in position was executed
        event_clientorderid = event_dict['clientOrderId'] 
        radar_list = get_radar_list()
        print("in process_event radar_list: " + str(radar_list))

        match_order_id = False
        match_order_id_to_close = False
        radar_list_dict_order_id = ""
        radar_list_dict_order_id_to_close = ""

        match_order_id, radar_list_dict_order_id = run_match_order_id(radar_list, event_order_id) 
        print("match_order_id,radar_list_dict_order_id: " + str(match_order_id) + ", " + str(radar_list_dict_order_id))

        match_order_id_to_close, radar_list_dict_order_id_to_close = run_match_order_id_to_close(radar_list, event_order_id)
        print("match_order_id_to_close,radar_list_dict_order_id_to_close: " + str(match_order_id_to_close) + ", " + str(radar_list_dict_order_id_to_close))

        is_new_pivot = False
        if "new_pivot" in event_clientorderid:
            is_new_pivot = True

        is_goto_in_position = False
        if "goto_in_position" in event_clientorderid:
            is_goto_in_position = True

##  option 1 
# checkear si se cerro una orden con pnl != 0, if yes call process_pnl 
# facts:
# si se cerro una orden con pnl = 0, quiere decir que se cerro una orden new y entró en posicion
# rp : realized profit of the trade, is != 0 when an order which was in position was executed
        if event_execution_type == "TRADE" and event_order_status == "FILLED" and is_goto_in_position:
            message_print = "OK call process_pnl, params event_order_id, radar_list_dict_order_id_to_close: " + str(event_order_id) +  ", " + str(radar_list_dict_order_id_to_close)
            print(".... " + message_print)
            rc = process_pnl(event_order_id, radar_list_dict_order_id_to_close)
            return rc 
        '''
        if event_execution_type == "TRADE" and event_order_status == "FILLED" and float(event_rp) != 0:
            print("DETECTED TRADE FILLED rp != 0")
            if match_order_id_to_close and radar_list_dict_order_id_to_close['order_status'] == 'IN_POSITION':
                message_print = "OK call process_pnl, params event_order_id, radar_list_dict: " + str(event_order_id) +  ", " + str(radar_list_dict_order_id_to_close)
                print(".... " + message_print)
                rc = process_pnl(event_order_id, radar_list_dict_order_id_to_close)
                return rc 
            else:
                rc = "ERROR, cannot process_pnl, strange situation"
                print(".... .... " + rc)
                return rc
        '''
    # option 2
    # checkear si se cerro una orden con pnl = 0, if yes:
    #     upddate order_status = IN_POSITION where order_id = event_order_id
    #     create limit order to close Z, and update order_id_to_close = Z(order_id) where order_id = event_order_id
    # si se cerro una orden con pnl = 0, quiere decir que se cerro una orden new y entró en posicion
    # rp : realized profit of the trade, is != 0 when an order which was in position was executed
        #elif event_execution_type == "TRADE" and event_order_status == "FILLED" and is_new_pivot:

        elif event_execution_type == "TRADE" and event_order_status == "FILLED" and is_new_pivot:
            print(".... DETECTED TRADE FILLED rp == 0 , option 2")
            message_print = "OK call process_goto_in_position, params event_order_id, radar_list_dict_order_id: " + str(event_order_id) +  ", " + str(radar_list_dict_order_id)
       #     print(".... .... " + message_print)
       #     rc = process_goto_in_position(event_order_id, radar_list_dict_order_id)
       #     return rc
        ''' 
        elif event_execution_type == "TRADE" and event_order_status == "FILLED" and float(event_rp) == 0:
            print(".... DETECTED TRADE FILLED rp == 0 , option 2")
            if match_order_id and radar_list_dict_order_id['order_status'] == "NEW" and radar_list_dict_order_id['order_id_to_close'] == 0:
                message_print = "OK call process_goto_in_position, params event_order_id, radar_list_dict_order_id: " + str(event_order_id) +  ", " + str(radar_list_dict_order_id)
                print(".... .... " + message_print)
                rc = process_goto_in_position(event_order_id, radar_list_dict_order_id)
                return rc
            else:
                rc = "ERROR, cannot process_goto_in_position, strange situation"
                print(".... .... " + rc)
                return rc
        '''
        # option 3  
        # can be an initial pivot or a new order to close
        #### 
        elif event_order_status == "NEW" and is_new_pivot:
            rc = "DETECTED initial pivot"
            print(".... .... " + rc)
            return rc 
        ####
        '''
        elif event_execution_type == "NEW" and event_order_status == "NEW":
            print(".... DETECTED NEW NEW, checking if not exists in radar_list[order_id]")
            match_order_id = False
            match_order_id_to_close = False
            radar_list_dict_order_id = ""
            radar_list_dict_order_id_to_close = ""

            match_order_id, radar_list_dict_order_id = run_match_order_id(radar_list, event_order_id) 
            print("match_order_id,radar_list_dict_order_id: " + str(match_order_id) + ", " + str(radar_list_dict_order_id))

            match_order_id_to_close, radar_list_dict_order_id_to_close = run_match_order_id_to_close(radar_list, event_order_id)
            print("match_order_id_to_close,radar_list_dict_order_id_to_close: " + str(match_order_id_to_close) + ", " + str(radar_list_dict_order_id_to_close))

            if not match_order_id and not match_order_id_to_close:
                rc = "DETECTED initial pivot"
                print(".... .... " + rc)
                return rc
            elif not match_order_id and match_order_id_to_close and radar_list_dict_order_id_to_close['order_status'] == 'IN_POSITION': 
                rc = "DETECTED new new in_position order_id_to_close , this is the creation of a new order_id_to_close"
                print(".... .... " + rc)
                return rc
            else:
                rc = "ERROR, strange situation" 
                print(".... .... " + rc) 
                return rc
            '''
        else:
            nada = 1 

def process_pnl(event_order_id, radar_list_dict):
    print("in " + funcname() + ", args event_order_id, radar_list_dict: " + str(event_order_id) + ", " + str(radar_list_dict)) 
    p_price = radar_list_dict['trigger_price_to_put_in_position']
    p_size = radar_list_dict['original_quantity']
    sql = "update radar_list set order_status = 'PNL' "
    sql += " where order_id ='" + event_order_id + "' and order_status='IN_POSITION'"    
    print(".... cal exec_sql with sql: " + str(sql))
    result = exec_sql(sql = sql , sql_command = "update", error_message = "update process_pnl")
    if result != 1:
        print(".... .... ERROR in " + funcname() + ", result: " + str(result))
        rc = "ERROR in process_pnl exec_sql"
        return rc
    else:
        print(".... .... exec_sql OK, call exec_transaction_pivot, args : p_price, p_size: " + str(p_price) + ", p_size: " + str(p_size))    
        rc = exec_transaction_pivot(p_price, p_size) 
        if rc == "OK":
            rc = "OK, pivot recreated"
            print(".... .... .... OK, pivot recreated")
            return rc   

def process_goto_in_position(event_order_id, radar_list_dict):
    print("in " + funcname() + ", args event_order_id, radar_list_dict: " + str(event_order_id) + ", " + str(radar_list_dict))
    p_price = radar_list_dict['trigger_price_to_close']
    p_size = radar_list_dict['original_quantity']
    print(".... create limit order to close, call silent_limit_no_oco_sell_long")
    output = silent_limit_no_oco_sell_long(p_price, p_size, p_clientorderid="goto_in_position")
    print(".... .... output: " + str(output))
    output_dict =  create_dict_from_output(output)
    print(".... .... output_dict: " + str(output_dict))
    print(".... .... output_dict is type: " + str(type(output_dict)))
    #POST LIMIT ,no OCO, SELL, LONG
    #result OK: {"orderId":5370806071,"symbol":"ADAUSD_PERP","pair":"ADAUSD","status":"NEW","clientOrderId":"ntBkH7G8R74PJD3kwizuMT",
    #"price":"100","avgPrice":"0.00000","origQty":"1","executedQty":"0","cumQty":"0","cumBase":"0","timeInForce":"GTC","type":"LIMIT","reduceOnly":true,
    #"closePosition":false,"side":"SELL","positionSide":"LONG","stopPrice":"0","workingType":"CONTRACT_PRICE","priceProtect":false,"origType":"LIMIT","updateTime":1645305366798}
    order_id_to_close = output_dict['orderId']
    
    print(".... .... order_id_to_close: " + str(order_id_to_close))
    sql = "update radar_list set order_status ='IN_POSITION', "
    sql += "order_id_to_close = " + order_id_to_close
    sql += " where order_id ='" + event_order_id + "' and order_status='NEW'"
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

def run_match_order_id(radar_list, event_order_id):
    flag_found = False
    radar_list_dict = {}
    for radar_list_dict in radar_list:
        if str(radar_list_dict['order_id']) == event_order_id:
            flag_found = True
            break
    return flag_found, radar_list_dict 

def run_match_order_id_to_close(radar_list, event_order_id):
    flag_found = False
    radar_list_dict = {}
    for radar_list_dict in radar_list:
        if str(radar_list_dict['order_id_to_close']) == event_order_id:
            flag_found = True
            break
    return flag_found, radar_list_dict        