import sys
import json

from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *


from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, funcname, update_to_in_position, dump_radar_list


from binance_d.general_settings import adaperp_decimals
#factor_gain = 1.005

def get_trigger_price_to_close(price, factor_gain):
    print("raw trigger_price close", factor_gain*price)
    trigger_price = round(float(factor_gain) * float(price), adaperp_decimals)
    return trigger_price


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
        



def create_multiple_pivots(distance_percentage, initial_price, pivots_number, size, factor_gain, end_price):
    distance = 1 - (distance_percentage/100)
    price = initial_price
    tp_old = 100
    print("initial price to close", initial_price)
    deviation_percentage = 0
    max_deviation_percentage = 0
    for counter_pivots in range(1, pivots_number + 1):
        print("expected tc in loop", price)
        price = round(price * distance, adaperp_decimals)
        print("real calculated tp:", price)
        tc = get_trigger_price_to_close(price, factor_gain)
        print("real calculated tc:", tc)
        real_fg = tc/price
        #print("real_fg%", 100 * ( real_fg - 1) )
        print("real_fg % round", round( 100 * (real_fg -1 )  , adaperp_decimals))
        r_fg_percentage = round( 100 * ( real_fg -1 )  , adaperp_decimals)
        print("r_fg_percentage :" + str(r_fg_percentage) + ", pivot number : " + str(counter_pivots) + ", tp: " + str(price) + ", distance_percentage: " + str(distance_percentage) + ", tc: " + str(tc))
        deviation_percentage = 0 
        if r_fg_percentage < distance_percentage:
            deviation_percentage =  100 * ((r_fg_percentage/distance_percentage) - 1)
            print("deviation%", round(deviation_percentage, 5))
            if abs(deviation_percentage) >= max_deviation_percentage:
                max_deviation_percentage = abs(deviation_percentage)
        elif r_fg_percentage > distance_percentage:
            print("> distance")
            print("raw r_fg_percentage", r_fg_percentage)
            print("raw distance_percentage", distance_percentage)
            print( 100 * ( (r_fg_percentage/distance_percentage) - 1) )
            deviation_percentage = 100 * ( (r_fg_percentage/distance_percentage) - 1)
            print("deviation%", round(deviation_percentage, 5))
            if abs(deviation_percentage) >= max_deviation_percentage:
                max_deviation_percentage = abs(deviation_percentage)
        elif r_fg_percentage == 0:
            deviation_percentage = 0
            print("deviation%", deviation_percentage)
        fee_maker = 0.0001
        contract_quantity_in_ada_buy = round(10/price, 8) 
        contract_quantity_in_ada_sell = round(10/tc, 8)
        print("contract_quantity_in_ada_buy", contract_quantity_in_ada_buy)
        print("contract_quantity_in_ada_sell", contract_quantity_in_ada_sell)
        contract_sell_cost = round((contract_quantity_in_ada_sell*fee_maker), 8)
        print("contract_sell_cost", contract_sell_cost)
        gain_ada = round(contract_quantity_in_ada_buy - ( contract_quantity_in_ada_sell + contract_sell_cost), 8)
        print("gain_ada", gain_ada)
        real_tp = round(price*real_fg, 4)
        real_tp_cost = round(price*( 1 + fee_maker), 4)
        print("real_tp", real_tp)
        print("real_tp_cost", real_tp_cost)
        if real_tp > real_tp_cost and gain_ada > 0:
            print("OK sirve")
        else:
            print("NO sirve")
            break
        tp_old = price
        print("")
        if price < end_price:
            print("end_price reached")
            break
        if abs(deviation_percentage) == 100:
            print("100% deviation reached")
            break
        
        #input("next pivot, pec")
        #print("")
    print("max_deviation_percentage", max_deviation_percentage)        

def sirve(tc, factor_gain, distance_percentage):
    distance = 1 - (distance_percentage/100)
    print("distance", distance)
    tp = round(tc * distance, adaperp_decimals)
    print("tp", tp)
    # check1 > check2
    fee_maker = 0.0001
    check1 = round(tp*(factor_gain), 4)
    check2 = round(tp*( 1 + fee_maker), 4)
    print("check1", check1)
    print("check2", check2)

def delta_total():
#For example, suppose you want to calculate the maximum deviation of 3.14 multiplied by 2.718 and the 
# result rounded to 2 decimal places. Since both numbers have 3 digits of precision, we can assume k = 3. 
# The maximum absolute value of the two numbers is max(|x|, |y|) = max(|3.14|, |2.718|) = 3.14. 
#Assuming double-precision floating-point arithmetic with machine epsilon eps = 2.22e-16, we can calculate:
    '''
    >>> import sys
    >>> sys.float_info
    sys.float_info(max=1.7976931348623157e+308, max_exp=1024, max_10_exp=308, 
    min=2.2250738585072014e-308, min_exp=-1021, min_10_exp=-307, dig=15, mant_dig=53, 
    epsilon=2.220446049250313e-16, radix=2, rounds=1)
    
    delta_multiplication = k * max(|x|, |y|) * eps
                        = 3 * 3.14 * 2.22e-16
                        = 2.2012e-15
    
    delta_rounding = 0.5 * 10^(-d)
                   = 0.5 * 10^(-2)
                   = 0.005
    
    delta_total = delta_multiplication + delta_rounding
                = 2.2012e-15 + 0.005
                = 0.005
    '''
    k = 4
    eps = 2.22e-16
    fg = 1.0003
    tp = 0.18
    d = 4
    delta_multiplication = k*(max(fg, tp)) * eps
    delta_rounding = 0.5 * pow(10, -d)
    print(delta_multiplication)
    print(delta_rounding)
    float(delta_rounding)
    print("float delta_rounding", float(delta_rounding))
    delta_total = delta_multiplication + delta_rounding
    print("%.10f" % float(delta_total))
    #print(eps)

if __name__ == "__main__":
    # initial_price es el precio de venta
    distance_percentage = 0.125
    distance_percentage = 0.0625
    distance_percentage = 0.12
    #distance_percentage = 0.06
    #distance_percentage = 0.03
    #distance_percentage = 0.02
    #distance_percentage = 0.01
    #distance_percentage = 0.0625/2
    factor_gain = (distance_percentage / 100 ) + 1    
    #print("factor_gain: ", factor_gain)
    ###################################
    initial_price = 0.39 #  
    initial_price = 0.39#  it is the tclose of the first pivot
    end_price = 0.1299 
    pivots_number = 2000
    size = 1  
    #delta_total()
    #input("in main in " + funcname())
    #sirve(initial_price, factor_gain, distance_percentage)
    create_multiple_pivots(distance_percentage, initial_price, pivots_number, size, factor_gain, end_price)   
    
