from binance_d.example_d.user.helpers_scripts.helpers_module import funcname, get_radar_list, create_dict_from_output
from binance_d.example_d.user.common_scripts.create_orders_module import silent_limit_no_oco_sell_long, silent_limit_no_oco_buy_long
from binance_d.example_d.user.common_scripts.create_pivot_module import exec_transaction_pivot
from binance_d.example_d.user.helpers_scripts.sql import exec_sql


def process_event(event_dict):
#update radar_list(id)(status: IN_POSITION)
#generate_limit_order_sell(id) and status(id)[has_limit_order_to_close]=true
#}
    event_execution_type = event_dict['o']['x']
    event_order_status = event_dict['o']['X']
    event_order_id = event_dict['o']['i']
    event_rp = event_dict['o']['rp'] #realized profit of the trade, is != 0 when an order which was in position was executed
    radar_list = get_radar_list()
       
##  option 1 
# checkear si se cerro una orden con pnl != 0, if yes call process_pnl 
# facts:
# si se cerro una orden con pnl = 0, quiere decir que se cerro una orden new y entró en posicion
# rp : realized profit of the trade, is != 0 when an order which was in position was executed
    if event_execution_type == "TRADE" and event_order_status == "FILLED" and event_rp != 0:
        if event_order_id in str(radar_list):
            print("OK, event_order_id exists in radar_list")
            print("check status in radar_list")
            for radar_list_dict in radar_list:
                if radar_list_dict['order_id_to_close'] == event_order_id:
                    print("found radar_list_dict: " + str(radar_list_dict))
                    break
            status_in_radar_list = radar_list_dict['order_status']
            print("status_in_radar_list: " + status_in_radar_list)
            if status_in_radar_list == "IN_POSITON":
                print("OK, the order_status expected is IN_POSITION") 
                process_pnl(event_order_id, radar_list_dict)
            else:
                print("ERROR, order_status must be IN_POSITION")
                raise
        else:
            print("ERROR , event_order_id not exists in radar_list")
            raise


# option 2
# checkear si se cerro una orden con pnl = 0, if yes:
#     upddate order_status = IN_POSITION where order_id = event_order_id
#     create limit order to close Z, and update order_id_to_close = Z(order_id) where order_id = event_order_id
# si se cerro una orden con pnl = 0, quiere decir que se cerro una orden new y entró en posicion
# rp : realized profit of the trade, is != 0 when an order which was in position was executed
    elif event_execution_type == "TRADE" and event_order_status == "FILLED" and event_rp == 0:
        if event_order_id in str(radar_list):
            print("OK, event_order_id exists in radar_list")
            print("check status in radar_list")
            for radar_list_dict in radar_list:
                if radar_list_dict['order_id'] == event_order_id:
                    print("found radar_list_dict: " + str(radar_list_dict))
                    break
                status_in_radar_list = radar_list_dict['order_status']
                print("status_in_radar_list: " + status_in_radar_list)
                if status_in_radar_list == "NEW":
                    print("OK, the order_status expected is NEW") 
                    process_goto_in_position(event_order_id, radar_list_dict)
                else:
                    print("ERROR, order_status must be NEW")
                    raise
        else:
            print("ERROR , event_order_id not exists in radar_list")
            raise

def process_pnl(event_order_id, radar_list_dict):
    print("in " + funcname()) 
    p_price = radar_list_dict['trigger_price_to_put_in_position']
    p_size = radar_list_dict['original_quantity']
    sql = "update radar_list set order_status = 'PNL' "
    sql += " where order_id ='" + event_order_id + "' and order_status='IN_POSITION'"    
    rc = exec_transaction_pivot(p_price, p_size) 
    if rc == "OK":
        print("OK process_pnl, pivot recreated")
 
def process_goto_in_position(event_order_id, radar_list_dict):
    print("in " + funcname())
    p_price = radar_list_dict['trigger_price_to_close']
    p_size = radar_list_dict['original_quantity']
    output = silent_limit_no_oco_sell_long(p_price, p_size)
    output_dict =  create_dict_from_output(output)
    #POST LIMIT ,no OCO, SELL, LONG
    #result OK: {"orderId":5370806071,"symbol":"ADAUSD_PERP","pair":"ADAUSD","status":"NEW","clientOrderId":"ntBkH7G8R74PJD3kwizuMT",
    #"price":"100","avgPrice":"0.00000","origQty":"1","executedQty":"0","cumQty":"0","cumBase":"0","timeInForce":"GTC","type":"LIMIT","reduceOnly":true,
    #"closePosition":false,"side":"SELL","positionSide":"LONG","stopPrice":"0","workingType":"CONTRACT_PRICE","priceProtect":false,"origType":"LIMIT","updateTime":1645305366798}
    order_id_to_close = output_dict['orderId']
    
    sql = "update radar_list set order_status ='IN_POSITION', "
    sql += "order_id_to_close = " + order_id_to_close
    sql += " where order_id ='" + event_order_id + "' and order_status='NEW'"
    result = exec_sql(sql = sql , sql_command = "update", error_message = "update process_goto_in_position")
    if result != 1:
        print("ERROR in " + funcname() + ", result: " + str(result))
        raise
    