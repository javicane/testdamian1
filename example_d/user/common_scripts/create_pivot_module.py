import sys
import json

#from binance_d.requestclient import RequestClient
#from binance_d.subscriptionclient import SubscriptionClient
#from binance_d import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *


from socket import create_connection
from binance_d.example_d.user.common_scripts.create_orders_module import silent_limit_no_oco_buy_long
from binance_d.example_d.trade.damian_cancel_order import cancel_order_by_id_and_symbol
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, funcname, update_to_in_position, get_trigger_price_to_close, dump_radar_list
from binance_d.example_d.user.helpers_scripts.sql import exec_sql

from binance_d.impl.utils.timeservice import get_current_timestamp 

from binance_d.general_settings import adaperp_decimals
#factor_gain = 1.005

def get_factor_gain():
    factor_gain_config_file = "/home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/config_scripts/factor_gain.json"
    with open(factor_gain_config_file) as conf:
        data_dict = json.load(conf)
    factor_gain = data_dict['factor_gain']
   # print("factor_gain: " + str(factor_gain))
   # print("factor_gain type: " + str(type(factor_gain)))
    return factor_gain


def check_price_and_size(p_price, p_size, output_dict):
    #input(funcname() + ", pec")
    print("output_dict: " + str(output_dict))
    print("status: " + str(output_dict['status']))
    print("price: " + str(output_dict['price']))
    print("origQty: " + str(output_dict['origQty']))
    print("orderId: " + str(output_dict['orderId']))
    #p_price = 10
    if ( ( ( float(p_price) - float(output_dict['price']) ) == 0 ) and
         ( ( round(float(p_size)) - round(float(output_dict["origQty"])) ) == 0 ) ):
        print("price and size ok") 
        return "OK" 
    else:
        print("ERROR in " + funcname()) 
        return "ERROR in check_price_and_size"

def create_one_pivot(p_price, p_size):
    print("in " + funcname())
    # attention, ,"priceProtect":false by default
    clientorderid_value = "new_pivot" + str(get_current_timestamp())
    output = silent_limit_no_oco_buy_long(p_price, p_size, p_clientorderid=clientorderid_value )
    #print("output is type: " + str(type(output)))
    output_dict =  create_dict_from_output(output)
   # print("output_dict: " + str(output_dict))
    #print("status: " + str(output_dict['status']))
    #print("price: " + str(output_dict['price']))
    #print("origQty: " + str(output_dict['origQty']))
    #print("orderId: " + str(output_dict['orderId']))
    rc = check_price_and_size(p_price, p_size, output_dict) 
    print("in " + funcname() + ", rc: " + str(rc))
    if "ERROR" in rc:
        err = "ERROR in " + funcname() + ", plus " + str(rc)
        print(err)
        return err
    else:
        return output_dict 


def insert_radar_list_new_pivot_conditional(output_dict, p_tc, group_id=0): 
    '''
    tree: 
        1. begin caller is process_event_scripts/process_module.process_pnl
        2. caller is proces_module.process_conditional_pivot 
        3. caller is local exec_transaction_pivot_conditional
    '''
    print("in " + funcname())
    price = output_dict['price']
    order_id = output_dict['orderId']
    order_status = "NEW"
    order_id_to_close = 0
    trigger_price_to_put_in_position = price
    trigger_price_to_close = round(float(p_tc), adaperp_decimals)
    original_quantity = output_dict['origQty']
    clientorderid = output_dict['clientOrderId']
    resize = original_quantity
    conditional = "Y"
    factor_gain=666

    tuple1 = (order_id, order_status, order_id_to_close, trigger_price_to_put_in_position, trigger_price_to_close, original_quantity, clientorderid, resize, factor_gain, group_id, conditional)
    print(funcname(), ", tuple1", tuple1)
    sql = "insert into radar_list ( order_id, order_status, order_id_to_close, trigger_price_to_put_in_position,"
    sql += "trigger_price_to_close, original_quantity, clientorderid, resize, factor_gain, group_id, conditional ) values " 
    sql += str(tuple1)
    print(funcname(), ", sql: ", sql)
    rows_inserted = exec_sql(sql = sql, sql_command = "insert", error_message = "error in " + str(funcname()))
    #rows_inserted = 0
    if rows_inserted != 1:
        err = "ERROR in " + funcname() + ", aborting"
        print(err)
        raise 

