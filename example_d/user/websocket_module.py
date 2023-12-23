#from line_profiler import LineProfiler
#lprofiler = LineProfiler()
#import pdb
#pdb.set_trace()

import sys
import logging
import json
import types
sys.path.append('/home/damian/.local/lib/python3.8/site-packages/')
#from binance_d import RequestClient
import memcache
from binance_d.subscriptionclient import SubscriptionClient
from binance_d.constant.test import *
from binance_d.model import *
from binance_d.exception.binanceapiexception import BinanceApiException

from binance_d.base.printobject import *
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, check_existence_radar_list_in_disc, list_pivots_in_radar_list_in_disk, funcname
from binance_d.example_d.user.process_event_scripts.process_module import process_event
from time import sleep
from binance_d.impl.websocketwatchdog import request_client
from binance_d.impl.websocketwatchdog import listen_key
from binance_d.example_d.user.process_event_scripts.process_account_update_event_module import process_account_update 

#request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
#listen_key = request_client.start_user_data_stream()
#print("#### in example_d.user.subscribeuserdata.py listenKey: ", listen_key)

print("websocket_module.py line 26 scope global")
# Crear una conexión al servidor Memcached (asegúrate de que Memcached esté en ejecución)
memcached_conn = None 
try:
    if memcached_conn is None:
        memcached_conn = memcache.Client(['localhost:11211'], debug=0)
except:
    print("except memcached not working:", sys.exc_info())

try:
    if memcached_conn is not None:
        memcached_conn.set('check_run_fake_order', "INIT")
except:
        print("except in memcached set(check_run_fake_order):", sys.exc_info())

def first_steps():
    print("in websocket_module.first_steps listen_key: " + str(listen_key))
    #input("pec")
    #sys.exit(67)

def websocket_steps():
    # Start user data stream
    #request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    #listen_key = request_client.start_user_data_stream()
    #print("#### in example_d.user.subscribeuserdata.py listenKey: ", listen_key)
    #input("#### in example_d.user.subscribeuserdata.py call keep_user_data_stream(), pec")
    # Keep user data stream
    result = request_client.keep_user_data_stream()
    print("#### in example_d.user.subscribeuserdata.py Result keep user data stream: ", result)

    # Close user data stream
    #result = request_client.close_user_data_stream()
    #print("Result close user data stream: ", result)
    #input("close user data stream")
    #print("#### in example_d.user.subscribeuserdata.py call sub_client = SubscriptionClient(api_key=g_api_key, secret_key=g_secret_key, pec")

    # aca controlo el threshold para cerrar el websocket por inactividad 
    ws_threshold = 86400001   # 24 hours
    sub_client = SubscriptionClient(api_key=g_api_key, secret_key=g_secret_key, receive_limit_ms=ws_threshold)


    #input("start websockets ? , pec")
    #print("start websockets ? , pec")
    sub_client.subscribe_user_data_event(listen_key, callback, error)
    sub_client.subscribe_mark_price_event("adausd_perp", callback, error)
    
    '''
    try:
        listen_key = request_client.start_user_data_stream()
        sub_client.subscribe_user_data_event(listen_key, callback, error)
       # sub_client.subscribe_mark_price_event("adausd_perp", callback, error)
        for i in range(2, 60*60*24):
            #if i % 60*60 == 0:
            if i % 3*60 == 0:
                result = request_client.keep_user_data_stream()
                print("#### in example_d.user.websocket_module Result keep user data stream: ", result)
                #get_spot_client().renew_listen_key(listen_key)
            #if i % 61 == 0:
            if i % 21 == 0:
                #click.secho(f"Socket ок, {int(i/61)} min.", fg="yellow")
                print(f"Socket ок, {int(i/61)} min.")
            sleep(2)        
    except:
        print("except in websocket :" + str(sys.exc_info()))
    finally:
        print("this is finally")
    '''


def setup_logger():
    logger = logging.getLogger("binance-client")
    logger.setLevel(level=logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)


