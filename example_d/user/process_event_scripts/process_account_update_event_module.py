import sys
import json
import types
#import pickle
from binance_d.example_d.user.helpers_scripts.helpers_module import funcname
from binance_d.example_d.user.helpers_scripts.sql import exec_sql
from binance_d.impl.utils.timeservice import get_current_timestamp

def create_dict_from_output(output):
    members = [attr for attr in dir(output) if not callable(attr) and not attr.startswith("__")]
    my_dict = {}
    for member_def in members:
        val_str = str(getattr(output, member_def))
        val_raw = getattr(output, member_def)
        ###
        # check if "member_def" is pointing to a function
        j = isinstance(val_raw, types.FunctionType)
        if not j:
            my_dict[member_def] = val_str
        else:
            #nada = 1
            print(member_def + " is pointing to a function " + str(type(val_raw)))
    return my_dict

def process_account_update(event):
    '''
    event esta modelado en model.accountupdate.py
    '''

    print("in process_account_update DETECTED ACCOUNT_UPDATE, BEGIN")
    
    print("in callback, ACCOUNT_UPDATE Event Type: ", event.eventType)
    print("in callback, ACCOUNT_UPDATE event is:", event)
    print("in callback, ACCOUNT_UPDATE Event time: ", event.eventTime)
    #print("dir(event):", dir(event))
    #in callback, data_type received is PAYLOAD
    #in callback, ACCOUNT_UPDATE Event Type:  ACCOUNT_UPDATE
    #in callback, ACCOUNT_UPDATE event is: <binance_d.model.accountupdate.AccountUpdate object at 0x7fd008a438e0>
    #dir(event): ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
    # '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', 
    # '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
    # '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'balances', 'eventTime', 'eventType', 
    # 'event_reason_type', 'json_parse', 'positions', 'transactionTime']
    val_str_event_reason_type = ""
    balance_change = 0.0
    walletBalance = 0.0
    entry_price = 0.0
    unrealized_pnl = 0.0 
    try:
        obj = event
        members = [attr for attr in dir(obj) if not callable(attr) and not attr.startswith("__")]
        #print("members:", members)
        #members: ['balances', 'eventTime', 'eventType', 'event_reason_type', 'json_parse', 'positions', 'transactionTime']
      
        #extract event_reason_type
        #print("extract event_reason_type")
        val_str_event_reason_type = str(getattr(obj, "event_reason_type"))
        val_raw_event_reason_type = getattr(obj, "event_reason_type")
        #print("val_str_event_reason_type", val_str_event_reason_type)
        #print("val_raw_event_reason_type", val_raw_event_reason_type)
        #member_def type: <class 'str'>
        #val_str: ORDER
        #val_raw: ORDER
                #member_def: event_reason_type
                #member_def type: <class 'str'>
                #val_str: ORDER
                #val_raw: ORDER
                #val_raw type: <class 'str'>
                #inside if if member_def == event_reason_type
                #event_reason_type val_str: ORDER
                #event_reason_type val_raw: ORDER

        #extract balances                
        #print("extract balances")
        val_str_balances = str(getattr(obj, "balances"))
        val_raw_balances = getattr(obj, "balances")

        #extract positions
        try:
            val_str_positions = str(getattr(obj, "positions"))
            val_raw_positions = getattr(obj, "positions")
        except:
            print("except in getattr(obj, positions)", sys.exc_info())

        #print("val_str_balances", val_str_balances)
        #print("val_raw_balances", val_raw_balances)
        #member_def: balances
        #member_def type: <class 'str'>
        #val_str: [<binance_d.model.accountupdate.Balance object at 0x7fefbd4dbe20>, <binance_d.model.accountupdate.Balance object at 0x7fefbd4c3fd0>, <binance_d.model.accountupdate.Balance object at 0x7fefbd4c3640>]
        #val_raw: [<binance_d.model.accountupdate.Balance object at 0x7fefbd4dbe20>, <binance_d.model.accountupdate.Balance object at 0x7fefbd4c3fd0>, <binance_d.model.accountupdate.Balance object at 0x7fefbd4c3640>]
        #val_raw type: <class 'list'>
        #print("balances dir(val_raw_balances):", dir(val_raw_balances))
                #balances dir(val_raw_balances): ['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', 
                # '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', 
                # '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', 
                # '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', 
                # '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 
                # 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']


        ### begin parsing balances
        try:
            for i in val_raw_balances:
                #print("dir(i) ver balances:", dir(i))
                #print("ver balances val_raw i:", i) 
                #print("ver balances val_raw i type:", type(i)) 
                balance_change = ""
                try:
                    asset = str(getattr(i, "asset"))
                    if asset == "ADA":
                        balance_change = str(getattr(i, "balance_change"))                                
                        walletBalance = str(getattr(i, "walletBalance"))
                    #print("balance_change:", balance_change)
                    #print("asset:", asset)
                    #dir(i) ver balances: ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', 
                    # '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', 
                    # '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', 
                    # '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 
                    # '__weakref__', 'asset', 'balance_change', 'crossWallet', 'json_parse', 'walletBalance']
                    #ver balances val_raw i: <binance_d.model.accountupdate.Balance object at 0x7fefbd4c3640>
                    #ver balances val_raw i type: <class 'binance_d.model.accountupdate.Balance'>
                    #balance_change: 0.0
                    #asset: ADA
                    #print("walletBalance", walletBalance)
                except:
                    print("marca2 ver balances except:", sys.exc_info())
        except:
            print("marca1 ver balances except:", sys.exc_info())
        ### end parsing balances
        ### begin parsing positions
        #in on_message, message (raw message received by websocket client): 
        # |||| {"e":"ACCOUNT_UPDATE","T":1663517406961,"E":1663517406969,"i":"oCTiSgXqfWFzoC",
        # "a":{"B":[{"a":"BTC","wb":"0","cw":"0","bc":"0"},{"a":"SOL","wb":"0.00415687","cw":"0.00415687","bc":"0"},
        # {"a":"ADA","wb":"8112.64221254","cw":"8112.64221254","bc":"0"}],
        # "P":[{"s":"ADAUSD_PERP","pa":"0","ep":"0.00000","cr":"-20483.39987094","up":"0","mt":"cross","iw":"0","ps":"BOTH","ma":"ADA"},
        # {"s":"ADAUSD_PERP","pa":"928","ep":"0.47586","cr":"-12574.15823851","up":"-294.65998317","mt":"cross","iw":"0","ps":"LONG","ma":"ADA"},
        # {"s":"ADAUSD_PERP","pa":"0","ep":"0.00000","cr":"-16737.49239759","up":"0","mt":"cross","iw":"0","ps":"SHORT","ma":"ADA"}],"m":"ORDER"}} ||||end of message
        try:
            for i in val_raw_positions:
                try:
                    symbol = str(getattr(i, "symbol"))
                    positionside = str(getattr(i, "positionSide"))
                    #print("loop symbol POSITION:", symbol)
                    #print("loop positionside:", positionside)
                    if symbol == "ADAUSD_PERP" and positionside == "LONG":
                        entry_price = str(getattr(i, "entryPrice"))                                
                        unrealized_pnl = str(getattr(i, "unrealizedPnl"))
                        #print(".... entry_price:", entry_price)
                        #print(".... unrealized_pnl:", unrealized_pnl)
                except:
                    print("marca2 ver positions except:", sys.exc_info())
        except:
            print("marca1 ver positions except:", sys.exc_info())
        ### end parsing positions 




        if val_str_event_reason_type == "FUNDING_FEE":
            print("detected FUNDING_FEE event_reason_type")
            print("balance_change FUNDING_FEE:", balance_change)
            print("walletBalance FUNDING_FEE:", walletBalance)
            insert_funding_fee_in_db(balance_change, event.eventTime)
        elif val_str_event_reason_type == 'ORDER':
            print("detected ORDER event_reason_type")
            print("walletBalance ORDER:", walletBalance)
            try:
                print("entry_price ORDER:", entry_price)
                print("unrealized_pnl ORDER:", unrealized_pnl)
            except:
                print("except in print entry_price and unrealized_pnl:", sys.exc_info())
            update_entry_price_in_db(entry_price, event.eventTime)
            update_balance_in_db(walletBalance, event.eventTime)
    except:
        print("in callback ACCOUNT_UPDATE except primer try:", sys.exc_info())
    
    #try:
        #PrintList.print_origin_object(event)
        #print("try PrintBasic")
    #    obj = event
        #PrintBasic.print_obj(obj)
    #except:
    #    print("except callback ACCOUNT_UPDATE PrintBasic.print_obj(obj) :", sys.exc_info())
   # process_account_update(event) 
    #print("in callback, callbackEvent time: ", event.eventTime)
    #print("================")

    print("in process_account_update DETECTED ACCOUNT_UPDATE, END")
    #event_dict = create_dict_from_output(event)
    #with open('/home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/pickle.event', 'wb') as pickle_file:
    #    try:
    #        pickle.dump(event, pickle_file)
    #    except:
    #        print("except pickle:", sys.exc_info())

