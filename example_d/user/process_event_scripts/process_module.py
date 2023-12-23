import sys
from binance_d.example_d.user.helpers_scripts.helpers_module import funcname, get_radar_list, create_dict_from_output
from binance_d.example_d.user.common_scripts.create_orders_module import silent_limit_no_oco_sell_long
from binance_d.example_d.user.common_scripts.create_pivot_module import exec_transaction_pivot, exec_transaction_pivot_conditional
from binance_d.example_d.user.helpers_scripts.sql import exec_sql
from binance_d.impl.utils.timeservice import get_current_timestamp


def process_event(event_dict):
    '''
    caller is example_d.user.websocket_module.py
    event_dict esta modelado en model.orderupdate.py
    '''
#event_dict: {'activationPrice': 'None', 'asksNotional': '1134.13422041', 'avgPrice': '0.0', 'bidsNotional': '0.0', 'callbackRate': 'None', 
#'clientOrderId': 'fakeorder', 'commissionAmount': 'None', 'commissionAsset': 'None', 'cumulativeFilledQty': '0.0', 'eventTime': '1652726042036', 
#'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'CANCELED', 'isClosePosition': 'False', 'isMarkerSide': 'False', 'isReduceOnly': 'False', 
#'lastFilledPrice': '0.0', 'lastFilledQty': '0.0', 'orderId': '6436496462', 'orderStatus': 'CANCELED', 'orderTradeTime': '1652726042029', 
#'origQty': '1.0', 'positionSide': 'LONG', 'price': '0.1', 'realizedprofit': '0.0', 'side': 'BUY', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP',
# 'timeInForce': 'GTC', 'tradeID': '0', 'transactionTime': '1652726042029', 'type': 'LIMIT', 'workingType': 'CONTRACT_PRICE'}
    #nombre reales de eventos:
    #"x":"NEW",                  // Execution Type
    #"X":"NEW",                  // Order Status
    #print("in process_event arg event_dict:" + str(event_dict))
    if "fakeorder" in event_dict['clientOrderId']:
        print("in process_event DETECTED FAKE ORDER")
        rc = "DETECTED FAKE ORDER" # useless rc variable
        return rc
    else:
        print("in process_event DETECTED OK ORDER, BEGIN")
        event_execution_type = event_dict['executionType']
        event_order_status = event_dict['orderStatus']
        event_order_id = event_dict['orderId']
        event_rp = event_dict['realizedprofit']  #realized profit of the trade, is != 0 when an order which was in position was executed
        event_clientorderid = event_dict['clientOrderId'] 
        #radar_list = get_radar_list()
        #print("in process_event radar_list: " + str(radar_list))

        #radar_list_dict_order_id = ""
        #match_order_id = False
        #match_order_id, radar_list_dict_order_id = run_match_order_id(radar_list, event_order_id) 
        #print("match_order_id,radar_list_dict_order_id: " + str(match_order_id) + ", " + str(radar_list_dict_order_id))

        #match_order_id_to_close = False
        #radar_list_dict_order_id_to_close = ""
        #match_order_id_to_close, radar_list_dict_order_id_to_close = run_match_order_id_to_close(radar_list, event_order_id)
        #print("match_order_id_to_close,radar_list_dict_order_id_to_close: " + str(match_order_id_to_close) + ", " + str(radar_list_dict_order_id_to_close))

        is_new_pivot = False
        if "new_pivot" in event_clientorderid:
            is_new_pivot = True

        is_goto_in_position = False
        if "goto_in_position" in event_clientorderid:
            is_goto_in_position = True

