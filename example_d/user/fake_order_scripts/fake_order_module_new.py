import sys
from binance_d.requestclient import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *
from binance_d.example_d.user.helpers_scripts.helpers_module import funcname
from binance_d.impl.utils.timeservice import get_current_timestamp
from datetime import datetime

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)


def create_fake_buy_order(request_client):
    '''
    '''
    print("in " + funcname() + ", BEGIN CREATE CREATE")
    p_symbol_name = "ADAUSD_PERP"
    p_side = OrderSide.BUY
    p_order_type = OrderType.LIMIT
    p_price = str(0.1 ) # must be string or '[Executing] -1111: Precision is over the maximum defined for this asset.')
    p_quantity = 1
    p_timeinforce = TimeInForce.GTC
    p_positionside = PositionSide.LONG
    print("in " + funcname() + ", call request_client.post_order")
    clientorderid_value = "fakeordernew"# + str(get_current_timestamp())
    result = request_client.post_order(symbol=p_symbol_name, side=p_side, ordertype=p_order_type, price=p_price, quantity=p_quantity, timeInForce=p_timeinforce, positionSide=p_positionside, newClientOrderId=clientorderid_value)
    print("in " + funcname() + ", END CREATE CREATE")
    print("result raw: " + str(result))
    #input("in limit_no_oco_buy_long, pec")
    #print("###")
    PrintBasic.print_obj(result)
    #result_raw = str(result)
    #return result_raw
    #return result

def modify_fake_order(request_client, p_price):
    '''
    except in run_fake_order_new: (<class 'binance_d.exception.binanceapiexception.BinanceApiException'>,
    BinanceApiException('ExecuteError', '[Executing] -4197: No need to modify the order.'), <traceback object at 0x7f733ad39780>)
    '''
    print("in " + funcname() + ", BEGIN CREATE CREATE")
    p_symbol_name = "ADAUSD_PERP"
    p_side = OrderSide.BUY
    p_quantity = 1
    print("in " + funcname() + ", call request_client.put_order")
    clientorderid_value = "fakeordernew"# + str(get_current_timestamp())
    p_price = str(p_price) # must be string or '[Executing] -1111: Precision is over the maximum defined for this asset.')
    result = request_client.put_order(side=p_side, symbol=p_symbol_name, price=p_price, quantity=p_quantity, origClientOrderId=clientorderid_value)

    print("in " + funcname() + ", END CREATE CREATE")
    print("result raw: " + str(result))
    PrintBasic.print_obj(result)
    result_raw = str(result)

def run_fake_order(request_client):
    print("==== in " + funcname() + ", call try create_fake_buy_order, create_fake_buy_order BEGIN")
    # lo corro 2 veces para asegurar que corra bien  porque no se cual es el valor anterior, sino da esto:
    #      except in run_fake_order_new: (<class 'binance_d.exception.binanceapiexception.BinanceApiException'>,
    # BinanceApiException('ExecuteError', '[Executing] -4197: No need to modify the order.'), <traceback object at 0x7f733ad39780>)
    try:
        #create_fake_buy_order(request_client)
        #price = int(datetime.now().strftime("%H%M%S"))
        price = int(datetime.now().strftime("%M%S%m"))
        price =  0.1 + price / 10000000
        #price = + price
        print("price: " + str(price))

        #modify_fake_order(request_client, price)
    except:
        print("except in run_fake_order_new: " + str(sys.exc_info()))
        #if "[Executing] -4197: No need to modify the order." in str(sys.exc_info()):
        #    try:
        #        modify_fake_order(request_client, 0.11)
        #    except:
        #        print("except in run_fake_order_new try 2: " + str(sys.exc_info()))
        #    finally:
        #        print("try 2 OK")
    finally:
        print("==== in " + funcname() + ", call try create_fake_buy_order, create_fake_buy_order END")

run_fake_order(request_client)