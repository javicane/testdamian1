from binance_d.requestclient import RequestClient
from binance_d.constant.test import *
import types
import sys
from decimal import Decimal
from binance_d.base.printobject import *

from binance_d.model.constant import *

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

def get_dict(data):
    '''
    # output: my_list(list of dicts):  
    #output = request_client.get_income_history(symbol, incomeType=IncomeType, startTime=1661950896257, limit=2) 
    #output: [<binance_d.model.income.Income object at 0x7f38d57b4b20>]
    #my_list:  [{'asset': 'ADA', 'income': '-0.42642078', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661961600000'}]
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


def damian_get_income_history(symbol="ADAUSD_PERP"):
    #https://binance-docs.github.io/apidocs/delivery/en/#get-income-history-user_data
    #GET /dapi/v1/income (HMAC SHA256)
    #
    #Weight: 20
    #
    #Parameters:
    #
    #Name	Type	Mandatory	Description
    #symbol	STRING	NO	
    #incomeType	STRING	NO	"TRANSFER","WELCOME_BONUS", "FUNDING_FEE", "REALIZED_PNL", "COMMISSION", "INSURANCE_CLEAR", and "DELIVERED_SETTELMENT"
    #startTime	LONG	NO	Timestamp in ms to get funding from INCLUSIVE.
    #endTime	LONG	NO	Timestamp in ms to get funding until INCLUSIVE.
    #limit	INT	NO	Default 100; max 1000
    #recvWindow	LONG	NO	
    #timestamp	LONG	YES	
    #If incomeType is not sent, all kinds of flow will be returned
    #"trandId" is unique in the same "incomeType" for a user
    #The interval between startTime and endTime can not exceed 200 days:
    #If startTime and endTime are not sent, the last 200 days will be returned
    #def get_income_history(self, symbol: 'str' = None, incomeType: 'IncomeType' = IncomeType.INVALID, 
    #                    startTime: 'long' = None, endTime: 'long' = None, limit: 'int' = None) -> any:
    #output = request_client.get_account_trades(symbol, limit=1,fromId=115248184)
    IncomeType = "FUNDING_FEE"
    #IncomeType = "REALIZED_PNL"
    # 1/1/2022 1641065492000
    # may 1 2022 1651433492000
    may_1_2022 = 1651433492000
    aug_1_2022 = 1659312000000 
    aug_31_2022 = 1661972400000 
    start_epoch = aug_1_2022

    #output = request_client.get_income_history(symbol, incomeType=IncomeType, startTime=1661950896257, limit=2) 
    output = request_client.get_income_history(symbol, incomeType=IncomeType, startTime=start_epoch) 
    PrintMix.print_data(output)
    sys.exit(66)
    output =  [{'asset': 'ADA', 'income': '-0.57155349', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659312000000'},]
    print("output:", output)
    my_dict = get_dict(output)
    print("my_list: ", my_dict)
    size_list = len(my_dict)
    print("size:", size_list)
    my_list = [{'asset': 'ADA', 'income': '-0.57155349', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659312000000'}, {'asset': 'ADA', 'income': '-0.51327104', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659340800000'}, {'asset': 'ADA', 'income': '-0.57178299', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659369600000'}, {'asset': 'ADA', 'income': '-0.35150429', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659398400000'}, {'asset': 'ADA', 'income': '-0.18918141', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659427200000'}, {'asset': 'ADA', 'income': '-0.7391573', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659456000000'}, {'asset': 'ADA', 'income': '-0.74574245', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659484800000'}, {'asset': 'ADA', 'income': '0.65829105', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659513600000'}, {'asset': 'ADA', 'income': '-0.37346483', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659542400000'}, {'asset': 'ADA', 'income': '-0.86156117', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659571200000'}, {'asset': 'ADA', 'income': '-0.69008292', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659600000000'}, {'asset': 'ADA', 'income': '-0.83150919', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659628800000'}, {'asset': 'ADA', 'income': '-0.90311089', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659657600000'}, {'asset': 'ADA', 'income': '-0.62969569', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659686400000'}, {'asset': 'ADA', 'income': '-0.64370792', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659715200000'}, {'asset': 'ADA', 'income': '-0.55861065', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659744000000'}, {'asset': 'ADA', 'income': '-0.56376745', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659772800000'}, {'asset': 'ADA', 'income': '-0.56377186', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659801600000'}, {'asset': 'ADA', 'income': '-0.67878225', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659830400000'}, {'asset': 'ADA', 'income': '-0.5844671', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659859200000'}, {'asset': 'ADA', 'income': '-0.55344505', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659888000000'}, {'asset': 'ADA', 'income': '-0.44386274', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659916800000'}, {'asset': 'ADA', 'income': '-0.09321282', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659945600000'}, {'asset': 'ADA', 'income': '-0.52962412', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1659974400000'}, {'asset': 'ADA', 'income': '-0.34550366', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660003200000'}, {'asset': 'ADA', 'income': '-0.22639253', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660032000000'}, {'asset': 'ADA', 'income': '0.38878337', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660060800000'}, {'asset': 'ADA', 'income': '-0.31152518', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660089600000'}, {'asset': 'ADA', 'income': '-0.47906883', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660118400000'}, {'asset': 'ADA', 'income': '-0.49012271', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660147200000'}, {'asset': 'ADA', 'income': '-0.21786865', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660176000000'}, {'asset': 'ADA', 'income': '-0.01908856', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660204800000'}, {'asset': 'ADA', 'income': '-0.19716332', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660233600000'}, {'asset': 'ADA', 'income': '-0.58059214', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660262400000'}, {'asset': 'ADA', 'income': '-0.53285049', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660291200000'}, {'asset': 'ADA', 'income': '-0.58130784', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660320000000'}, {'asset': 'ADA', 'income': '-0.39419791', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660348800000'}, {'asset': 'ADA', 'income': '-0.0966743', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660377600000'}, {'asset': 'ADA', 'income': '-0.04872414', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660406400000'}, {'asset': 'ADA', 'income': '-0.18770781', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660435200000'}, {'asset': 'ADA', 'income': '-0.1657802', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660492800000'}, {'asset': 'ADA', 'income': '-0.37048092', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660521600000'}, {'asset': 'ADA', 'income': '-0.87689841', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660550400000'}, {'asset': 'ADA', 'income': '-0.20139058', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660579200000'}, {'asset': 'ADA', 'income': '-0.91487813', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660608000000'}, {'asset': 'ADA', 'income': '-0.74931876', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660636800000'}, {'asset': 'ADA', 'income': '-0.71082558', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660665600000'}, {'asset': 'ADA', 'income': '-0.76475838', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660694400000'}, {'asset': 'ADA', 'income': '-0.81050966', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660723200000'}, {'asset': 'ADA', 'income': '-1.25048993', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660752000000'}, {'asset': 'ADA', 'income': '-0.883711', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660780800000'}, {'asset': 'ADA', 'income': '-1.164192', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660809600000'}, {'asset': 'ADA', 'income': '-0.55697099', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660838400000'}, {'asset': 'ADA', 'income': '-0.84936469', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660867200000'}, {'asset': 'ADA', 'income': '4.13110634', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660896000000'}, {'asset': 'ADA', 'income': '5.03761906', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660924801000'}, {'asset': 'ADA', 'income': '-2.09375517', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660953600000'}, {'asset': 'ADA', 'income': '2.45787657', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1660982400000'}, {'asset': 'ADA', 'income': '4.40407634', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661011200000'}, {'asset': 'ADA', 'income': '8.82521692', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661040000000'}, {'asset': 'ADA', 'income': '-3.28554848', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661068800000'}, {'asset': 'ADA', 'income': '4.06801601', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661097600000'}, {'asset': 'ADA', 'income': '1.39990603', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661126400000'}, {'asset': 'ADA', 'income': '2.48455674', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661155200000'}, {'asset': 'ADA', 'income': '3.2678039', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661184000000'}, {'asset': 'ADA', 'income': '2.03700008', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661212800000'}, {'asset': 'ADA', 'income': '1.01440155', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661241600000'}, {'asset': 'ADA', 'income': '1.92954125', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661270400000'}, {'asset': 'ADA', 'income': '0.09544535', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661299200000'}, {'asset': 'ADA', 'income': '2.11715343', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661328000000'}, {'asset': 'ADA', 'income': '-0.19618111', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661356800000'}, {'asset': 'ADA', 'income': '2.48582558', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661385600000'}, {'asset': 'ADA', 'income': '-2.88611377', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661414400000'}, {'asset': 'ADA', 'income': '-3.30738772', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661443200000'}, {'asset': 'ADA', 'income': '-2.57497836', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661472000000'}, {'asset': 'ADA', 'income': '-0.43389163', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661500800000'}, {'asset': 'ADA', 'income': '-0.93874662', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661529600000'}, {'asset': 'ADA', 'income': '7.38489141', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661558400000'}, {'asset': 'ADA', 'income': '3.7114531', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661587200000'}, {'asset': 'ADA', 'income': '2.35083753', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661616000000'}, {'asset': 'ADA', 'income': '1.45141058', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661644800000'}, {'asset': 'ADA', 'income': '3.523091', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661673600000'}, {'asset': 'ADA', 'income': '-1.68405432', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661702400000'}, {'asset': 'ADA', 'income': '-0.32660502', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661731200000'}, {'asset': 'ADA', 'income': '4.64796113', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661760000000'}, {'asset': 'ADA', 'income': '-0.80982632', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661788800000'}, {'asset': 'ADA', 'income': '0.0706756', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661817600000'}, {'asset': 'ADA', 'income': '0.65095651', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661846400000'}, {'asset': 'ADA', 'income': '1.07711094', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661875200000'}, {'asset': 'ADA', 'income': '-0.32220779', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661904000000'}, {'asset': 'ADA', 'income': '-0.28600375', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661932800000'}, {'asset': 'ADA', 'income': '-0.42642078', 'incomeType': 'FUNDING_FEE', 'symbol': 'ADAUSD_PERP', 'time': '1661961600000'}]
    acum = 0
    for i in my_list:
        income = i['income']
        acum = Decimal(income) + acum
    print("acum", acum) 
     
damian_get_income_history()