##  option 1 
# checkear si se cerro una orden que estaba en posicion, y llamar a process_pnl, que se encarga de repetir el pivot
# si estaba en posicion se cumple que: clientorderid = goto_in_positionXXX 
# facts:
# si se cerro una orden con pnl = 0, quiere decir que se cerro una orden new y entró en posicion
# rp : realized profit of the trade, is != 0 when an order which was in position was executed
        if event_execution_type == "TRADE" and event_order_status == "FILLED" and is_goto_in_position:
            match_order_id_to_close = False
            radar_list_dict_order_id_to_close = ""
            radar_list = get_radar_list()
            match_order_id_to_close, radar_list_dict_order_id_to_close = run_match_order_id_to_close(radar_list, event_order_id)
            print("match_order_id_to_close,radar_list_dict_order_id_to_close: " + str(match_order_id_to_close) + ", " + str(radar_list_dict_order_id_to_close))
            if match_order_id_to_close:
                message_print = "OK will call process_pnl, params event_order_id, radar_list_dict_order_id_to_close: " + str(event_order_id) +  ", " + str(radar_list_dict_order_id_to_close)
                print(".... " + message_print)
                rc = process_pnl(event_order_id, event_rp, radar_list_dict_order_id_to_close) # useless rc variable
                return rc 
            
    # option 2
    # checkear si un pivot entró en posicion, y llamar a process_goto_in_position que se encarga de generar la orden de venta
    # si el pivot es nuevo se cumple que: clientorderid = new_pivotXXX
    #     upddate order_status = IN_POSITION where order_id = event_order_id
    #     create limit order to close Z, and update order_id_to_close = Z(order_id) where order_id = event_order_id
        elif event_execution_type == "TRADE" and event_order_status == "FILLED" and is_new_pivot:
            print(".... DETECTED TRADE FILLED rp == 0 , option 2")
            print(".... event_order_id:", event_order_id)
            radar_list = get_radar_list()
            radar_list_dict_order_id = ""
            match_order_id, radar_list_dict_order_id = run_match_order_id(radar_list, event_order_id) 
            print("match_order_id,radar_list_dict_order_id: " + str(match_order_id) + ", " + str(radar_list_dict_order_id))
            if match_order_id:
                message_print = "OK call process_goto_in_position, params event_order_id, radar_list_dict_order_id: " + str(event_order_id) +  ", " + str(radar_list_dict_order_id)
                print(".... .... " + message_print)
                rc = process_goto_in_position(event_order_id, radar_list_dict_order_id)
                return rc
            else:
                message_print = "ERROR call process_goto_in_position, order_id: " + str(event_order_id) + " not found in radar_list"
                print(".... .... " + message_print)
                rc = message_print
                return rc
        # option 3  
        # chequear si se creó un pivot o una nueva orden de venta
        #### 
        elif event_order_status == "NEW" and is_new_pivot:
            rc = "DETECTED initial pivot"
            print(".... .... " + rc)
            return rc 
        elif event_order_status == "NEW" and is_goto_in_position:
            rc = "DETECTED creation of NEW order_id_to_close"
            print(".... .... " + rc)
            return rc 
        else:
            rc = "ERROR, strange situation"
            print(".... .... " + rc)
            return rc 
       
def insert_tracker_pnl(event_order_id, event_rp):
    try:
        timestamp = get_current_timestamp()
        tuple1 = (event_order_id, timestamp, event_rp)
        sql = "insert into tracker_pnl ( order_id, timestamp, rp) values "
        sql += str(tuple1)
        rows_inserted = exec_sql(sql = sql, sql_command = "insert", error_message = "error in " + str(funcname()))
        if rows_inserted != 1:
            err = "ERROR in " + funcname()
            print(err)
        else:
            print("OK " + funcname()) 
    except:
        err = "ERROR except in " + funcname() + ", non critical error, can continue"
        print(err)

def pnl_bkp_and_clean_from_radar_list(event_order_id):
    try:
        sql = "insert into pnl_hist select * from radar_list where order_id_to_close=" + event_order_id + " and order_status ='PNL';"
        rows_inserted = exec_sql(sql = sql, sql_command = "insert", error_message = "error in " + str(funcname()))
        if rows_inserted != 1:
            print(".... ERROR in " + funcname() + ", rows_inserted !=1 : " + str(rows_inserted))
        elif rows_inserted == 1:
            print(".... OK 1 rows_inserted in pnl_hist")
            sql = "delete from radar_list where order_id_to_close=" + event_order_id + " and order_status ='PNL';" 
            rows_deleted = exec_sql(sql = sql, sql_command = "delete", error_message = "error in " + str(funcname())) 
            if rows_deleted != 1:
                print("ERROR in " + funcname() + ", rows_deleted !=1 : " + str(rows_deleted))
            elif rows_deleted == 1:
                print(".... OK 1 rows_deleted in radar_list")
    except:
        err = ".... ERROR except in " + funcname() + ", non critical error, can continue"
        print(err)
    finally:
        print(".... OK END " + funcname()) 
        

