#from binance_d import RequestClient
from binance_d.requestclient import RequestClient
#from binance_d.subscriptionclient import SubscriptionClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *


def cancel_order_by_id_and_symbol(orderid, symbol):
   # orderid = "6182795716"
   # symbol = "ADAUSD_PERP"
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    result = request_client.cancel_order(symbol=symbol, orderId=orderid)
    #PrintBasic.print_obj(result)
    return result

