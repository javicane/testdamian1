from binance_d import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
# print(request_client.change_position_mode(dualSidePosition=True))
#result = request_client.post_order(symbol="btcusd_200925", side=OrderSide.BUY, ordertype=OrderType.LIMIT, price=10001, quantity=2, timeInForce=TimeInForce.GTC)

def limit_no_oco_sell_long():
    '''
    POST LIMIT ,no OCO, SELL, LONG
    result OK: {"orderId":5370806071,"symbol":"ADAUSD_PERP","pair":"ADAUSD","status":"NEW","clientOrderId":"ntBkH7G8R74PJD3kwizuMT",
    "price":"100","avgPrice":"0.00000","origQty":"1","executedQty":"0","cumQty":"0","cumBase":"0","timeInForce":"GTC","type":"LIMIT","reduceOnly":true,
    "closePosition":false,"side":"SELL","positionSide":"LONG","stopPrice":"0","workingType":"CONTRACT_PRICE","priceProtect":false,"origType":"LIMIT","updateTime":1645305366798}
    '''
    p_symbol_name = "ADAUSD_PERP"
    p_side = OrderSide.SELL
    p_order_type = OrderType.LIMIT
    p_price = "100" # must be string or '[Executing] -1111: Precision is over the maximum defined for this asset.')
    p_quantity = 1
    p_timeinforce = TimeInForce.GTC
    p_positionside = PositionSide.LONG
    result = request_client.post_order(symbol=p_symbol_name, side=p_side, ordertype=p_order_type, price=p_price, quantity=p_quantity, timeInForce=p_timeinforce, positionSide=p_positionside)
    print("result raw: " + str(result))
    print("###")
    PrintBasic.print_obj(result)

def limit_no_oco_buy_long(p_price, p_size):
    '''
    #POST LIMIT, no OCO, BUY, LONG
    result de una orden LIMIT BUY LONG pero no OCO:
    method:POST
    post_body:{}
    url:/dapi/v1/order?symbol=ADAUSD_PERP&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.666&positionSide=LONG&recvWindow=60000&timestamp=1645302840523&signature=7c807a8cec088eef81544d15442804db5ba574b6e4d4f8abadbb492d82d480d9
    =====================
    {"orderId":5370582891,"symbol":"ADAUSD_PERP","pair":"ADAUSD",
     "status":"NEW","clientOrderId":"omicpIA4jAqLrWotqOWsta",
     "price":"0.66600","avgPrice":"0.00000","origQty":"1",
     "executedQty":"0","cumQty":"0","cumBase":"0",
     "timeInForce":"GTC","type":"LIMIT","reduceOnly":false,"closePosition":false,
     "side":"BUY","positionSide":"LONG","stopPrice":"0","workingType":"CONTRACT_PRICE",
     "priceProtect":false,"origType":"LIMIT","updateTime":1645302842202}
    '''
    #input("in limit_no_oco_buy_long, pec")
    p_symbol_name = "ADAUSD_PERP"
    p_side = OrderSide.BUY
    p_order_type = OrderType.LIMIT
    p_price = str(p_price) # must be string or '[Executing] -1111: Precision is over the maximum defined for this asset.')
    p_quantity = p_size
    p_timeinforce = TimeInForce.GTC
    p_positionside = PositionSide.LONG
    result = request_client.post_order(symbol=p_symbol_name, side=p_side, ordertype=p_order_type, price=p_price, quantity=p_quantity, timeInForce=p_timeinforce, positionSide=p_positionside)
    print("result raw: " + str(result))
    #input("in limit_no_oco_buy_long, pec")
    print("###")
    PrintBasic.print_obj(result)
    return result

def silent_limit_no_oco_buy_long(p_price, p_size):
    '''
    #POST LIMIT, no OCO, BUY, LONG
    result de una orden LIMIT BUY LONG pero no OCO:
    method:POST
    post_body:{}
    url:/dapi/v1/order?symbol=ADAUSD_PERP&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.666&positionSide=LONG&recvWindow=60000&timestamp=1645302840523&signature=7c807a8cec088eef81544d15442804db5ba574b6e4d4f8abadbb492d82d480d9
    =====================
    {"orderId":5370582891,"symbol":"ADAUSD_PERP","pair":"ADAUSD",
     "status":"NEW","clientOrderId":"omicpIA4jAqLrWotqOWsta",
     "price":"0.66600","avgPrice":"0.00000","origQty":"1",
     "executedQty":"0","cumQty":"0","cumBase":"0",
     "timeInForce":"GTC","type":"LIMIT","reduceOnly":false,"closePosition":false,
     "side":"BUY","positionSide":"LONG","stopPrice":"0","workingType":"CONTRACT_PRICE",
     "priceProtect":false,"origType":"LIMIT","updateTime":1645302842202}
    '''
    #input("in limit_no_oco_buy_long, pec")
    p_symbol_name = "ADAUSD_PERP"
    p_side = OrderSide.BUY
    p_order_type = OrderType.LIMIT
    p_price = str(p_price) # must be string or '[Executing] -1111: Precision is over the maximum defined for this asset.')
    p_quantity = p_size
    p_timeinforce = TimeInForce.GTC
    p_positionside = PositionSide.LONG
    result = request_client.post_order(symbol=p_symbol_name, side=p_side, ordertype=p_order_type, price=p_price, quantity=p_quantity, timeInForce=p_timeinforce, positionSide=p_positionside)
    #print("result raw: " + str(result))
    #input("in limit_no_oco_buy_long, pec")
    #print("###")
    #PrintBasic.print_obj(result)
    #result_raw = str(result)
    #return result_raw
    return result

'''
###
def post_order(self, symbol: 'str', side: 'OrderSide', ordertype: 'OrderType', 
                timeInForce: 'TimeInForce' = TimeInForce.INVALID, quantity: 'float' = None,
                reduceOnly: 'boolean' = None, price: 'float' = None,
                newClientOrderId: 'str' = None, stopPrice: 'float' = None, 
                workingType: 'WorkingType' = WorkingType.INVALID, closePosition: 'boolean' = None,
                positionSide: 'PositionSide' = PositionSide.INVALID, callbackRate: 'float' = None,
                activationPrice: 'float' = None, newOrderRespType: 'OrderRespType' = OrderRespType.INVALID) -> any:

###
POST para 
place-order para OCO en LONG (positionSide":"LONG) :
extraida con developer tools del browser creando una orden OCO con TP:
{"strategyType":"OTO","subOrderList":[
    {"strategySubId":1,"firstDrivenId":0,"secondDrivenId":0,"side":"BUY","positionSide":"LONG",
     "symbol":"ADAUSD_PERP","type":"LIMIT","timeInForce":"GTC","quantity":1,"price":"0.5",
     "securityType":"COIN_FUTURES"},
     {"side":"SELL","positionSide":"LONG","symbol":"ADAUSD_PERP","securityType":"COIN_FUTURES",
      "firstTrigger":"PLACE_ORDER","firstDrivenOn":"PARTIALLY_FILLED_OR_FILLED",
      "timeInForce":"GTE_GTC","quantity":1,"strategySubId":2,"firstDrivenId":1,
      "secondDrivenId":0,"stopPrice":"1","workingType":"MARK_PRICE","type":"TAKE_PROFIT_MARKET","priceProtect":true}]}
'''
#limit_no_oco_buy_long(0.667, 1)