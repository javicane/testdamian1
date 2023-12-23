from binance_d.requestclient import RequestClient
from binance_d.constant.test import *
import types
import sys

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

def get_dict(data):
    '''
    # output: my_list(list of dicts):  [{'baseQty': '21.02563024', 'commission': '0.00210256', 
    # 'commissionAsset': 'ADA', 'counterPartyId': 'None', 'id': '115248184', 
    # 'isBuyer': 'True', 'isMaker': 'True', 
    # 'orderId': '6896017455', 'price': '0.47561', 
    # 'qty': '1.0', 'realizedPnl': '0.0', 
    # 'side': 'BUY', 'symbol': 'ADAUSD_PERP', 'time': '1656018344073'},
    # 
    # {'baseQty': '21.30106931', 'commission': '0.0021301', 'commissionAsset': 'ADA', 'counterPartyId': 'None', 
    # 'id': '115771797', 'isBuyer': 'False', 'isMaker': 'True', 
    # 'orderId': '6935472319', 'price': '0.46946', 
    # 'qty': '1.0', 'realizedPnl': '-0.91475072', 
    # 'side': 'SELL', 'symbol': 'ADAUSD_PERP', 'time': '1656457646502'}, {..}]
    '''
    if not data:
        print (sys._getframe().f_code.co_name + " none data")
        return -1
    #print("obj_type is TYPE_LIST")
    my_list = []
    for idx, row in enumerate(data):
        my_dict = {}
        members = [attr for attr in dir(row) if not callable(attr) and not attr.startswith("__")]
        for member_def in members:
            val_str = str(getattr(row, member_def))
            val_raw = getattr(row, member_def)
            ###
            # check if "member_def" is pointing to a function
            j = isinstance(val_raw, types.FunctionType)
            if not j:
                my_dict[member_def] = val_str
            else:
                nada = 1
                #print(member_def + " is pointing to a function " + str(type(val_raw)))
        my_list.append(my_dict)
    return my_list


def damian_get_account_trades(symbol="ADAUSD_PERP"):
   # (self, symbol: 'str', startTime: 'long' = None, endTime: 'long' = None, 
   #                     fromId: 'long' = None, limit: 'int' = None) -> any:
    #output = request_client.get_account_trades(symbol, limit=1,fromId=115248184)
    output = request_client.get_account_trades(symbol, limit=2) 
    my_dict = get_dict(output)
    print("my_list: ", my_dict)
damian_get_account_trades()