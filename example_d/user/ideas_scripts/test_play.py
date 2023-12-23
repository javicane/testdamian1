import pdb
pdb.set_trace()
from binance_d.requestclient import RequestClient
a = "0"
b = float(a)
print("b: " + str(b))
if b == 0:
    print("b es cero")
a = "-0.1"
b = float(a)
print("b: " + str(b))
if b != 0:
    print("distinto")

def match_order_id(radar_list, event_order_id):
    flag_found = False
    radar_list_dict = {}
    for radar_list_dict in radar_list:
        if str(radar_list_dict['order_id']) == event_order_id:
            flag_found = True
            break
    return flag_found, radar_list_dict

my_dict = dict(order_id=1,order_status='IN_POSITION',order_id_to_close=333,trigger_price_to_put_in_position=0.89,
                       trigger_price_to_close=0.893, original_quantity=97)
my_list = []
my_list.append(my_dict)
event_dict = { 
                      'clientOrderId': 'dummy',
                      'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'NEW', 
                      'orderId': '333', 'orderStatus': 'NEW', 
                      'origQty': '1.0', 'price': '0.1', 'realizedprofit': '0.0'
                      }
import dis
dis.dis(match_order_id)