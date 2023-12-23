from binance_d.requestclient import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
symbol_name = "ADAUSD_PERP"
#result = request_client.get_mark_price(symbol="btcusd_200925")
result = request_client.get_mark_price(symbol=symbol_name)
print("result", result)
print("======= Mark Price =======")
PrintMix.print_data(result)
print("==========================")
