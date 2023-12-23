import sys
from binance_d.example_d.user.helpers_scripts.helpers_module import funcname, get_radar_list, create_dict_from_output
from binance_d.example_d.user.common_scripts.create_orders_module import silent_limit_no_oco_sell_long, silent_limit_no_oco_buy_long
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
    print("unittest          event_dict:" + str(event_dict))
    
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
        print("radar_list mock: " + str(radar_list))
##  option 1 
# checkear si se cerro una orden con pnl != 0, if yes call process_pnl 
# facts:
# si se cerro una orden con pnl = 0, quiere decir que se cerro una orden new y entró en posicion
# rp : realized profit of the trade, is != 0 when an order which was in position was executed
        if event_execution_type == "TRADE" and event_order_status == "FILLED" and float(event_rp) != 0:
            print("DETECTED TRADE FILLED rp != 0")
            if str(event_order_id) in str(radar_list):
                print(".... OK, event_order_id exists in radar_list, now we have to check if match radar_list [order_id_to_close]")
                print(".... find radar_list_dict in radar_list where order_id_to_close=" + str(event_order_id) + ", start loop")
                radar_list_dict = ""
                flag_found = False
                for radar_list_dict in radar_list:
                    if str(radar_list_dict['order_id_to_close']) == event_order_id:
                        print(".... .... found radar_list_dict: " + str(radar_list_dict))
                        print(".... .... .... break loop")
                        flag_found = True
                        break
                if not flag_found:
                    err = ".... .... ERROR, radar_list [order_id_to_close] not match event_order_id"
                    print(err)
                    return err 
                print(".... .... .... .... check if status_in_radar_list = IN_POSITION")
                status_in_radar_list = radar_list_dict['order_status']
                if status_in_radar_list == "IN_POSITION":
                    print(".... .... .... .... .... OK, status_in_radar_list = " + status_in_radar_list) 
                    print(".... .... .... .... .... .... SIERRA CALL process_pnl, params event_order_id, radar_list_dict: " + str(event_order_id) +  ", " + str(radar_list_dict))
                    rc = process_pnl(event_order_id, radar_list_dict)
                    return rc
                else:
                    print(".... .... .... .... ERROR, status_in_radar_list : " + status_in_radar_list)
                    rc = "ERROR, order_status must be IN_POSITION"
                    return rc
                    #raise
            else:
                print(".... ERROR , event_order_id not exists in radar_list")
                rc = "ERROR , event_order_id not exists in radar_list"
                return rc
                #raise
    
    
    # option 2
    # checkear si se cerro una orden con pnl = 0, if yes:
    #     upddate order_status = IN_POSITION where order_id = event_order_id
    #     create limit order to close Z, and update order_id_to_close = Z(order_id) where order_id = event_order_id
    # si se cerro una orden con pnl = 0, quiere decir que se cerro una orden new y entró en posicion
    # rp : realized profit of the trade, is != 0 when an order which was in position was executed
        elif event_execution_type == "TRADE" and event_order_status == "FILLED" and float(event_rp) == 0:
            print(".... DETECTED TRADE FILLED rp == 0 , option 2")
            print(".... .... check if order_id exists in radar_list: " + str(event_order_id))
            if event_order_id in str(radar_list):
                print(".... .... .... OK, event_order_id exists in radar_list")
                print(".... .... .... check status in radar_list, start loop")
                for radar_list_dict in radar_list:
                    if radar_list_dict['order_id'] == event_order_id:
                        print(".... .... .... .... found radar_list_dict: " + str(radar_list_dict))
                        print(".... .... .... .... .... break loop")
                        break
                status_in_radar_list = radar_list_dict['order_status']
                print(".... .... .... .... .... .... status_in_radar_list: " + status_in_radar_list)
                print(".... .... .... .... .... .... expected status_in_radar_list: NEW") 
                if status_in_radar_list == "NEW":
                        print(".... .... .... .... .... .... .... OK, status_in_radar_list: " + str(status_in_radar_list)) 
                        print(".... .... .... .... .... .... .... .... SIERRA CALL process_goto_in_position !!!, params event_order_id, radar_list_dict: " + str(event_order_id) + ", " + str(radar_list_dict))
                        rc = process_goto_in_position(event_order_id, radar_list_dict)
                        #print("mock rc: " + str(rc))
                        return rc
                else:
                    print("... .... .... .... .... .... .... ERROR, status_in_radar_list: " + str(status_in_radar_list))
                    rc = "ERROR, order_status must be NEW"
                    return rc 
                    #raise
            else:
                print(".... .... .... ERROR , event_order_id not exists in radar_list")
                rc = "ERROR , event_order_id not exists in radar_list"
                return rc
                #raise
        #### option 3,  can be an initial pivot or a new order to close
        elif event_execution_type == "NEW" and event_order_status == "NEW":
            print(".... DETECTED NEW NEW, checking if not exists in radar list")
            if event_order_id not in str(radar_list):
                print(".... .... not exists in radar_list")
                print(".... .... .... DETECTED creation of initial pivot or something to analize")
                rc = "DETECTED initial pivot or something to analize"
            else:
                print(".... .... event_order_id exists in radar_list, now we have to check if match radar_list [order_id_to_close]")
                print(".... .... .... find radar_list_dict in radar_list where order_id_to_close=" + str(event_order_id) + ", start loop")
                radar_list_dict = ""
                flag_found = False
                for radar_list_dict in radar_list:
                    if str(radar_list_dict['order_id_to_close']) == event_order_id:
                        print(".... .... .... .... found radar_list_dict: " + str(radar_list_dict))
                        print(".... .... .... .... .... break loop")
                        flag_found = True
                        break
                if not flag_found:
                    print(".... .... .... .... .... .... ERROR, radar_list [order_id_to_close] not match event_order_id")
                    err = "ERROR, new new exists order_id in radar_list [order_id_to_close] not match event_order_id"
                    print(err)
                    return err
                elif radar_list_dict['order_status'] == "IN_POSITION" and flag_found:
                    print(".... .... .... .... .... .... .... OK order_status IN_POSITION") 
                    rc = "DETECTED new new in_position order_id_to_close , this is the creation of a new order_id_to_close" #OK
                    return rc
                elif radar_list_dict['order_status'] != "IN_POSITION" and flag_found:
                    print(".... .... .... .... .... .... .... ERROR, order_status not IN_POSITION, strange situation to analyze") 
                    err = "ERROR, order_status new new order_id_to_close_exists not IN_POSITION" #OK
                    return err

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
    output = silent_limit_no_oco_sell_long(p_price, p_size)
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