def insert_radar_list_new_pivot(output_dict, factor_gain, group_id=0): 
    price = output_dict['price']
    order_id = output_dict['orderId']
    order_status = "NEW"
    order_id_to_close = 0
    trigger_price_to_put_in_position = price
    #trigger_price_to_close = get_trigger_price_to_close(price, get_factor_gain())
    trigger_price_to_close = get_trigger_price_to_close(price, factor_gain)
    original_quantity = output_dict['origQty']
    clientorderid = output_dict['clientOrderId']
    resize = original_quantity

    tuple1 = (order_id, order_status, order_id_to_close, trigger_price_to_put_in_position, trigger_price_to_close, original_quantity, clientorderid, resize, factor_gain, group_id)
    sql = "insert into radar_list ( order_id, order_status, order_id_to_close, trigger_price_to_put_in_position,"
    sql += "trigger_price_to_close, original_quantity, clientorderid, resize, factor_gain, group_id ) values " 
    sql += str(tuple1)

    rows_inserted = exec_sql(sql = sql, sql_command = "insert", error_message = "error in " + str(funcname()))
    if rows_inserted != 1:
        err = "ERROR in " + funcname() + ", aborting"
        print(err)
        raise 
    
def exec_transaction_pivot_conditional(p_tp, p_tc, p_size):
    '''
    tree: 
        1. begin caller is process_event_scripts/process_module.process_pnl
        2. caller is proces_module.process_conditional_pivot
    ''' 
    group_id = 0 # for compatibility only
    print("in " + funcname() + " args p_tp, p_tc, p_size: ", p_tp, p_tc, p_size)
    err = ""
    try:
        print("in " + funcname() + ",call create_one_pivot(" + str(p_tp) + ", " + str(p_size) + ")")
        rc = create_one_pivot(p_tp, p_size)
        #rc = "OK"
        if "ERROR" in rc:
            err = "ERROR in " + funcname() + ", plus " + str(rc)
            print(err)
        else:
            print("in " + funcname() + ",call insert_radar_list_new_pivot_conditional")
            output_dict = rc
            ####
            #debug
            #output_dict = dict(price=p_tp,
            #                   orderId=666666,
            #                   origQty=p_size,
            #                   clientOrderId="zaraza_clientorderid")
            ####
            insert_radar_list_new_pivot_conditional(output_dict, p_tc, group_id)
            print("in " + funcname() + ", return from insert")
            return "OK" 
    except:
        err = "except in " + funcname() + ", " + str(sys.exc_info())
        print(err)
        raise
    finally:
        if "ERROR" in err:
            print("in " + funcname() + "," + err)
            raise

def exec_transaction_pivot(p_price, p_size, factor_gain, group_id=0):
    print("in " + funcname() + " args p_price, p_size, factor_gain: " + str(p_price) + ", " + str(p_size) + ", factor_gain: " + str(factor_gain) + ", group_id: " + str(group_id))
    err = ""
    try:
        print("call create_one_pivot(" + str(p_price) + ", " + str(p_size) + ")")
        rc = create_one_pivot(p_price, p_size)
        if "ERROR" in rc:
            err = "ERROR in " + funcname() + ", plus " + str(rc)
            print(err)
        else:
            #next_step_dict = { "name" : insert_radar_list_new_pivot }
            #print("in " + funcname() + ", call:  " + str(next_step_dict['name']))
            #next_step_dict['name'](rc)
            output_dict = rc
            insert_radar_list_new_pivot(output_dict, factor_gain, group_id)
            return "OK" 
    except:
        err = "except in " + funcname() + ", " + str(sys.exc_info())
        print(err)
        raise
    finally:
        if "ERROR" in err:
            print("transaction_pivot failed : " + err)
            raise

def create_multiple_pivots(distance_percentage, initial_price, pivots_number, size, factor_gain):
    distance = 1 - (distance_percentage/100)
    price = initial_price
    for counter_pivots in range(1, pivots_number + 1):
        price = round(price, adaperp_decimals)
        #print("pivot number : " + str(counter_pivots) + ", price: " + str(price) + ", distance_percentage: " + str(distance_percentage) + ", size: " + str(size))
        #distance = 1 - (distance_percentage/100)
        price = round(price * distance, adaperp_decimals)
        print("pivot number : " + str(counter_pivots) + ", price: " + str(price) + ", distance_percentage: " + str(distance_percentage) + ", size: " + str(size))
        #exec_transaction_pivot(p_price=price, p_size=size, factor_gain)
        exec_transaction_pivot(price, size, factor_gain)
        #input("next pivot, pec")
        

