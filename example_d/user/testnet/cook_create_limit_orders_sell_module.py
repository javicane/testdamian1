from binance_d import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *

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

limit_no_oco_sell_long(0.6262,3)
