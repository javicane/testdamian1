import sys
#sys.path.append("C:/binance/futures/futures")
from binance_d.requestclient import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output

print("#### in example_d.trade.get_position.py")
print("#### in example_d.trade.get_position.py g_api_key, g_secret_key: " + str(g_api_key) + ", " + str(g_secret_key)) 
request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
print("#### in example_d.trade.get_position.py request_client: " + str(request_client))
input("#### in example_d.trade.get_position.py call request_client.get_position(), pec")
# binance_d.impl.restapirequestimpl.RestApiRequestImpl.get_position define hardcoded url /dapi/v1/positionRisk")
result = request_client.get_position()
#print("result: " + str(result))

print("#### in example_d.trade.get_position.py result is type:" + str(type(result)))
#PrintMix.print_data(result)
##### in example_d.trade.get_position.py result is type:<class 'list'>
#i dict: {'entryPrice': '0.0', 'isAutoAddMargin': 'True', 'isolatedMargin': '0.0', 'leverage': '20.0', 'liquidationPrice': '0.0', 'marginType': 'cross', 'markPrice': '0.78346', 'maxQty': '250000.0', 'positionAmt': '0.0', 'positionSide': 'BOTH', 'symbol': 'ADAUSD_PERP', 'unrealizedProfit': '0.0'}
#i dict: {'entryPrice': '0.89230367', 'isAutoAddMargin': 'True', 'isolatedMargin': '0.0', 'leverage': '20.0', 'liquidationPrice': '0.46101131', 'marginType': 'cross', 'markPrice': '0.78346', 'maxQty': '250000.0', 'positionAmt': '97.0', 'positionSide': 'LONG', 'symbol': 'ADAUSD_PERP', 'unrealizedProfit': '-151.02380433'}
#i dict: {'entryPrice': '0.0', 'isAutoAddMargin': 'True', 'isolatedMargin': '0.0', 'leverage': '20.0', 'liquidationPrice': '0.0', 'marginType': 'cross', 'markPrice': '0.78346', 'maxQty': '250000.0', 'positionAmt': '0.0', 'positionSide': 'SHORT', 'symbol': 'ADAUSD_PERP', 'unrealizedProfit': '0.0'}
my_list = []
for idx, row in enumerate(result):
    #print("data number " + (str(idx)) + " :")
    my_dict = create_dict_from_output(row)
    my_list.append(my_dict)
    #print("my_dict: " + str(my_dict))
#print("my_list: ", my_list)
# example of my_list, siempre devuelve minimamente estas 3 positions, en este ejemplo la ultima es la que interesa porque tiene positionAmt != 0.0
#{'entryPrice': '0.0', 'isAutoAddMargin': 'True', 'isolatedMargin': '0.0', 'leverage': '20.0', 'liquidationPrice': '0.0', 'marginType': 'cross', 'markPrice': '0.38347434', 'maxQty': '250000.0', 'positionAmt': '0.0', 'positionSide': 'BOTH', 'symbol': 'ADAUSD_PERP', 'unrealizedProfit': '0.0'}
#{'entryPrice': '0.0', 'isAutoAddMargin': 'True', 'isolatedMargin': '0.0', 'leverage': '20.0', 'liquidationPrice': '0.0', 'marginType': 'cross', 'markPrice': '0.38347434', 'maxQty': '250000.0', 'positionAmt': '0.0', 'positionSide': 'LONG', 'symbol': 'ADAUSD_PERP', 'unrealizedProfit': '0.0'}
#{'entryPrice': '0.38182559', 'isAutoAddMargin': 'True', 'isolatedMargin': '0.0', 'leverage': '20.0', 'liquidationPrice': '0.52095422', 'marginType': 'cross', 'markPrice': '0.38347434', 'maxQty': '250000.0', 'positionAmt': '-100.0', 'positionSide': 'SHORT', 'symbol': 'ADAUSD_PERP', 'unrealizedProfit': '-11.26032831'}
# en position SELL siempre el positionAmt es negativo
for i in my_list:
    if i['symbol'] == "ADAUSD_PERP" and abs(float(i['positionAmt'])) > 0: 
        print("positionAmt raw:", i['positionAmt'])
        # to float 
        position_size = float(i['positionAmt'])
        print("position_size:", position_size)
        print(i)
        print("....")     