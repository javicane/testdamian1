import sys
sys.path.append("C:/binance/futures/futures")
from binance_d import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *

print("#### in example_d.trade.get_position.py")
print("#### in example_d.trade.get_position.py g_api_key, g_secret_key: " + str(g_api_key) + ", " + str(g_secret_key)) 
request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
print("#### in example_d.trade.get_position.py request_client: " + str(request_client))
input("#### in example_d.trade.get_position.py call request_client.get_position(), pec")
# binance_d.impl.restapirequestimpl.RestApiRequestImpl.get_position define hardcoded url /dapi/v1/positionRisk")
result = request_client.get_position()
#print("result: " + str(result))

print("#### in example_d.trade.get_position.py result is type:" + str(type(result)))
for i in result:
    print("i dict:" + str(i))
    #        if i['symbol'] == "ADAUSD_PERP":
    #            if i['positionAmt'] != '0':
    #                print("i: " + str(i))

        #sys.exit(66)
for item in result:
    print("#### in example_d.trade.get_position.py item is type: " + str(type(item)))
    #print(str(item))
    sys.exit(66)
    #nada = 1
#sys.exit(66)
#PrintMix.print_data(result)
