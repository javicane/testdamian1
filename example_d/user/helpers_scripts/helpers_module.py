import inspect
import sys
import types
import os
import json

from os.path import exists
from binance_d.example_d.user.helpers_scripts.sql import create_db_conn, dict_factory

from binance_d.general_settings import adaperp_decimals

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
            nada = 1
            #print(member_def + " is pointing to a function " + str(type(val_raw)))
    return my_dict

def funcname():
    funcname_who_call_me = sys._getframe(1).f_code.co_name
    return funcname_who_call_me

def update_to_in_position(id, radar_list):
    for radar_list_dict in radar_list:
        if radar_list_dict['id'] == id:
            radar_list_dict['id'] = "IN_POSITION"

def get_trigger_price_to_close(price, factor_gain):

    trigger_price = round(float(factor_gain) * float(price), adaperp_decimals)
    print("in " + funcname() + ", parameter price:", price)
    print("in " + funcname() + ", parameter factor_gain:", factor_gain)
    print(".... trigger_price: " + str(trigger_price))
    return trigger_price

def dump_radar_list(radar_list):
    with open("radar_list.txt", "w") as f:
        f.write(str(radar_list))

def check_existence_radar_list_in_disc():
    if os.path.exists("radar_list.txt"):
        print("in " + funcname() + ", radar_list.txt exists in disk") 
    else:
        print("in " + funcname() + ", radar_list.txt not exists, aborting")
        sys.exit(66)


def list_pivots_in_radar_list_in_disk():
    with open("radar_list.txt", "r") as f:
        try:
            radar_list_from_disk = f.read().replace("'", '"')
            #print("radar_list_from_disk: " + str(radar_list_from_disk))
            #print("radar_list_from_disk is type: " + str(type(radar_list_from_disk)))
            radar_list = json.loads(radar_list_from_disk)
            #print("res_list is type: " + str(type(res_list)))
            #print("res_list: " + str(res_list))
            for i in radar_list:
                print("pivot: " + str(i))
            return radar_list
        except:
                err = "except in " + funcname() + ", error: " + str(sys.exc_info()) + ", aborting"
                print(err)
                sys.exit(66)

def get_radar_list():
    #https://docs.python.org/2/library/sqlite3.html
    conn = create_db_conn()
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("select * from radar_list")
    #print(cur.fetchone()["order_id"])
    result = cur.fetchall()
    #print("str result is type: " + str(type(result)))
    #print("in get_radar_list result: " + str(result))
    return result