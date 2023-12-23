from binance_d.requestclient import RequestClient
from binance_d.constant.test import *
import types
import sys
from binance_d.base.printobject import *
from binance_d.model.constant import *
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, funcname, update_to_in_position, get_trigger_price_to_close, dump_radar_list

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

def get_order_status(order_id):
    """
      get_order(self, symbol: 'str', orderId: 'long' = None, origClientOrderId: 'str' = None) -> any:
       Query Order (USER_DATA)
        GET /dapi/v1/order (HMAC SHA256)
        Check an order's status.
        response = call_sync(self.request_impl.get_order(symbol, orderId, origClientOrderId))

        output:  <binance_d.model.order.Order object at 0x7f9a088c3af0>
        output_dict:  {'activatePrice': 'None', 'avgPrice': '0.50969',
                       'clientOrderId': 'new_pivot1659526072408', 'closePosition': 'False', 'cumBase': '98.09884438', 
                       'executedQty': '5.0', 'orderId': '7249661216', 'origQty': '5.0', 'origType': 'LIMIT', 
                       'positionSide': 'LONG', 'price': '0.50969', 'priceRate': 'None', 'reduceOnly': 'False', 
                       'side': 'BUY', 'status': 'FILLED', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 
                       'timeInForce': 'GTC', 'type': 'LIMIT', 'updateTime': '1659529828548', 'workingType': 'CONTRACT_PRICE'}
    """
    symbol="ADAUSD_PERP"
    output = request_client.get_order(symbol, orderId=str(order_id)) 
    #print("output: ", output)
    output_dict =  create_dict_from_output(output)
    #print("output_dict: ", output_dict)
    #my_dict = get_dict(output)
    #print("my_list: ", my_dict)
    #print("result raw: " + str(output))
    #print("###")
    #PrintBasic.print_obj(output)
    return output_dict
#get_order_status(7249661216)