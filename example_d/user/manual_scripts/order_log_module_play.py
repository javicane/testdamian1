from binance_d import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output 
from binance_d.example_d.user.helpers_scripts.sql import exec_sql
from requests import get
from binance_d.impl.utils.timeservice import get_current_timestamp

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

def limit_no_oco_sell_long(p_price, p_size):
    '''
    POST LIMIT ,no OCO, SELL, LONG
    result OK: {"orderId":5370806071,"symbol":"ADAUSD_PERP","pair":"ADAUSD","status":"NEW","clientOrderId":"ntBkH7G8R74PJD3kwizuMT",
    "price":"100","avgPrice":"0.00000","origQty":"1","executedQty":"0","cumQty":"0","cumBase":"0","timeInForce":"GTC","type":"LIMIT","reduceOnly":true,
    "closePosition":false,"side":"SELL","positionSide":"LONG","stopPrice":"0","workingType":"CONTRACT_PRICE","priceProtect":false,"origType":"LIMIT","updateTime":1645305366798}
    '''
    p_symbol_name = "ADAUSD_PERP"
    p_side = OrderSide.SELL
    p_order_type = OrderType.LIMIT
    p_price = str(p_price) # must be string or '[Executing] -1111: Precision is over the maximum defined for this asset.') 
    p_quantity = p_size
    p_timeinforce = TimeInForce.GTC
    p_positionside = PositionSide.LONG
    result = request_client.post_order(symbol=p_symbol_name, side=p_side, ordertype=p_order_type, price=p_price, quantity=p_quantity, timeInForce=p_timeinforce, positionSide=p_positionside)
    return result


def orders_hist():
    p_symbol_name = "ADAUSD_PERP"
    p_side = OrderSide.BUY
    p_order_type = OrderType.LIMIT
    
    p_price = 2
    p_size = 1

    p_price = str(p_price) # must be string or '[Executing] -1111: Precision is over the maximum defined for this asset.')
    p_quantity = p_size

    p_timeinforce = TimeInForce.GTC
    p_positionside = PositionSide.LONG
    result = limit_no_oco_sell_long(p_price, p_size)
    output_dict =  create_dict_from_output(result)
    #del result usar esto     "T":1651189973485, el "Trade time"
    print("output_dict: " + str(output_dict))
    print("output_dict is type: " + str(type(output_dict)))
#in impl.restapiinvoker.call_sync POST: {"orderId":6445469087,"symbol":"ADAUSD_PERP","pair":"ADAUSD","status":"NEW","clientOrderId":"mUWZty6wbfSp8MzoX1nROP",
# "price":"2","avgPrice":"0.00000","origQty":"1","executedQty":"0","cumQty":"0","cumBase":"0","timeInForce":"GTC","type":"LIMIT","reduceOnly":true,
# "closePosition":false,"side":"SELL","positionSide":"LONG","stopPrice":"0","workingType":"CONTRACT_PRICE","priceProtect":false,"origType":"LIMIT",
# "updateTime":1652811823407}|||
#output_dict: {'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'mUWZty6wbfSp8MzoX1nROP', 'closePosition': 'False', 'cumBase': '0.0', 
# 'executedQty': '0.0', 'orderId': '6445469087', 'origQty': '1.0', 'origType': 'LIMIT', 'positionSide': 'LONG', 'price': '2.0', 'priceRate': 'None', 
# 'reduceOnly': 'True', 'side': 'SELL', 'status': 'NEW', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 'timeInForce': 'GTC', 'type': 'LIMIT', 
# 'updateTime': '1652811823407', 'workingType': 'CONTRACT_PRICE'}

    sql = "insert into order_hist (current_timestamp, activatePrice,avgPrice,clientOrderId, closePosition, cumBase, executedQty, orderId, origQty,origType, positionSide,price,"
    sql += "priceRate, reduceOnly, side, status,stopPrice,symbol,timeInForce,type, updateTime , workingType ) "
    sql += " values (" + str(get_current_timestamp()) + ","
    sql += "'" + str(output_dict['activatePrice']) + "',"
    sql += "'" + str(output_dict['avgPrice']) + "',"
    sql += "'" + str(output_dict['clientOrderId']) + "',"
    sql += "'" + str(output_dict['closePosition']) + "',"
    sql += "'" + str(output_dict['cumBase']) + "',"
    sql += "'" + str(output_dict['executedQty']) + "',"
    sql += "'" + str(output_dict['orderId']) + "',"
    sql += "'" + str(output_dict['origQty']) + "',"
    sql += "'" + str(output_dict['origType']) + "',"
    sql += "'" + str(output_dict['positionSide']) + "',"
    sql += "'" + str(output_dict['price']) + "',"
    sql += "'" + str(output_dict['priceRate']) + "',"
    sql += "'" + str(output_dict['reduceOnly']) + "',"
    sql += "'" + str(output_dict['side']) + "',"
    sql += "'" + str(output_dict['status']) + "',"
    sql += "'" + str(output_dict['stopPrice']) + "',"
    sql += "'" + str(output_dict['symbol']) + "',"
    sql += "'" + str(output_dict['timeInForce']) + "',"
    sql += "'" + str(output_dict['type']) + "',"
    sql += "'" + str(output_dict['updateTime']) + "',"
    sql += "'" + str(output_dict['workingType']) + "');"
    print(sql) 
    result = exec_sql(sql = sql , sql_command = "insert", error_message = "insert order_hist")
    print("result insert is: " + str(result))


orders_hist()