if __name__ == "__main__":
    # initial_price es el precio de venta
    distance_percentage = 0.125
    distance_percentage = 0.0625
    distance_percentage = 0.12
    #distance_percentage = 0.06
    #distance_percentage = 0.0625/2
    factor_gain = (distance_percentage / 100 ) + 1    
    print("factor_gain: ", factor_gain)
    #sys.exit(66)
    #distance_percentage = 0.25
    ##################
    # para completar huecos hacia arriba
    #initial_price = round(0.43*1.000625,5) # poner el tclose del pivot inferior mas cercano 
    initial_price = round(0.32459*factor_gain, adaperp_decimals) # en este caso initial_price va a ser el tp del pivot a crear
    ###################################
    initial_price = 0.39 #  
    pivots_number = 40
    size = 1  
    #input("in main in " + funcname())
    create_multiple_pivots(distance_percentage, initial_price, pivots_number, size, factor_gain)   

#el post_order.py  incluye un check_response, si viene este payload como respuesta es que salio bien:

#header:{'client_SDK_Version': 'binance_dutures-1.0.1-py3.7', 'Content-Type': 'application/json', 'X-MBX-APIKEY': 'Hmn1YedMgRbHvfvLPzPmCdDAV6doTqReE7gZRSZw5au109vZS5ooKQU3PHpavaKi'}
#host:https://dapi.binance.com
#json_parser:None
#method:POST
#post_body:{}
#url:/dapi/v1/order?symbol=ADAUSD_PERP&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.666&positionSide=LONG&recvWindow=60000&timestamp=1651194242291&signature=02dbfa9fb9af04b33b4c570df35fb751b9e1f59a430c46d60a753567399f2e3a
#=====================
#{"orderId":6159647539,"symbol":"ADAUSD_PERP","pair":"ADAUSD","status":"NEW","clientOrderId":"TWEsEnk4rIrVHVDAEujX9l","price":"0.66600","avgPrice":"0.00000","origQty":"1","executedQty":"0","cumQty":"0","cumBase":"0","timeInForce":"GTC","type":"LIMIT","reduceOnly":false,"closePosition":false,"side":"BUY","positionSide":"LONG","stopPrice":"0","workingType":"CONTRACT_PRICE","priceProtect":false,"origType":"LIMIT","updateTime":1651194244159}
#result raw: <binance_d.model.order.Order object at 0x7f78e144fb80>
###
#activatePrice:None
#avgPrice:0.0
#clientOrderId:TWEsEnk4rIrVHVDAEujX9l
#closePosition:False
#cumBase:0.0
#executedQty:0.0
#json_parse:<function Order.json_parse at 0x7f78e22d40d0>
#orderId:6159647539
#origQty:1.0
#origType:LIMIT
#positionSide:LONG
#price:0.666
#priceRate:None
#reduceOnly:False
#side:BUY
#status:NEW
#stopPrice:0.0
#symbol:ADAUSD_PERP
#timeInForce:GTC
#type:LIMIT
#updateTime:1651194244159
#workingType:CONTRACT_PRICE
#
#
#nueva orden limit:
#{"e":"ORDER_TRADE_UPDATE","T":1651189973485,"E":1651189973488,"i":"oCTiSgXqfWFzoC","o":
# {"s":"ADAUSD_PERP","c":"web_9pudjCixrL2gFS3KyxvU","S":"BUY","o":"LIMIT","f":"GTC","q":"2","p":"0.84300","ap":"0","sp":"0",
#  "x":"NEW","X":"NEW","i":6159050498,"l":"0","z":"0","L":"0","T":1651189973485,"t":0,"b":"26.89686192","a":"0","m":false,"R":false,
#  "wt":"CONTRACT_PRICE","ot":"LIMIT","ps":"LONG","cp":false,"ma":"ADA","rp":"0","pP":false,"si":0,"ss":0}}
#
#y cuando entra en position:
#
#{"e":"ORDER_TRADE_UPDATE","T":1651189973485,"E":1651189973488,"i":"oCTiSgXqfWFzoC","o":
# {"s":"ADAUSD_PERP","c":"web_9pudjCixrL2gFS3KyxvU","S":"BUY","o":"LIMIT","f":"GTC","q":"2","p":"0.84300","ap":"0.84236","sp":"0",
#  "x":"TRADE","X":"FILLED","i":6159050498,"l":"2","z":"2","L":"0.84236","n":"0.01187140","N":"ADA","T":1651189973485,"t":101799742,"b":"26.89686192","a":"0","m":false,"R":false,
#  "wt":"CONTRACT_PRICE","ot":"LIMIT","ps":"LONG","cp":false,"ma":"ADA","rp":"0","pP":false,"si":0,"ss":0}}
#  "t":101799742
#
#voy a hacer una orden limit sell de size 3 de contracts in position, usando un precio muy alto para que no se ejecute , price 3:
#
#{"e":"ORDER_TRADE_UPDATE","T":1651190312740,"E":1651190312746,"i":"oCTiSgXqfWFzoC","o":
# {"s":"ADAUSD_PERP","c":"web_6WLVHdpJDvNParez2o0a","S":"BUY","o":"LIMIT","f":"GTC","q":"3","p":"0.84236","ap":"0","sp":"0",
#  "x":"NEW","X":"NEW","i":6159093127,"l":"0","z":"0","L":"0","T":1651190312740,"t":0,"b":"62.51108862","a":"0","m":false,"R":false,
#  "wt":"CONTRACT_PRICE","ot":"LIMIT","ps":"LONG","cp":false,"ma":"ADA","rp":"0","pP":false,"si":0,"ss":0}}
#
#+++
#voy a hacer una orden limit sell de size 1 de contracts in position, using a price value less than market to force to execute immediately:
#el market esta en 0.84383 y la hago a 0.842
#
#al final termina haciendo el flow usual new a filled
#
#{"e":"ORDER_TRADE_UPDATE","T":1651174951054,"E":1651174951058,"i":"oCTiSgXqfWFzoC","o":
# {"s":"ADAUSD_PERP","c":"web_rBl2a7k4gVQHtReMno8y","S":"SELL","o":"LIMIT","f":"GTC","q":"1","p":"0.84200","ap":"0","sp":"0",
#  "x":"NEW","X":"NEW","i":6156859044,"l":"0","z":"0","L":"0","T":1651174951054,"t":0,"b":"0","a":"0","m":false,"R":true,
#  "wt":"CONTRACT_PRICE","ot":"LIMIT","ps":"LONG","cp":false,"ma":"ADA","rp":"0","pP":false,"si":0,"ss":0}}
#
#{"e":"ORDER_TRADE_UPDATE","T":1651174951054,"E":1651174951058,"i":"oCTiSgXqfWFzoC","o":
# {"s":"ADAUSD_PERP","c":"web_rBl2a7k4gVQHtReMno8y","S":"SELL","o":"LIMIT","f":"GTC","q":"1","p":"0.84200","ap":"0.84310","sp":"0",
#  "x":"TRADE","X":"FILLED","i":6156859044,"l":"1","z":"1","L":"0.84310","n":"0.00593049","N":"ADA","T":1651174951054,"t":101765945,"b":"0","a":"0","m":false,"R":true,
#  "wt":"CONTRACT_PRICE","ot":"LIMIT","ps":"LONG","cp":false,"ma":"ADA","rp":"-0.70592310","pP":false,"si":0,"ss":0}}
#
####
#insert into radar_list :
#{ id, status: NEW, has_limit_order_to_close=false , trigger_to_put_in_position}
#
#if event user
#{ if radar_list(id)= event(id) and radar_list(id)(status) =NEW and event(id)(status) = FILLED then
#update radar_list(id)(status: IN_POSITION)
#generate_limit_order_sell(id) and status(id)[has_limit_order_to_close]=true
#}
#elif
#{ event_status(id) = FILLED then
#if status(id) = IN_POSITION and has_limit_order_to_close(id) = true then
#status(id) = FILLED
#new_id= open_new_order(settings(id) )
#insert into radar_list (
#id=new_id, settings(id), status=NEW , has_limit_order_to_close=false)
#insert(radar_list(id)) into filled_dict
#delete_from_radar_list(id)
#}


