import sys
import json
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, funcname, update_to_in_position, get_trigger_price_to_close, dump_radar_list

def get_trigger_price_to_close(price, factor_gain):
    trigger_price = round(float(factor_gain) * float(price), 5)
    print("in " + funcname())
    print(".... trigger_price: " + str(trigger_price))
    return trigger_price

def get_factor_gain():
    factor_gain_config_file = "/home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/config_scripts/factor_gain.json"
    with open(factor_gain_config_file) as conf:
        data_dict = json.load(conf)
    factor_gain = data_dict['factor_gain']
   # print("factor_gain: " + str(factor_gain))
   # print("factor_gain type: " + str(type(factor_gain)))
    return factor_gain        

def create_multiple_pivots(distance_percentage, initial_price, pivots_number, size):
    distance = 1 - (distance_percentage/100)
    price = initial_price
    for counter_pivots in range(1, pivots_number + 1):
        price = round(price, 5)
        #print("pivot number : " + str(counter_pivots) + ", price: " + str(price) + ", distance_percentage: " + str(distance_percentage) + ", size: " + str(size))
        #distance = 1 - (distance_percentage/100)
        price = round(price * distance, 5)
        print("pivot number : " + str(counter_pivots) + ", price: " + str(price) + ", distance_percentage: " + str(distance_percentage) + ", size: " + str(size))
        #input("next pivot, pec")
        trigger_price_to_close = get_trigger_price_to_close(price, get_factor_gain())
        print("trigger_price_to_close: ", trigger_price_to_close)


if __name__ == "__main__":
    distance_percentage = 0.12
    #distance_percentage = 0.25
    initial_price = 0.54664 
    pivots_number = 3 
    size = 4 
    #input("in main in " + funcname())
    create_multiple_pivots(distance_percentage, initial_price, pivots_number, size)        