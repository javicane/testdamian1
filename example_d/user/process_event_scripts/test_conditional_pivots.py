import sys
from binance_d.example_d.user.helpers_scripts.helpers_module import funcname, get_radar_list, create_dict_from_output
from binance_d.example_d.user.common_scripts.create_orders_module import silent_limit_no_oco_sell_long
from binance_d.example_d.user.common_scripts.create_pivot_module import exec_transaction_pivot, exec_transaction_pivot_conditional
from binance_d.example_d.user.helpers_scripts.sql import exec_sql
from binance_d.impl.utils.timeservice import get_current_timestamp


def process_conditional_pivot(p_price):
    '''
    caller is local process_pnl
    arguments:
        p_price: tp
    '''
    # primer paso check si hay pivot conditional a crear con el tp recibido por argumento
    sql = "select trigger_price_to_put_in_position, trigger_price_to_close, original_quantity, repeat from "
    sql += "conditional_pivots where active='Y' and main_trigger_price='" + str(p_price) + "'" 
    result = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error sql conditional_pivots")
    print("check table conditional_pivots result:", result)
    print("result type:", type(result))
    repeat_conditional_pivot = "N"
    if result: # is a list of tuples
        print("result true, conditional pivot start process")
        print("in,", funcname(), ", ok proceed to create conditional pivot")
        for item_tuple in result:
            tp = item_tuple[0]
            tc = item_tuple[1] 
            size = item_tuple[2]
            repeat_conditional_pivot = item_tuple[3]
        result_dict = dict(tp=tp, tc=tc, size=size)
        print("conditional pivot to create, result_dict:", result_dict)
        print("in", funcname(), ", check if conditional pivot already exists")
        #sql = "select * from radar_list_test_conditional where conditional ='Y' and "
        sql = "select case when count(*) = 0 then 0 "
        sql += "else count(*) end as num_rows "
        sql += "from radar_list_test_conditional where conditional='Y' and "
        sql += "(trigger_price_to_put_in_position, trigger_price_to_close, original_quantity) in "
        sql += "(select trigger_price_to_put_in_position, trigger_price_to_close, original_quantity from "
        sql += "conditional_pivots where active='Y' and main_trigger_price='" + str(p_price) + "')"  
        result_already_exists = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error sql conditional_pivots")
        print("conditional_pivot check result_already_exists:", result_already_exists)
        print("conditional_pivot check result_already_exists type:", type(result_already_exists))
        num_rows = 0
        for num_rows_tuple in result_already_exists:
            num_rows = num_rows_tuple[0]
            print("num_rows:", num_rows)
        if num_rows == 0:
            print("conditional_pivot not exists, create") 
            try:
                #pass
                exec_transaction_pivot_conditional(tp, tc, size)
            except:
                pass
        else:
            print("conditional_pivot already exists, check if we can repeat") 
            if repeat_conditional_pivot == "Y":
                print("check = Y, proceed to repeat_conditional_pivot:", repeat_conditional_pivot)
                try:
                    #pass
                    exec_transaction_pivot_conditional(tp, tc, size)
                    print("return to root caller")
                    return
                except:
                    pass
            else:
                print("check repeat_conditional_pivot:", repeat_conditional_pivot)
    else:
        print("no proceed to create conditional pivot, sql result empty")
    message = "in " + funcname() + ", return only"
    return message

process_conditional_pivot(1)