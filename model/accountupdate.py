import sys
from binance_d.base.printobject import *

class Balance:

    def __init__(self):
        self.asset = ""
        self.walletBalance = 0.0
        self.crossWallet = 0.0
        self.balance_change = 0.0 #damian

    @staticmethod
    def json_parse(json_data):
        result = Balance()
        
        result.asset = json_data.get_string("a")
        result.walletBalance = json_data.get_float("wb")
        result.crossWallet = json_data.get_float("cw")
        result.balance_change = json_data.get_float("bc") # damian
        # event FUNDING_FEE
        ###{"e":"ACCOUNT_UPDATE","T":1662105600141,"E":1662105600198,"i":"oCTiSgXqfWFzoC",
        # "a":{"B":[{"a":"ADA","wb":"7620.73025767","cw":"7620.73025767","bc":"-0.88984664"}],"P":[],"m":"FUNDING_FEE"}}
        return result


class Position:

    def __init__(self):
        self.symbol = ""
        self.amount = 0.0
        self.entryPrice = 0.0
        self.preFee = 0.0
        self.unrealizedPnl = 0.0
        self.marginType = ""
        self.isolatedWallet = 0.0
        self.positionSide = ""

    @staticmethod
    def json_parse(json_data):
        result = Position()
        result.symbol = json_data.get_string("s")
        result.amount = json_data.get_float("pa")
        result.entryPrice = json_data.get_float("ep")
        result.preFee = json_data.get_float("cr")
        result.unrealizedPnl = json_data.get_float("up")
        result.marginType = json_data.get_string("mt")
        result.isolatedWallet = json_data.get_float("iw")
        result.positionSide = json_data.get_string("ps")
        return result


class AccountUpdate:
    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
        self.transactionTime = 0
        self.balances = list()
        self.positions = list()
        self.event_reason_type = "" # damian

    @staticmethod
    def json_parse(json_data):
        result = AccountUpdate()
        result.eventType = json_data.get_string("e")
        result.eventTime = json_data.get_int("E")
        result.transactionTime = json_data.get_int("T")

        data_group = json_data.get_object("a") # la key "a" contiene un dict con 3 elements: B, P, m

        # event FUNDING_FEE
        ###{"e":"ACCOUNT_UPDATE","T":1662105600141,"E":1662105600198,"i":"oCTiSgXqfWFzoC",
        # "a":{"B":[{"a":"ADA","wb":"7620.73025767","cw":"7620.73025767","bc":"-0.88984664"}],"P":[],"m":"FUNDING_FEE"}} 
        
        # event no FUNDING_FEE
        #{"e":"ACCOUNT_UPDATE","T":1662117941194,"E":1662117941202,"i":"oCTiSgXqfWFzoC",
        # "a":{"B":[{"a":"BTC","wb":"0","cw":"0","bc":"0"},{"a":"SOL","wb":"0.00415687","cw":"0.00415687","bc":"0"},
        # {"a":"ADA","wb":"7634.72978052","cw":"7634.72978052","bc":"0"}],
        # "P":[{"s":"ADAUSD_PERP","pa":"0","ep":"0.00000","cr":"-20483.39987094","up":"0","mt":"cross","iw":"0","ps":"BOTH","ma":"ADA"},
        # {"s":"ADAUSD_PERP","pa":"440","ep":"0.45293","cr":"-13245.38103947","up":"18.01574881","mt":"cross","iw":"0","ps":"LONG",
        # "ma":"ADA"},{"s":"ADAUSD_PERP","pa":"0","ep":"0.00000","cr":"-16737.49239759","up":"0","mt":"cross","iw":"0","ps":"SHORT",
        # "ma":"ADA"}],"m":"ORDER"}}

        #damian
        '''
        try:
            event_reason_type_temp = data_group.get_string("m")
            result.event_reason_type = event_reason_type_temp
            print("in model.accountupdate.AccountUpdate.json_parse event_reason_type_temp:", event_reason_type_temp)
        except:
            print("except in model.accountupdate.AccountUpdate.json_parse in event_reason_type_temp:", sys.exc_info())
        '''     
        event_reason_type_temp = data_group.get_string("m")
        result.event_reason_type = event_reason_type_temp

        element_list = list()
        data_list = data_group.get_array("B")
        for item in data_list.get_items():
           # print("in model.accountupdate.AccountUpdate.json_parse for loop Balances, item:", item)  
            element = Balance.json_parse(item)
            #print("in model.accountupdate.AccountUpdate.json_parse for loop Balances, element = Balance.json_parse(item):", element)  
           #in model.accountupdate.AccountUpdate.json_parse for loop Balances,
            # element = Balance.json_parse(item): <binance_d.model.accountupdate.Balance object at 0x7fd10f7d1a60>
#            print("in model.accountupdate.AccountUpdate.json_parse for loop Balances call PrintMix.print_data(element)")
###
            #obj = element
            #print("in model.accountupdate.AccountUpdate.json_parse:", obj)
            #print("in model.accountupdate.AccountUpdate.json_parse dir(obj):", dir(obj))
            #members = [attr for attr in dir(obj) if not callable(attr) and not attr.startswith("__")]
            #print("in model.accountupdate.AccountUpdate.json_parse members:", members)
            #print("in model.accountupdate.AccountUpdate.json_parse loop")
            #for member_def in members:
                #val_str = str(getattr(obj, member_def))
                #print(".... model.accountupdate.AccountUpdate.json_parse begin step loop") 
                #print("model.accountupdate.AccountUpdate.json_parse member_def:", member_def)
                #print("model.accountupdate.AccountUpdate.json_parse val_str:", val_str)
                #print(member_def + ":" + val_str)
                #print("....model.accountupdate.AccountUpdate.json_parse end step loop") 
                #print("")
            #print("----model.accountupdate.AccountUpdate.json_parse end print_obj")
####
#            PrintMix.print_data(element)            
    #        print("")
            element_list.append(element)
        result.balances = element_list
        #if event_reason_type_temp == 'ORDER' or event_reason_type_temp == 'FUNDING_FEE':
        #    print("model.accountupdate.AccountUpdate.json_parse balances (element_list):", element_list)
       
        if data_group.contain_key("P"):
            element_list = list()
            data_list = data_group.get_array("P")
            for item in data_list.get_items():
                element = Position.json_parse(item)
                element_list.append(element)
            result.positions = element_list

        return result
