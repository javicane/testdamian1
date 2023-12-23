from binance_d.requestclient import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, funcname, update_to_in_position, get_trigger_price_to_close, dump_radar_list


request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

def get_mark_price():
    symbol_name = "ADAUSD_PERP"
    #result = request_client.get_mark_price(symbol="btcusd_200925")
    result = request_client.get_mark_price(symbol=symbol_name)
    #pr int("======= Mark Price =======")
    #PrintMix.print_data(result)
    #output = PrintList.print_object_list_damian(result)
    #print("==========================")
    my_list = []
    for idx, row in enumerate(result):
        #print("data number " + (str(idx)) + " :")
        my_dict = create_dict_from_output(row)
        my_list.append(my_dict)
    print("my_dict:", my_dict)
    mark_price = my_dict['markPrice']
    #print("my_list:", my_list)
    #my_dict: {'estimatedSettlePrice': '0.29182538', 'indexPrice': '0.29213939', 'markPrice': '0.29202977', 'pair': 'ADAUSD', 'symbol': 'ADAUSD_PERP', 'time': '1691104800000'}
    #my_list: [{'estimatedSettlePrice': '0.29182538', 'indexPrice': '0.29213939', 'markPrice': '0.29202977', 'pair': 'ADAUSD', 'symbol': 'ADAUSD_PERP', 'time': '1691104800000'}]
    print("mark_price:", mark_price)
    return float(mark_price)

mark_price = get_mark_price()
print("returned mark_price:", mark_price, type(mark_price))
print(round(mark_price, 4))