def process_pnl(event_order_id, event_rp, radar_list_dict):
    '''
    caller is process_event_scripts.process_module.process_event
    radar_list_dict: {'order_id': 8652093236, 'order_status': 'IN_POSITION', 'order_id_to_close': 8652097881, 
    'trigger_price_to_put_in_position': 0.2779, 'trigger_price_to_close': 0.2786, 'original_quantity': 1, 
    'clientorderid': 'new_pivot1698177695676', 'repeat': 'Y', 'resize': 1, 'factor_gain': 1.0025, 'group_id': 0, 
    'conditional': 'N'}
    '''
    print("in " + funcname() + ", args event_order_id, radar_list_dict: " + str(event_order_id) + ", " + str(radar_list_dict)) 
    return_flag = "N"
    p_price = radar_list_dict['trigger_price_to_put_in_position']
    p_size = radar_list_dict['original_quantity']
    tp = p_price
    tc = radar_list_dict['trigger_price_to_close']
    conditional_pivot = "N"
    try:
        conditional_pivot = radar_list_dict['conditional']
        print("in " + funcname() + ", conditional_pivot:", conditional_pivot)
    except:
        error = "in " + funcname() + ", except set variable conditional_pivot, " + str(sys.exc_info())
        print(error)
    try:
        group_id = radar_list_dict['group_id']
        print(funcname(), ".... extract group_id:", group_id)
    except:
        print(funcname(), ".... except extract group_id", sys.exc_info())
        group_id = 0
        print(funcname(), ".... .... group_id hardcoded to zero due to exception:", group_id)
    try:
        repeat_pivot = radar_list_dict['repeat']
        resize_pivot = radar_list_dict['resize']
        factor_gain = radar_list_dict['factor_gain']
        print(funcname(), ", repeat_pivot, resize_pivot, factor_gain: ", repeat_pivot, resize_pivot, factor_gain)
    except:
        nada = 1
        print(funcname(), ", except repeat_pivot, resize_pivot: " + str(sys.exc_info()))

    if conditional_pivot == "N":
        print("in " + funcname() + ", processing ws event non conditional_pivot")
        sql = "update radar_list set order_status = 'PNL' "
        sql += " where order_id_to_close ='" + event_order_id + "' and order_status='IN_POSITION'"    
        print(funcname(), ".... cal exec_sql with sql: " + str(sql))
        result = exec_sql(sql = sql , sql_command = "update", error_message = "update process_pnl")
        if result != 1:
            print(".... .... ERROR in " + funcname() + ", result: " + str(result))
            rc = "ERROR in process_pnl exec_sql"
            return rc
           # return_flag = "Y"
        else:
            print(funcname(), ".... .... call insert_tracker_pnl")
            insert_tracker_pnl(event_order_id, event_rp)
            pnl_bkp_and_clean_from_radar_list(event_order_id)
            print(funcname(), ".... .... exec_sql OK, call exec_transaction_pivot, args : p_price, p_size: " + str(p_price) + ", p_size: " + str(p_size) + ", factor_gain: " + str(factor_gain) + ", group_id: " + str(group_id))    
            try:
                if repeat_pivot == "Y":
                    print(funcname(), ", repeat_pivot == Y")
                    if resize_pivot != p_size:
                        print(funcname(), ", resize_pivot != p_size: ", resize_pivot, p_size)
                        p_size = resize_pivot
                        print(funcname(), ", pivot resized: ", p_size) 
                    rc = exec_transaction_pivot(p_price, p_size, factor_gain, group_id) 
                    if rc == "OK":
                        print(funcname(), ".... .... .... OK, pivot recreated")
                        rc = "OK, pivot recreated, " # useless rc variable
                        # first step in processing conditional pivot
                        rc += process_conditional_pivot(tp, tc) 
                        return rc
                else:
                    print(funcname(), ", repeat_pivot != Y , no se repite este pivot")
                    rc = "OK, pivot not repeated, " # useless rc variable
                    # first step in processing conditional pivot
                    rc += process_conditional_pivot(tp, tc)
                    return rc
            except:
                err = "except in " + funcname() + ", try/except block repeat pivot non conditional, " + str(sys.exc_info())
                print(err)
    elif conditional_pivot == "Y":
        print("in " + funcname() + ", processing ws event conditional_pivot")
        sql = "update radar_list set order_status = 'PNL' "
        sql += " where order_id_to_close ='" + event_order_id + "' and order_status='IN_POSITION'"    
        print(funcname(), ".... cal exec_sql with sql: " + str(sql))
        result = exec_sql(sql = sql , sql_command = "update", error_message = "update process_pnl conditional_pivot")
        if result != 1:
            print(".... .... ERROR in " + funcname() + ", result: " + str(result))
            rc = "ERROR in process_pnl exec_sql conditional_pivot"
            return rc
        else:
            print(funcname(), ".... .... call insert_tracker_pnl conditional_pivot")
            insert_tracker_pnl(event_order_id, event_rp)
            pnl_bkp_and_clean_from_radar_list(event_order_id)
            # check if active and repeat
            sql = "select trigger_price_to_put_in_position, trigger_price_to_close, original_quantity, repeat from "
            sql += "conditional_pivots where active='Y' and main_trigger_price='" + str(p_price) + "'" 
            result = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error sql conditional_pivots")
            print(funcname(), ", check table conditional_pivots result:", result)
            print(funcname(), ", result type:", type(result))
            repeat_conditional_pivot = "N"
            if result: # is a list of tuples
                print(funcname(), ", result true, conditional pivot start process")
                print("in,", funcname(), ", ok proceed to create conditional pivot")
                for item_tuple in result:
                    tp = item_tuple[0]
                    tc = item_tuple[1] 
                    size = item_tuple[2]
                    repeat_conditional_pivot = item_tuple[3]
                result_dict = dict(tp=tp, tc=tc, size=size)
                print(funcname(), ", conditional pivot to create, result_dict:", result_dict)
                print(funcname(), ", conditional_pivot is active, check if we can repeat") 
                if repeat_conditional_pivot == "Y":
                    print(funcname(), ", check = Y, proceed to repeat_conditional_pivot:", repeat_conditional_pivot)
                    try:
                        exec_transaction_pivot_conditional(tp, tc, size)
                        print("in " + funcname() + ", return to root caller")
                        return
                    except:
                        err = "except in " + funcname() + ", except_transaction_pivot_conditional call" + str(sys.exc_info())
                        print(err)
                else:
                    print(funcname(), ", no repeat, check repeat_conditional_pivot:", repeat_conditional_pivot)
            else:
                print(funcname(),", no proceed to create conditional pivot, sql result if active=Y is empty")
                message = "in " + funcname() + ", return only"
                return message