def callback(data_type: 'SubscribeMessageType', event: 'any'):
    print("#### #### #### callback BEGIN")
    if data_type == SubscribeMessageType.RESPONSE:
        print("Event ID: ", event)
    elif  data_type == SubscribeMessageType.PAYLOAD:
        #PrintBasic.print_obj(event)
        #'''
        print("in callback, data_type received is PAYLOAD")
        if(event.eventType == "ACCOUNT_UPDATE"):
            print("in callback, ACCOUNT_UPDATE Event Type: ", event.eventType)
            print("in callback, ACCOUNT_UPDATE event is:", event)
            print("in callback, ACCOUNT_UPDATE call process_account_update")
            process_account_update(event) 
        elif(event.eventType == "ORDER_TRADE_UPDATE"):
            print("++++ in callback ORDER_TRADE_UPDATE payload BEGIN")
            event_dict = create_dict_from_output(event)
            print("in callback, ORDER_TRADE_UPDATE event_dict: " + str(event_dict))
            # event_dict: {'activationPrice': 'None', 'asksNotional': '1.0', 'avgPrice': '0.0', 'bidsNotional': '346.30322511', 'callbackRate': 'None', 
            # 'clientOrderId': 'web_eS3mZZJNK8Afy6qVY5LA', 'commissionAmount': 'None', 'commissionAsset': 'None', 'cumulativeFilledQty': '0.0', 
            # 'eventTime': '1651364195659', 'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'NEW', 'isClosePosition': 'False', 'isMarkerSide': 'False',
            #  'isReduceOnly': 'False', 'lastFilledPrice': '1.0', 'lastFilledQty': '0.0', 'orderId': '6183269971', 'orderStatus': 'NEW', 'orderTradeTime': '1651364195651',
            #  'origQty': '2.0', 'positionSide': 'LONG', 'price': '0.222', 'side': 'BUY', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 'timeInForce': 'GTC', 'tradeID': '0',
            #  'transactionTime': '1651364195652', 'type': 'LIMIT', 'workingType': 'CONTRACT_PRICE'}
            #print("in callback, ORDER_TRADE_UPDATE, Event Type: ", event.eventType)
            print("in callback, ORDER_TRADE_UPDATE, Event time: ", event.eventTime)
            #print("in callback, ORDER_TRADE_UPDATE, call process_event")
            result = process_event(event_dict) # result variable is useless
            print("++++  in callback, ORDER_TRADE_UPDATE payload END")
            if not event.activationPrice is None:
                print("Activation Price for Trailing Stop: ", event.activationPrice)
            if not event.callbackRate is None:
                print("Callback Rate for Trailing Stop: ", event.callbackRate)
            print("++++++++++++++++++")
        elif(event.eventType == "listenKeyExpired"):
            print("Event: ", event.eventType)
            print("Event time: ", event.eventTime)
            print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
            print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
            print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
        elif(event.eventType == "markPriceUpdate"):
            #print("EVent type should be markPriceUpdate: ", event.eventType) 
            #PrintBasic.print_obj(event)
    
            print("markPriceUpdate Event, time, symbol, markprice: ", event.eventTime, event.symbol, event.markPrice)
            if memcached_conn is not None:
                try:
                    memcached_conn.set('markprice', str(event.markPrice))
                except:
                    print("except in memcached set(markprice):", sys.exc_info())
            #print("Symbol: ", event.symbol)
            #print("Mark price: ", event.markPrice)
            #print("================")
    else:
        print("Unknown Data:")
    print("#### #### #### callback END")

def error(e: 'BinanceApiException'):
    print(e.error_code + e.error_message)

def perror():
    print("error is :" + str(sys.exc_info()))


def main():
    first_steps()
    #setup_logger() 
    websocket_steps()
    print("marca final")

#lprofiler.add_function(first_steps)
#lprofiler.add_function(callback)
#lprofiler.add_function(error)
#lprofiler.add_function(websocket_steps) #<------aca vamos agregando las funciones que queremos profilear
#lp_wrapper = lprofiler(main)  #<----aca ejecutamos la funcion principal( no debe tener parametros)
#lp_wrapper()
#lprofiler.print_stats()

if __name__ == "__main__":
#    #pdb.set_trace()
    main()



#wss://dstream.binance.com