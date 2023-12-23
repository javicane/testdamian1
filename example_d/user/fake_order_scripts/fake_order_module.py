import sys
import time
import sys
import memcache
from binance_d.requestclient import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *
from binance_d.example_d.user.helpers_scripts.helpers_module import funcname
from binance_d.impl.utils.timeservice import get_current_timestamp

# Crear una conexión al servidor Memcached (asegúrate de que Memcached esté en ejecución)
try:
    memcached_conn = memcache.Client(['localhost:11211'], debug=0)
except:
    print("except memcached not working:", sys.exc_info())

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

def cancel_fake_order(request_client):
    print("in " + funcname() + ", BEGIN")
   # orderid = "6182795716"
    symbol = "ADAUSD_PERP"
    clientorderid_value = "fakeorder"# + str(get_current_timestamp())
    result = request_client.cancel_order(symbol=symbol, origClientOrderId=clientorderid_value)
    #print("in " + funcname() + ", END CANCEL CANCEL")
    #PrintBasic.print_obj(result)
    #return result

def create_fake_buy_order(request_client, tseconds):
    '''
    host:https://dapi.binance.com
    json_parser:None
    method:DELETE
    post_body:
    url:/dapi/v1/order?symbol=ADAUSD_PERP&origClientOrderId=fakeorder&recvWindow=60000&timestamp=1652273471156&signature=f2362521cceb33dd972b1d5a4bced79b8a0675e36e04501a6997f7f35f216612
    in base.printobject.PrintMix, silent
    =====================
    {"orderId":6351361240,"symbol":"ADAUSD_PERP","pair":"ADAUSD","status":"CANCELED","clientOrderId":"fakeorder","price":"0.10000","avgPrice":"0.00000","origQty":"1",
    "executedQty":"0","cumQty":"0","cumBase":"0","timeInForce":"GTC","type":"LIMIT","reduceOnly":false,"closePosition":false,"side":"BUY",
    "positionSide":"LONG","stopPrice":"0","workingType":"CONTRACT_PRICE","priceProtect":false,"origType":"LIMIT","updateTime":1652273472933}
    '''
    print("in " + funcname() + ", BEGIN")
    p_symbol_name = "ADAUSD_PERP"
    p_side = OrderSide.BUY
    p_order_type = OrderType.LIMIT
    p_price = str(0.1 ) # must be string or '[Executing] -1111: Precision is over the maximum defined for this asset.')
    p_quantity = 1
    p_timeinforce = TimeInForce.GTC
    p_positionside = PositionSide.LONG
    print("in " + funcname() + ", call request_client.post_order")
    clientorderid_value = "fakeorder"# + str(get_current_timestamp())
    # debug, not execute fake
    if tseconds >= 55:
        result = request_client.post_order(symbol=p_symbol_name, side=p_side, ordertype=p_order_type, price=p_price, quantity=p_quantity, timeInForce=p_timeinforce, positionSide=p_positionside, newClientOrderId=clientorderid_value)
    

    #print("in " + funcname() + ", END CREATE CREATE")
    #print("result raw: " + str(result))
    #input("in limit_no_oco_buy_long, pec")
    #print("###")
    #PrintBasic.print_obj(result)
    #result_raw = str(result)
    #return result_raw
    #return result