def process_conditional_pivot(p_price, trigger_price_to_close):
    '''
    first step in processing conditional pivot
    tree: 
        1. begin caller is local, process_event_scripts/process_module.process_pnl 
    arguments:
        p_price: tp
    '''
    print("in ", funcname(),", begin")
    # primer paso check si hay pivot conditional a crear con el tp recibido por argumento
    sql = "select trigger_price_to_put_in_position, trigger_price_to_close, original_quantity, repeat from "
    sql += "conditional_pivots where active='Y' and main_trigger_price='" + str(p_price) + "'" 
    print(funcname(), ",check table conditional_pivots sql:", sql)
    result = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error sql conditional_pivots")
    print(funcname(), ", check table conditional_pivots result:", result)
    #print(funcname(), ", result type:", type(result))
    repeat_conditional_pivot = "N"
    if result: # is a list of tuples
        print(funcname(), ",trigger_to_create_activated result true, conditional pivot start process")
        print("in,", funcname(), ", ok proceed to create conditional pivot")
        for item_tuple in result:
            tp = item_tuple[0]
            tc = item_tuple[1] 
            size = item_tuple[2]
            repeat_conditional_pivot = item_tuple[3]
        result_dict = dict(tp=tp, tc=tc, size=size)
        print(funcname(), ", conditional pivot to create, result_dict:", result_dict)
        print("in ", funcname(), ", check if conditional pivot already exists")
        #sql = "select * from radar_list_test_conditional where conditional ='Y' and "
        sql = "select case when count(*) = 0 then 0 "
        sql += "else count(*) end as num_rows "
        sql += "from radar_list where conditional='Y' and order_status not like 'PNL' and "
        sql += "(trigger_price_to_put_in_position, trigger_price_to_close, original_quantity) in "
        sql += "(select trigger_price_to_put_in_position, trigger_price_to_close, original_quantity from "
        sql += "conditional_pivots where active='Y' and main_trigger_price='" + str(p_price) + "')"  
        result_already_exists = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error sql conditional_pivots")
        print(funcname(), ", conditional_pivot check result_already_exists:", result_already_exists)
        print(funcname(), ", conditional_pivot check result_already_exists type:", type(result_already_exists))
        num_rows = 0
        for num_rows_tuple in result_already_exists:
            num_rows = num_rows_tuple[0]
            print(funcname(), ", num_rows:", num_rows)
        if num_rows == 0:
            print(funcname(), ", conditional_pivot not exists, proceed to create") 
            try:
                pass
                exec_transaction_pivot_conditional(tp, tc, size)
            except:
                err = "in " + funcname() + "except in call exec_transaction_pivot_conditional, " + str(sys.exc_info())
                print(err)
        else:
            print("in ", funcname(), ", conditional_pivot already exists") 
    else:
        print(funcname(), ", trigger_to_create_no , sql result empty")
    message = "in " + funcname() + ", return only"
    return message

def process_goto_in_position(event_order_id, radar_list_dict):
    # genera la orden de venta(Z) de un pivot que entró en posicion y hace
    #  update order_status='IN_POSITION', order_id_to_close=el id de la orden de venta creada(Z)
    print("in " + funcname() + ", args event_order_id, radar_list_dict: " + str(event_order_id) + ", " + str(radar_list_dict))
    p_price = radar_list_dict['trigger_price_to_close']
    p_size = radar_list_dict['original_quantity']
    print(".... create limit order to close, call silent_limit_no_oco_sell_long")
    clientorderid_value = "goto_in_position" + str(get_current_timestamp())
    output = silent_limit_no_oco_sell_long(p_price, p_size, p_clientorderid=clientorderid_value)
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