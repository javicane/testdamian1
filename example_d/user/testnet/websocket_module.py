import pdb
#pdb.set_trace()
import sys
import logging

sys.path.append('/home/damian/.local/lib/python3.8/site-packages/')
from binance_d import RequestClient
from binance_d import SubscriptionClient
from binance_d.constant.test import *
from binance_d.model import *
from binance_d.exception.binanceapiexception import BinanceApiException

from binance_d.base.printobject import *
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, check_existence_radar_list_in_disc, list_pivots_in_radar_list_in_disk, funcname
from binance_d.example_d.user.process_event_scripts.process_module import process_event
from time import sleep
from binance_d.impl.websocketwatchdog import request_client, listen_key

#request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
#listen_key = request_client.start_user_data_stream()
#print("#### in example_d.user.subscribeuserdata.py listenKey: ", listen_key)


def first_steps():
    print("in websocket_module.first_steps listen_key: " + str(listen_key))
    #input("pec")
    #sys.exit(66)

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
    sub_client = SubscriptionClient(api_key=g_api_key, secret_key=g_secret_key)


    #input("start websockets ? , pec")
    sub_client.subscribe_user_data_event(listen_key, callback, error)
   # sub_client.subscribe_mark_price_event("adausd_perp", callback, error)
    
    '''
    try:
        listen_key = request_client.start_user_data_stream()
        sub_client.subscribe_user_data_event(listen_key, callback, error)
       # sub_client.subscribe_mark_price_event("adausd_perp", callback, error)
        for i in range(1, 60*60*24):
            #if i % 59*60 == 0:
            if i % 2*60 == 0:
                result = request_client.keep_user_data_stream()
                print("#### in example_d.user.websocket_module Result keep user data stream: ", result)
                #get_spot_client().renew_listen_key(listen_key)
            #if i % 60 == 0:
            if i % 20 == 0:
                #click.secho(f"Socket ок, {int(i/60)} min.", fg="yellow")
                print(f"Socket ок, {int(i/60)} min.")
            sleep(1)        
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
    print("#### #### #### in callback BEGIN")
    if data_type == SubscribeMessageType.RESPONSE:
        print("Event ID: ", event)
    elif  data_type == SubscribeMessageType.PAYLOAD:
        #PrintBasic.print_obj(event)
        print("in callback comentado el PrintBasic.print_obj(event)")
        #'''
        if(event.eventType == "ACCOUNT_UPDATE"):
            print("Event Type: ", event.eventType)
            print("Event time: ", event.eventTime)
            print("================")
        elif(event.eventType == "ORDER_TRADE_UPDATE"):

            # create_dict_from_output works ok
            event_dict = create_dict_from_output(event)
            print("event_dict: " + str(event_dict))
            # event_dict: {'activationPrice': 'None', 'asksNotional': '0.0', 'avgPrice': '0.0', 'bidsNotional': '346.30322511', 'callbackRate': 'None', 
            # 'clientOrderId': 'web_eS2mZZJNK8Afy6qVY5LA', 'commissionAmount': 'None', 'commissionAsset': 'None', 'cumulativeFilledQty': '0.0', 
            # 'eventTime': '1651364195658', 'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'NEW', 'isClosePosition': 'False', 'isMarkerSide': 'False',
            #  'isReduceOnly': 'False', 'lastFilledPrice': '0.0', 'lastFilledQty': '0.0', 'orderId': '6183269971', 'orderStatus': 'NEW', 'orderTradeTime': '1651364195651',
            #  'origQty': '1.0', 'positionSide': 'LONG', 'price': '0.222', 'side': 'BUY', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP', 'timeInForce': 'GTC', 'tradeID': '0',
            #  'transactionTime': '1651364195651', 'type': 'LIMIT', 'workingType': 'CONTRACT_PRICE'}

            print("++++ print ORDER_TRADE_UPDATE details damian")
            print("Event Type: ", event.eventType)
            print("Event time: ", event.eventTime)
            #print("Transaction Time: ", event.transactionTime)
            print("Symbol: ", event.symbol)
            print("Client Order Id: ", event.clientOrderId)
            #print("Side: ", event.side)
            print("Order Type: ", event.type)
            #print("Time in Force: ", event.timeInForce)
            print("Original Quantity: ", event.origQty)
            #print("Position Side: ", event.positionSide)
            print("Price: ", event.price)
            #print("Average Price: ", event.avgPrice)
            #print("Stop Price: ", event.stopPrice)
            #print("Execution Type: ", event.executionType)
            #print("Order Status: ", event.orderStatus)
            print("Order Id: ", event.orderId)
            #print("Order Last Filled Quantity: ", event.lastFilledQty)
            #print("Order Filled Accumulated Quantity: ", event.cumulativeFilledQty)
            #print("Last Filled Price: ", event.lastFilledPrice)
            #print("Commission Asset: ", event.commissionAsset)
            #print("Commissions: ", event.commissionAmount)
            #print("Order Trade Time: ", event.orderTradeTime)
            #print("Trade Id: ", event.tradeID)
            #print("Bids Notional: ", event.bidsNotional)
            #print("Ask Notional: ", event.asksNotional)
            #print("Is this trade the maker side?: ", event.isMarkerSide)
            #print("Is this reduce only: ", event.isReduceOnly)
            #print("stop price working type: ", event.workingType)
            #print("Is this Close-All: ", event.isClosePosition)
            print("++++ end print ORDER_TRADE_UPDATE details damian")
            if not event.activationPrice is None:
                print("Activation Price for Trailing Stop: ", event.activationPrice)
            if not event.callbackRate is None:
                print("Callback Rate for Trailing Stop: ", event.callbackRate)
            print("++++++++++++++++++")
            print("++++++++++++++++++")
            print("++++++++++++++++++")
            #'''
        elif(event.eventType == "listenKeyExpired"):
            print("Event: ", event.eventType)
            print("Event time: ", event.eventTime)
            print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
            print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
            print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
    else:
        print("Unknown Data:")
    print()
    print("in callback END <<<< <<<< <<<< <<<<")
    print("in callback END <<<< <<<< <<<< <<<<")
    print("in callback END <<<< <<<< <<<< <<<<")
    print("in callback END <<<< <<<< <<<< <<<<")
    print("in callback END <<<< <<<< <<<< <<<<")
    print("in callback END <<<< <<<< <<<< <<<<")
    print("in callback END <<<< <<<< <<<< <<<<")
    print("in callback END <<<< <<<< <<<< <<<<")

def error(e: 'BinanceApiException'):
    print(e.error_code + e.error_message)

def perror():
    print("error is :" + str(sys.exc_info()))


def main():
    first_steps()
    #setup_logger() 
    websocket_steps()
    print("marca final")


if __name__ == "__main__":
    main()


#wss://dstream.binance.com