def create_fakenew_buy_order(request_client):
    '''
    host:https://dapi.binance.com
    json_parser:None
    method:DELETE
    post_body:
    url:/dapi/v1/order?symbol=ADAUSD_PERP&origClientOrderId=fakeorder&recvWindow=60000&timestamp=1652273471156&signature=f2362521cceb33dd972b1d5a4bced79b8a0675e36e04501a6997f7f35f216612
    in base.printobject.PrintMix, silent
    =====================
    {"orderId":6351361240,"symbol":"ADAUSD_PERP","pair":"ADAUSD","status":"CANCELED","clientOrderId":"fakeorder","price":"0.10000","avgPrice":"0.00000","origQty":"1",
    "executedQty":"0","cumQty":"0","cumBase":"0","timeInForce":"GTC","type":"LIMIT","reduceOnly":false,"closePosition":false,"side":"BUY",
    "positionSide":"LONG","stopPrice":"0","workingType":"CONTRACT_PRICE","priceProtect":false,"origType":"LIMIT","updateTime":1652273472933}
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
    #print("result raw: " + str(result))
    #input("in limit_no_oco_buy_long, pec")
    #print("###")
    #PrintBasic.print_obj(result)
    #result_raw = str(result)
    #return result_raw
    #return result

def modify_fake_order(request_client):
    '''
    host:https://dapi.binance.com
    json_parser:None
    method:DELETE
    post_body:
    url:/dapi/v1/order?symbol=ADAUSD_PERP&origClientOrderId=fakeorder&recvWindow=60000&timestamp=1652273471156&signature=f2362521cceb33dd972b1d5a4bced79b8a0675e36e04501a6997f7f35f216612
    in base.printobject.PrintMix, silent
    =====================
    {"orderId":6351361240,"symbol":"ADAUSD_PERP","pair":"ADAUSD","status":"CANCELED","clientOrderId":"fakeorder","price":"0.10000","avgPrice":"0.00000","origQty":"1",
    "executedQty":"0","cumQty":"0","cumBase":"0","timeInForce":"GTC","type":"LIMIT","reduceOnly":false,"closePosition":false,"side":"BUY",
    "positionSide":"LONG","stopPrice":"0","workingType":"CONTRACT_PRICE","priceProtect":false,"origType":"LIMIT","updateTime":1652273472933}
    '''
    print("in " + funcname() + ", BEGIN CREATE CREATE")
    p_symbol_name = "ADAUSD_PERP"
    #p_side = OrderSide.BUY
    #p_order_type = OrderType.LIMIT
    p_price = str(0.1 ) # must be string or '[Executing] -1111: Precision is over the maximum defined for this asset.')
    p_quantity = 1
    #p_timeinforce = TimeInForce.GTC
    #p_positionside = PositionSide.LONG
    print("in " + funcname() + ", call request_client.put_order")
    clientorderid_value = "fakeordernew"# + str(get_current_timestamp())
    result = request_client.put_order(symbol=p_symbol_name, price=p_price, quantity=p_quantity, newClientOrderId=clientorderid_value)
    print("in " + funcname() + ", END CREATE CREATE")
    print("result raw: " + str(result))
    #input("in limit_no_oco_buy_long, pec")
    #print("###")
    PrintBasic.print_obj(result)
    result_raw = str(result)
    #return result_raw
    #return result

def run_fake_order(request_client, tseconds):
    print("in " + funcname() + ", call try create_fake_buy_order BEGIN")
    print("in " + funcname() + ", tseconds:", tseconds)
    #if tseconds > 25:
    #    print("in " + funcname() + ", tseconds > 25, sleep(3)")
    #    time.sleep(3)
    try:
        create_fake_buy_order(request_client, tseconds)
        print("create_fake_buy_order OK")    
        try:
            memcached_conn.set('check_run_fake_order', 'OK')
        except:
            print("in fake_order_module.run_fake_order except in memcached set(check_run_fake_order OK):", sys.exc_info())
    except:
        print("in fake_order_module.run_fake_order except in run_fake_order: ", sys.exc_info())
        # possible error: except in run_fake_order:  (<class 'binance_d.exception.binanceapiexception.BinanceApiException'>, BinanceApiExc
        #eption('ExecuteError', '[Executing] -1021: Timestamp for this request is outside of the recvWindow.'), <tracebac
        #k object at 0x7fcfd03f92c0>)
        exc_string = str(sys.exc_info())
        error = exc_string
        try:
            memcached_conn.set('check_run_fake_order', error)
        except:
            print("in fake_order_module.fun_fake_order except in memcached_conn.set()", exc_string)
        '''
        error = "Timestamp for this request is outside of the recvWindow"
        error2 = "Margin is insufficient"

        if error in exc_string:
            try:
                memcached_conn.set('check_run_fake_order', error)
            except:
                print("in fake_order_module.run_fake_order except in memcached set(check_run_fake_order error):", sys.exc_info())
        elif error2 in exc_string:
            try:
                memcached_conn.set('check_run_fake_order', error2)
            except:
                print("in fake_order_module.run_fake_order except in memcached set(error_except_run_fake_order):", sys.exc_info())
        else:
                #memcached_conn.set('check_run_fake_order', 'OK')
                print("in fake_order_module.run_fake_order memcached_conn.set(exc_string):", exc_string)
                error = "error"
                error = exc_string
                try:
                    memcached_conn.set('check_run_fake_order', error)
                except:
                    print("in fake_order_module.fun_fake_order except in memcached_conn.set()", exc_string)
        ''' 

    try:
        cancel_fake_order(request_client)
        print("in " + funcname() + ", cancel_fake_order OK")
        try:
            memcached_conn.set('check_run_fake_order', 'OK')
        except:
            print("in fake_order_module.run_fake_order except in memcached set(check_run_fake_order OK):", sys.exc_info())
    except:
        print("in fake_order_module.run_fake_order except in cancel_fake_order :", sys.exc_info())  