def update_entry_price_in_db(entry_price, timestamp):
    try:
        sql = "update tracker_entry_price set entry_price = " + str(entry_price) + ", "
        sql += "timestamp=" + str(timestamp) + ";"
        print(".... cal exec_sql with sql: " + str(sql))
        try:
            result = exec_sql(sql = sql , sql_command = "update", error_message = "update entry_price")
        except:
            print("ERROR in " + funcname() + ", except: " + str(sys.exc_info()))
        if result != 1:
            err = ".... .... ERROR in " + funcname() + ", result: " + str(result)
            print(err)
        else:
            print("OK ", funcname())
    except:
        err = "ERROR except in " + funcname() + ", non critical error, can continue:" + str(sys.exc_info())
        print(err)

def update_balance_in_db(balance, timestamp):
    try:
        #timestamp = get_current_timestamp()
        sql = "update tracker_balance set balance = " + str(balance) + ", "
        sql += "timestamp=" + str(timestamp) + ";"
        print(".... cal exec_sql with sql: " + str(sql))
        try:
            result = exec_sql(sql = sql , sql_command = "update", error_message = "update balance")
        except:
            print("ERROR in " + funcname() + ", except: " + str(sys.exc_info()))
        if result != 1:
            err = ".... .... ERROR in " + funcname() + ", result: " + str(result)
            print(err)
        else:
            print("OK ", funcname())
    except:
        err = "ERROR except in " + funcname() + ", non critical error, can continue:" + str(sys.exc_info())
        print(err)

def insert_funding_fee_in_db(fee, timestamp):
    try:
        #timestamp = get_current_timestamp()
        tuple1 = (timestamp, fee)
        sql = "insert into tracker_funding_fee (timestamp, fee) values "
        sql += str(tuple1)
        rows_inserted = exec_sql(sql = sql, sql_command = "insert", error_message = "error in " + str(funcname()))
        if rows_inserted != 1:
            err = "ERROR in " + funcname()
            print(err)
        else:
            print("OK ", funcname()) 
    except:
        err = "ERROR except in " + funcname() + ", non critical error, can continue:" + str(sys.exc_info())
        print(err)