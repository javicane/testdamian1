import os
import sys
import collections
import memcache

from math import ceil
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import NoteSerializer
from .models import Notes
from collections import OrderedDict
from binance_d.impl.utils.timeservice import get_current_timestamp
from binance_d.example_d.user.helpers_scripts.sql import exec_sql, create_db_conn
from datetime import datetime
import datetime
import time
import pandas as pd
from binance_d.example_d.user.check_dangling_scripts.dangling_module import check_dangling_before_starting_websocket 
from binance_d.example_d.user.frontend_scripts.create_sell_order_frontend import create_sell_order_frontend
from binance_d.example_d.user.frontend_scripts.create_pivot_buy_frontend import create_pivot_buy_frontend
from binance_d.example_d.user.frontend_scripts.cancel_order_frontend_module import cancel_order_frontend, cancel_order_bulk_by_price_range_frontend
from binance_d.example_d.user.frontend_scripts.resize_pivot_frontend_module import resize_pivot_frontend
from binance_d.example_d.user.frontend_scripts.update_repeat_pivot_frontend_module import update_repeat_pivot_frontend
from binance_d.example_d.user.frontend_scripts.pivot_frequency_frontend_module import query_pivot_frequency_frontend
from binance_d.example_d.user.frontend_scripts.resize_order_frontend_module import resize_order_buy_frontend 
from binance_d.example_d.user.frontend_scripts.pnl_frequency_frontend_module import query_pnl_frequency_frontend
from binance_d.example_d.user.frontend_scripts.update_group_id_frontend_module import update_group_id_frontend

from binance_d.general_settings import adaperp_decimals
try:
    memcached_conn = memcache.Client(['localhost:11211'], debug=0)
except:
    print("except memcached not working:", sys.exc_info())

# Create your views here.
def front(request):
    context = {
        }
    return render(request, "index.html", context)

@api_view(['GET'])
def query_last20pnl_duration(request):
    if request.method == 'GET':
        timestamp_epoch = get_current_timestamp()
        #print("timestamp_epoch from get_current_timestamp:", timestamp_epoch)
        old_time = datetime.datetime.now()
        new_time = old_time - datetime.timedelta(hours=3)
        date_time = new_time.strftime("%d/%m/%Y, %H:%M:%S")
        current_time_string = date_time
       # data_dict = dict(id=35)
        query = "select timestamp/1000 tt from tracker_pnl order by timestamp asc"
     
        df = pd.read_sql(query, con = create_db_conn())
        df2 = df.diff() # hace la diferencia entre row y previous row

        last20pnl_list = []  
        for index, row in df2.tail(20).iterrows():
            last20pnl_list.append(row['tt'])
            #print("row: " + str(row['tt']))
#        print("last20pnl_list: " + str(last20pnl_list))
        last20pnl_list.reverse() # reverse order to new..old
#        print("last20pnl_list reverse: " + str(last20pnl_list))

        query = "select rp from tracker_pnl order by timestamp desc limit 20" 
        df = pd.read_sql(query, con = create_db_conn())
        last20rp_list = []
        for index, row in df.iterrows():
            last20rp_list.append(row['rp'])
       
        #data = [OrderedDict([('id', 35), ('date_now', current_time_string), ('timestamp_epoch', timestamp_epoch), 
        #                     ('last20pnl_list', last20pnl_list), ('last20rp_list', last20rp_list)])]
        #query = "select datetime(ROUND(max(timestamp)/ 1000) -10800, 'unixepoch') from tracker_pnl;"
        query = "select max(timestamp) from tracker_pnl;"
        last_pnl_timestamp = exec_sql(sql = query, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error sql last_pnl_timestamp")[0]
        #print("last_pnl_timestamp", last_pnl_timestamp)

        seconds_since_last_pnl = ceil((timestamp_epoch/1000) - (last_pnl_timestamp/1000))
        #print("seconds_since_last_pnl:", seconds_since_last_pnl)

        # cuantos pnl en las ultimas 24 hs
        days_number = 1
        seconds_number = days_number*24*60*60
        sql = "select count(*)/" + str(days_number) + " from tracker_pnl where " 
        sql += "timestamp/1000 >= " + str(ceil( (timestamp_epoch/1000) - seconds_number )) + ";"
        count_24hs = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error sql count_24hs")[0]
        #print("sql count_24hs:", sql) 
        #print("count_24hs:", count_24hs)
        days_number = 7
        seconds_number = days_number*24*60*60
        sql = "select count(*)/" + str(days_number) + " from tracker_pnl where " 
        sql += "timestamp/1000 >= " + str(ceil( (timestamp_epoch/1000) - seconds_number )) + ";"
        count_7days = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error sql count_24hs")[0]
  
        data = [{'count_7days': count_7days, 'count_24hs': count_24hs, 'date_now': current_time_string, 'timestamp_epoch': timestamp_epoch, 
                 'last20pnl_list': last20pnl_list, 'last20rp_list': last20rp_list, 'seconds_since_last_pnl': seconds_since_last_pnl}]
        #print("dangling data: " + str(data))
        return Response(data)

@api_view(['GET'])
def check_dangling(request):
    if request.method == 'GET':
        timestamp_epoch = get_current_timestamp()
        old_time = datetime.datetime.now()
        new_time = old_time - datetime.timedelta(hours=3)
        date_time = new_time.strftime("%d/%m/%Y, %H:%M:%S")
        current_time_string = date_time
        data_dict = dict(id=35)
        # return flag_dangling, flag_partially_filled, flag_expired
        dangling, flag_partially_filled, flag_expired, flag_dangling_check1_only, result_dangling_check1, flag_dangling_check2, flag_dangling_check3, flag_dangling_check4, result_dangling_check4, flag_possible_database_locked = check_dangling_before_starting_websocket("silent")
 
        #data = [OrderedDict([('id', 35), ('date_now', current_time_string), ('timestamp_epoch', timestamp_epoch), 
        #                     ('dangling', dangling)])]
        
        data = [{'date_now': current_time_string, 'timestamp_epoch': timestamp_epoch, 
                 'flag_possible_database_locked': flag_possible_database_locked,
                 'dangling': dangling, 'partially_filled': flag_partially_filled, 'expired': flag_expired,
                 'flag_dangling_check1_only': flag_dangling_check1_only, 'result_dangling_check1': result_dangling_check1,
                 'flag_dangling_check2': flag_dangling_check2, 'flag_dangling_check3': flag_dangling_check3,
                 'flag_dangling_check4': flag_dangling_check4, 'result_dangling_check4': result_dangling_check4}]
        #print("dangling data: " + str(data))
        return Response(data)

@api_view(['GET'])
def check_now_view(request):
    if request.method == 'GET':
        timestamp_epoch = get_current_timestamp()
        old_time = datetime.datetime.now()
        new_time = old_time - datetime.timedelta(hours=3)
        date_time = new_time.strftime("%d/%m/%Y, %H:%M:%S")
        current_time_string = date_time
        data_dict = dict(id=35)
        
        #### previous pivot
        sql = "select "
        sql += "trigger_price_to_put_in_position,"
        sql += "trigger_price_to_close,"
        sql += "original_quantity,"
        sql += "resize,"
        sql += "order_id,"
        sql += "repeat"
        sql += " from radar_list"
        sql += " where "
        sql += "trigger_price_to_put_in_position in "
        sql += "( select max(trigger_price_to_put_in_position) from radar_list where order_status ='NEW') and order_status='NEW'"
        #print(sql)
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error sql nearest price")
        #print("res_sql", res_sql)
        if res_sql:
            previous_pivot_list_of_dicts = [{'tp':a[0], 'tc':a[1],'size':a[2],'resize':a[3], 'order_id':a[4],'repeat':a[5]
                                            } for a in res_sql] #convert list of tuples in list of dicts
        else:
            previous_pivot_list_of_dicts = [{'tp':'0', 'tc':'0','size':'0','resize':'0', 'order_id':'0'}]
        
        #print("previous_pivot_list_of_dicts:", previous_pivot_list_of_dicts)
        ####
        #### active pivot
        sql = "select max(trigger_price_to_put_in_position) from radar_list where order_status ='NEW'"
        prev_pivot_tp = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", 
                                                    fetch_type = "fetchone", error_message = "error sql nearest price")[0]
        #print("prev_pivot_tp:", prev_pivot_tp)
        #sql = "select trigger_price_to_put_in_position from radar_list where trigger_price_to_close in "
        #sql += "(select min(trigger_price_to_close) from radar_list where order_status = 'IN_POSITION');"
        #active_pivot = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error sql active_pivot")[0]
        
        sql = "select trigger_price_to_put_in_position,"
        sql += "original_quantity,"
        sql += "resize,"
        sql += "trigger_price_to_close,"
        sql += "repeat"
        sql += " from radar_list where "
        sql += "order_status = 'IN_POSITION' and "
        sql += "trigger_price_to_close in "
        sql += "(select min(trigger_price_to_close) from radar_list where order_status = 'IN_POSITION') order by 1 desc;"
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone",
                           error_message = "error sql ")
        if not res_sql:
            #print("res_sql empty:", res_sql)
            active_pivot = 666
            active_pivot_pnl = 666
            size = 666
            resize = 666
            repeat = "U"
        else:
            active_pivot = res_sql[0]
            active_pivot_pnl = res_sql[3]
            size = res_sql[1]
            resize = res_sql[2]
            repeat = res_sql[4]
        # fetchall
        sql = "select trigger_price_to_put_in_position,"
        sql += "trigger_price_to_close,"
        sql += "original_quantity,"
        sql += "resize,"
        sql += "order_id"
        sql += " from radar_list where "
        sql += "order_status = 'IN_POSITION' and "
        sql += "trigger_price_to_close in "
        sql += "(select min(trigger_price_to_close) from radar_list where order_status = 'IN_POSITION') order by 1 desc;"
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall",
                           error_message = "error sql ")
        #print("res_sql", res_sql)
        current_pivot_list_of_dicts = [{'tp':a[0], 'tc':a[1],'size':a[2],'resize':a[3], 'order_id':a[4]
                                       } for a in res_sql] #convert list of tuples in list of dicts
        #print("current_pivot_list_of_dicts", current_pivot_list_of_dicts) 
        ####
        #### next pivot
        # using active pivot tp
        sql = "select min(trigger_price_to_put_in_position),"
        sql += "trigger_price_to_close,"
        sql += "original_quantity,"
        sql += "resize,"
        sql += "order_id,"
        sql += "repeat"
        sql += " from radar_list "
        sql += "where order_status='IN_POSITION' and "
        sql += "trigger_price_to_put_in_position > " + str(active_pivot) 
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error query next pivot")
        next_pivot_list_of_dicts = [{'tp':a[0], 'tc':a[1],'size':a[2],'resize':a[3], 'order_id':a[4], 'repeat':a[5]
                                       } for a in res_sql] #convert list of tuples in list of dicts
        

        ####
        # using active_pivot_pnl as distance ( the trigger_price_to_close of active pivot)
        sql = "select trigger_price_to_put_in_position,"
        sql += "trigger_price_to_close,"
        sql += "min(trigger_price_to_put_in_position - " + str(active_pivot_pnl) + "),"
        sql += "original_quantity,"
        sql += "resize,"
        sql += "order_id,"
        sql += "repeat"
        sql += " from radar_list "
        sql += "where order_status='IN_POSITION' and "
        sql += "trigger_price_to_close > " + str(active_pivot_pnl) 
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error query next pivot")
        #next_pivot_list_of_dicts = [{'tp':a[0], 'tc':a[1],'size':a[3],'resize':a[4], 'order_id':a[5], 'repeat':a[6]
         #                              } for a in res_sql] #convert list of tuples in list of dicts
        
        ####
        sql = "select round(entry_price,5) from tracker_entry_price;"
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "query tracker_entry_price")
        entry_price = res_sql[0]
        #pivots to entry
        sql = "select count(*) from radar_list where "
        sql += "trigger_price_to_close <= (select min(trigger_price_to_close) from radar_list "
        sql += "where trigger_price_to_close >= " + str(entry_price) + ") and "
        sql += "trigger_price_to_close >= " + str(active_pivot_pnl)
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "query pivot_to_entry")
        pivots_to_entry = res_sql[0]
        #print("pivots_to_entry:", pivots_to_entry)
        #last line of a file

        # deep ( count(*) pivots IN_POSITION)
        sql = "select count(*) from radar_list where order_status='IN_POSITION';"
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "query pivot_count_in_position")
        pivot_count_in_position = res_sql[0]
        #print("pivot_count_in_position", pivot_count_in_position)

        # pvts (count(*) pivots )
        sql = "select count(*) from radar_list where order_status not like 'PNL';"
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "query pivot_count_total")
        pivot_count_total = res_sql[0]
        #print("pivot_count_total", pivot_count_total)
        '''
        with open("/tmp/supervisord_websocket_user.out.log", "rb") as file:
            try:
                file.seek(-2, os.SEEK_END)
                while file.read(1) != b'\n':
                    file.seek(-2, os.SEEK_CUR)
            except OSError:
                file.seek(0)
            last_line_websocket = file.readline().decode()[:-1]
        '''
            #print(last_line + "---")
        # read last two lines
        with open('/tmp/supervisord_websocket_user.out.log', 'rb') as file:
            last_lines_websocket = []
            for line in reversed(list(file)):
                decoded_line = line.decode().strip()
                if decoded_line:
                    #print("decoded_line", decoded_line)
                    last_lines_websocket.append(decoded_line)
                    if len(last_lines_websocket) == 3:
                        break
            last_lines_websocket.reverse()
        last_line_websocket=""
        for i in last_lines_websocket:
            last_line_websocket += i + "||"
#        print(last_line_websocket)
        #print(second_last_line_websocket + "---")
        #print(last_line_websocket + "---")

        #data = [OrderedDict([('id', 35), ('date_now', current_time_string), ('timestamp_epoch', timestamp_epoch), 
        #                     ('nearest_pnl', nearest_pnl),
        #                     ('nearest_price_to_put_in_position', nearest_price_to_put_in_position)])]
        try: 
            tc = active_pivot_pnl
            tp = prev_pivot_tp
            #print("")
            goal = 10400
            market_price_aprox = tp
            contract_unit = 10 # 10 usd 
            ada_quantity = ( contract_unit * size ) / market_price_aprox
            #print("ada_quantity", ada_quantity)
            gain_per_pivot = ( tc - tp ) * ada_quantity
            #print("gain_per_pivot:", gain_per_pivot)
            #cuantas veces debo repetir el pivot current para llegar a ganar goal
            to_goal = int(( goal / gain_per_pivot ))
            #print("to_goal:", to_goal)
        except:
            to_goal = "666"
        markprice = "666"
        try:
                #markprice = str(round(float(memcached_conn.get('markprice')), 6))
      #          value = "666"
            value = 666
            if memcached_conn is not None:
                value = memcached_conn.get('markprice')
                if value is not None:
                    markprice = str(round(float(value), 6))
        except:
            print("except reading cached markprice :", sys.exc_info())
            markprice = "memcached_down!!!"
            nada = 1

        check_run_fake_order = "in_views"
        try:
            check_run_fake_order = memcached_conn.get('check_run_fake_order')
        except:
            print("except reading cached check_run_fake_order:", sys.exc_info())
            check_run_fake_order = "memcached_down!!!"
            nada = 1
        #print("check_run_fake_order:", check_run_fake_order)
        todo_junto = str(current_pivot_list_of_dicts) + "|||" + str(previous_pivot_list_of_dicts)
        #previous_pivot_list_of_dicts = todo_junto

        # position_size
        sql = "select sum(original_quantity) from radar_list where order_status='IN_POSITION' ;"
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "query position_size")
        position_size = res_sql[0]

        data = [{'date_now': current_time_string, 'timestamp_epoch': timestamp_epoch, 
                'to_goal': to_goal,
                'pivots_to_entry': pivots_to_entry,
                'size': size,
                'resize': resize,
                'repeat': repeat,
                'active_pivot_pnl': active_pivot_pnl,
                #'nearest_price_to_put_in_position': nearest_price_to_put_in_position,
            #previous_pivot_list_of_dicts = [{'tp':'0', 'tc':'0','size':'0','resize':'0', 'order_id':'0'}]
                'prev_pivot_tp': prev_pivot_tp, 
                'next_pivot_list_of_dicts': str(next_pivot_list_of_dicts), 
                'nearest_price_to_put_in_position': str(previous_pivot_list_of_dicts),
                'current_pivot_list_of_dicts': str(current_pivot_list_of_dicts),
                'active_pivot': active_pivot,
                'last_line_websocket': last_line_websocket,
                'pivot_count_in_position': pivot_count_in_position,
                'pivot_count_total': pivot_count_total,
                'markprice': markprice,
                'check_run_fake_order': check_run_fake_order,
                'entry_price': entry_price,
                'position_size': position_size}]
        #print("Mark Price:", markprice)
        #return Response(data_ordereddict)
        
        return Response(data)


@api_view(['GET'])
def query_min_pivot_view(request):
    if request.method == 'GET':
        timestamp_epoch = get_current_timestamp()
        sql = "select min(trigger_price_to_put_in_position) from radar_list where order_status='NEW';"
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "query_min_pivot")
        min_pivot = res_sql[0]
        old_time = datetime.datetime.now()
        new_time = old_time - datetime.timedelta(hours=3)
        date_time = new_time.strftime("%d/%m/%Y, %H:%M:%S")
        current_time_string = date_time
        #data = [OrderedDict([('id', 35), ('date_now', current_time_string), ('timestamp_epoch', timestamp_epoch), ('min_pivot', min_pivot)])]
        data = [{'date_now': current_time_string, 'timestamp_epoch': timestamp_epoch, 'min_pivot': min_pivot}]
        #print("data: " + str(data))
        return Response(data)

@api_view(['GET'])
def query_tracker_pnl_view(request):
    if request.method == 'GET':
        timestamp_epoch = get_current_timestamp()
        sql = "select round(sum(rp),5) , count(*) from tracker_pnl;"
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "query tracker_pnl")
        sum_rp = res_sql[0]
        rows = res_sql[1]

        pnl_dict_last7days = query_pnl_frequency_frontend(7) 
        sum_rp_last7days = pnl_dict_last7days['sum_rp']
        count_rp_last7days = pnl_dict_last7days['count']

        pnl_dict_last48hs = query_pnl_frequency_frontend(2) 
        sum_rp_last48hs = pnl_dict_last48hs['sum_rp']
        count_rp_last48hs = pnl_dict_last48hs['count']

        pnl_dict_last24hs = query_pnl_frequency_frontend(1) 
        # returns a dict {'sum_rp': -63.57425, 'count': 4055}
        sum_rp_last24hs = pnl_dict_last24hs['sum_rp']
        count_rp_last24hs = pnl_dict_last24hs['count']
        #print("pnl_dict_last24hs", pnl_dict_last24hs)

        pnl_dict_last12hs = query_pnl_frequency_frontend(0.5) 
        sum_rp_last12hs = pnl_dict_last12hs['sum_rp']
        count_rp_last12hs = pnl_dict_last12hs['count']
        #print("pnl_dict_last12hs", pnl_dict_last12hs)

        pnl_dict_last6hs = query_pnl_frequency_frontend(0.25) 
        sum_rp_last6hs = pnl_dict_last6hs['sum_rp']
        count_rp_last6hs = pnl_dict_last6hs['count']
        #print("pnl_dict_last6hs", pnl_dict_last6hs)

        sql = "select round(balance,4) from tracker_balance;"
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "query tracker_balance")
        balance = res_sql[0]
        
        sql = "select round(sum(fee),5), count(*) from tracker_funding_fee;"
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "query tracker_balance")
        sum_funding_fee = res_sql[0]
        rows_funding_fee = res_sql[1]


        sql = "select round(entry_price,5) from tracker_entry_price;"
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "query tracker_entry_price")
        entry_price = res_sql[0]

        #print("sum_rp: " + str(sum_rp))
        #data = [OrderedDict([('id', 35), ('title', timestamp_epoch), ('content', 'nn')]), OrderedDict([('id', 37), ('title', 'n3'), ('content', 'n3')])]
        #res_sql = 666
        old_time = datetime.datetime.now()
        new_time = old_time - datetime.timedelta(hours=3)
        date_time = new_time.strftime("%d/%m/%Y, %H:%M:%S")
        #print(date_time )
        #t = time.localtime() 
        #current_time_string = time.strftime("%d/%m/%Y %H:%M:%S", t)
        current_time_string = date_time
        #print(current_time_string)
        #data = [OrderedDict([('id', 35), ('date_now', current_time_string), ('timestamp_epoch', timestamp_epoch), ('sum_rp', sum_rp), ('rows', rows)])]
        data = [{'sum_rp_last7days': sum_rp_last7days, 'count_rp_last7days': count_rp_last7days, 'sum_rp_last48hs': sum_rp_last48hs, 'count_rp_last48hs': count_rp_last48hs, 'sum_rp_last6hs': sum_rp_last6hs, 'count_rp_last6hs': count_rp_last6hs, 'sum_rp_last12hs': sum_rp_last12hs, 'count_rp_last12hs': count_rp_last12hs, 'sum_rp_last24hs': sum_rp_last24hs, 'count_rp_last24hs': count_rp_last24hs, 'date_now': current_time_string, 'timestamp_epoch': timestamp_epoch, 'sum_rp': sum_rp, 'rows': rows, 'balance': balance,
                 'sum_funding_fee': sum_funding_fee, 'rows_funding_fee': rows_funding_fee, 'entry_price': entry_price}]
        #print("data: " + str(data))
        return Response(data)

@api_view(['GET', 'POST'])
def post_query_pivots(request):
    if request.method == 'POST':
        qdict = request.data
        #print("qdict: " + str(qdict))
        price_begin = qdict['price_begin']
        price_end = qdict['price_end']

        
        timestamp_epoch = get_current_timestamp()
        old_time = datetime.datetime.now()
        new_time = old_time - datetime.timedelta(hours=3)
        date_time = new_time.strftime("%d/%m/%Y, %H:%M:%S")
        #print(date_time )
        current_time_string = date_time
        #print(current_time_string)

        query = "select printf('%." + str(adaperp_decimals) + "f', trigger_price_to_put_in_position)||' '||original_quantity||' '||resize tp from radar_list where ( trigger_price_to_put_in_position >= " + str(price_end) + " and "
        #query = "select trigger_price_to_put_in_position ||' '||original_quantity tp from radar_list where trigger_price_to_put_in_position >= " + str(price_end) + " and "
        query += "trigger_price_to_put_in_position <= " + str(price_begin) + ") and order_status not like 'PNL' order by trigger_price_to_put_in_position desc " 
        df = pd.read_sql(query, con = create_db_conn())
        #print(df) 
        pivots_list = []
        for index, row in df.iterrows():
            pivots_list.append(row['tp'])
        #data = [OrderedDict([('id', 35), ('date_now', current_time_string), ('timestamp_epoch', timestamp_epoch), 
        #                     ('pivots_list', pivots_list)])]
        data = [{'date_now': current_time_string, 'timestamp_epoch': timestamp_epoch,
                 'pivots_list': pivots_list}]
        #print("data: " + str(data))
        return Response(data)

@api_view(['GET', 'POST'])
def note(request):

    if request.method == 'GET':
        note = Notes.objects.all()
        serializer = NoteSerializer(note, many=True)
        #print(serializer.data)
        #print("serializer.data is type: " + str(type(serializer.data)))
        #[OrderedDict([('id', 35), ('title', 'nn'), ('content', 'nn')]), OrderedDict([('id', 37), ('title', 'n3'), ('content', 'n3')])]
        #serializer.data is type: <class 'rest_framework.utils.serializer_helpers.ReturnList'>
        timestamp_epoch = get_current_timestamp()
        #data = [OrderedDict([('id', 35), ('title', timestamp_epoch), ('content', 'nn')]), OrderedDict([('id', 37), ('title', 'n3'), ('content', 'n3')])]
        data = [OrderedDict([('id', 35), ('title', timestamp_epoch), ('content', 'nn')])]
        return Response(data)
        #return Response(serializer.data)
        #return JsonResponse(data)

    elif request.method == 'POST':
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def note_detail(request, pk):
    try:
        note = Notes.objects.get(pk=pk)
    except Notes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def query_pivots_by_price_range_view(request):
    if request.method == 'GET':
        timestamp_epoch = get_current_timestamp()
        sql = "select min(trigger_price_to_put_in_position) from radar_list where order_status='NEW';"
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "query_min_pivot")
        min_pivot = res_sql[0]
        old_time = datetime.datetime.now()
        new_time = old_time - datetime.timedelta(hours=3)
        date_time = new_time.strftime("%d/%m/%Y, %H:%M:%S")
        current_time_string = date_time
        #data = [OrderedDict([('id', 35), ('date_now', current_time_string), ('timestamp_epoch', timestamp_epoch), ('min_pivot', min_pivot)])]
        data = [{'date_now':current_time_string, 'timestamp_epoch': timestamp_epoch, 'min_pivot': min_pivot},
                {'date_now':current_time_string, 'timestamp_epoch': timestamp_epoch, 'min_pivot': min_pivot},]
        data = [{'pivots':'hola', 'size': 'hola', 'resize':'hola' }, ]
        #print("data: " + str(data))
        return Response(data)        

    if request.method == 'POST':
        qdict = request.data
        #print("qdict: " + str(qdict))
        price_begin = qdict['price_begin']
        price_end = qdict['price_end']

        
        timestamp_epoch = get_current_timestamp()
        old_time = datetime.datetime.now()
        new_time = old_time - datetime.timedelta(hours=3)
        date_time = new_time.strftime("%d/%m/%Y, %H:%M:%S")
        #print(date_time )
        current_time_string = date_time
        #print(current_time_string)



        '''
        active_pivot_sql = " case "
        active_pivot_sql += "when trigger_price_to_put_in_position in "
        active_pivot_sql += "( select trigger_price_to_put_in_position from radar_list where trigger_price_to_close in "
        active_pivot_sql += "(select min(trigger_price_to_close) from radar_list where order_status = 'IN_POSITION') ) "
        active_pivot_sql += "then 'active' else 'n' "
        active_pivot_sql += "end active_pivot "

        sql = "select order_id_to_close, order_id, trigger_price_to_put_in_position, original_quantity, resize, repeat, trigger_price_to_put_in_position tp, "
        sql += "trigger_price_to_close tc, printf('%.5f',100*((trigger_price_to_close/trigger_price_to_put_in_position)-1)) f_gain, "
        sql += active_pivot_sql
        sql += "from radar_list where ( trigger_price_to_put_in_position >= " + str(price_end) + " and "
        sql += "trigger_price_to_put_in_position <= " + str(price_begin) + ") and order_status in ('NEW','IN_POSITION') order by trigger_price_to_put_in_position desc " 
        '''
        active_pivot_sql = "case when trigger_price_to_put_in_position in "
        active_pivot_sql += "( select min(trigger_price_to_put_in_position) from radar_list where "
        active_pivot_sql += "order_id_to_close != 0 and order_status in ('IN_POSITION') ) " 
        active_pivot_sql += " then 'active' else 'n' end active_pivot, "
        
        sql = "select trigger_price_to_put_in_position pivot, "
        sql += "original_quantity size, "
        sql += "resize, "
        sql += "repeat, "
        sql += "trigger_price_to_close, "
        #sql += "printf('%.5f',100*((trigger_price_to_close/trigger_price_to_put_in_position)-1)) f_gain, "
        sql += "printf('%." + str(adaperp_decimals) + "f',100*(factor_gain-1)) f_gain, "
        sql += active_pivot_sql
        sql += "order_id, "
        sql += "order_id_to_close, "
        sql += "LAG ( trigger_price_to_put_in_position, 1, 'nada') OVER ( order by trigger_price_to_put_in_position ) previous_pivot, "
        sql += "printf('%." + str(adaperp_decimals) + "f', (( trigger_price_to_put_in_position/LAG( trigger_price_to_put_in_position, 1, 'nada') OVER ( order by trigger_price_to_put_in_position ) ) -1 )*100 ) previous_pivot_distance "
        sql += "from radar_list "
        sql += "where ( trigger_price_to_put_in_position >= " + str(price_end) + " and "
        sql += "trigger_price_to_put_in_position <= " + str(price_begin) + ") " 
        sql += "and order_status in ('NEW', 'IN_POSITION') "
        sql += "order by trigger_price_to_put_in_position desc, previous_pivot desc;"

        #print(sql)
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "query_min_pivot")
        #print("res_sql: ", res_sql)
        res_dict = [{'pivot':a[0], 'size':a[1],'resize':a[2],'repeat':a[3], 'tc':a[4], 
                     'f_gain':a[5], 'active_pivot':a[6], 'order_id':a[7], 'order_id_to_close':a[8],
                      'previous_pivot':a[9], 'previous_pivot_distance':a[10]} for a in res_sql] #convert list of tuples in list of dicts
        #res_dict = [{'order_id_to_close':a[0], 'order_id':a[1], 'pivot':a[2], 'size':a[3],'resize':a[4],'repeat':a[5], 'tp':a[6], 'tc':a[7], 
        #             'f_gain':a[8], 'active_pivot':a[9], 'previous_pivot_distance':a[10]} for a in res_sql] #convert list of tuples in list of dicts
        #print("res_dict: ", res_dict)
        #query = "select printf('%.5f', trigger_price_to_put_in_position)||' '||original_quantity||' '||resize tp from radar_list where ( trigger_price_to_put_in_position >= " + str(price_end) + " and "
        #query = "select trigger_price_to_put_in_position ||' '||original_quantity tp from radar_list where trigger_price_to_put_in_position >= " + str(price_end) + " and "
        #query += "trigger_price_to_put_in_position <= " + str(price_begin) + ") and order_status in ('NEW','IN_POSITION') order by trigger_price_to_put_in_position desc " 
        #df = pd.read_sql(query, con = create_db_conn())
        #print(df) 
        #pivots_list = []
        #for index, row in df.iterrows():
        #    pivots_list.append(row['tp'])
        #data = [{'date_now': current_time_string, 'timestamp_epoch': timestamp_epoch,
        #         'pivots_list': pivots_list}]
        #pivots_list = "hola"
        #data = [{'pivots':current_time_string, 'size': timestamp_epoch, 'resize': pivots_list}, ]
        data = res_dict
        #print("data: " , data)
        return Response(data)

@api_view(['POST'])
def create_sell_order_view(request):
    if request.method == 'POST':
        qdict = request.data
        #print("qdict: " + str(qdict))
        price_to_put_in_position = qdict['price_to_put_in_position']
        price_close = qdict['price_close']
        size = qdict['size']
        repeat = qdict['repeat']
        resize = qdict['resize']
        factor_gain = qdict['factor_gain']
        rc = create_sell_order_frontend(price_to_put_in_position, price_close, size, repeat, resize, factor_gain) 
        #rc = "testing" 
        #print("") 
        #print("rc in post_create_sell_view: ", rc) 
        data = ""
        if rc is not None:
            data = [{'result': rc['result'], 'order_id': rc['order_id'], 'order_id_to_close': rc['order_id_to_close'], 'price_to_put_in_position': price_to_put_in_position, 'price_close': price_close, 'size': size,
                 'repeat': repeat, 'resize': resize, 'factor_gain': factor_gain}]
        #print("data: " + str(data))
        return Response(data)

@api_view(['POST'])
def create_pivot_buy_view(request):
    if request.method == 'POST':
        qdict = request.data
        print("qdict: " + str(qdict))

        confirm_custom = qdict['confirm_custom']
        try:
            factor_gain = round(float(qdict['factor_gain']), adaperp_decimals)
            up_down = qdict['up_down']
            if confirm_custom != "Y":
                price = round(float(qdict['price']), adaperp_decimals)
            else:
                price = 0
            size = int(qdict['size'])
            repeat = qdict['repeat']
            resize = int(qdict['resize'])

            #custom tpos/tclose
            price_tpos = qdict['price_tpos']
            price_tclose = qdict['price_tclose']
            confirm_custom = qdict['confirm_custom']
        except:
            result = str(sys.exc_info())
            print("result except", result)
            data = [{'factor_gain': 'except', 'up_down': 'except'}]
            return Response(data)
           
        #data = [{'factor_gain': factor_gain, 'up_down': up_down}]
        #if price_tpos != "6666" and price_tclose != "6666":
        if confirm_custom == "Y": 
            price_tpos = round(float(qdict['price_tpos']), adaperp_decimals)
            price_tclose = round(float(qdict['price_tclose']), adaperp_decimals)
            if price_tpos < price_tclose: 
                print("ok custom prices")
                factor_gain = round(price_tclose/price_tpos, adaperp_decimals)
                print("in views factor_gain", factor_gain)
                up_down = 'CUSTOM'
        '''
        rc = dict(result="OKA",
                  order_id=666,
                  order_id_to_close=777,
                  price_to_put_in_position=1,
                  price_close=1 )
        '''

        rc = create_pivot_buy_frontend(up_down, price, size, repeat, resize, factor_gain, price_tpos, price_tclose)
        print("rc in views", rc)
        #when ok rc = {'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': 'new_pivot1670072110289', 'closePosition': 'False', 
        # 'cumBase': '0.0', 'executedQty': '0.0', 'orderId': '7925838768', 'origQty': '1.0', 'origType': 'LIMIT', 'positionSide': 'LONG', 
        # 'price': '0.14981', 'priceRate': 'None', 'reduceOnly': 'False', 'side': 'BUY', 'status': 'NEW', 'stopPrice': '0.0', 
        # 'symbol': 'ADAUSD_PERP', 'timeInForce': 'GTC', 'type': 'LIMIT', 'updateTime': '1670072113517', 'workingType': 'CONTRACT_PRICE', 
        # 'result': 'OK', 'price_close': 0.15 }
        data = [{'up_down': up_down, 'result': rc['result'], 'order_id': rc['orderId'], 'order_id_to_close': 0, 'price_to_put_in_position': rc['price'], 'price_close': rc['price_close'], 'size': size,
                 'repeat': repeat, 'resize': resize, 'factor_gain': factor_gain}]
        #print("data: " + str(data))
        #data = [{'result': rc['result']}]
        return Response(data)

@api_view(['POST'])
def resize_order_buy_view(request):
    if request.method == 'POST':
        qdict = request.data
        #print("qdict: " + str(qdict))
        order_id = qdict['order_id']
        try:
            new_size = int(qdict['new_size'])
        except:
            result = str(sys.exc_info())
            data = [{'result': result, 'order_id': 0, 'new_size': 0}]
            return Response(data)
           
        rc = resize_order_buy_frontend(order_id, new_size) 
        #print("") 
        #print("in cancel_order_view: ", rc)
        data = [{'result': rc['result'], 'order_id': rc['order_id'], 'new_size': rc['new_size']}]
        #print("data: " + str(data))
        return Response(data)

@api_view(['POST'])
def cancel_order_view(request):
    if request.method == 'POST':
        qdict = request.data
        #print("qdict: " + str(qdict))
        order_id_to_cancel = qdict['order_id_to_cancel']
        rc = cancel_order_frontend(order_id_to_cancel) 
        #print("") 
        #print("in cancel_order_view: ", rc)
        data = ""
        if rc is not None:
            data = [{'result': rc['result'], 'order_id': rc['order_id']}]
        #print("data: " + str(data))
        return Response(data)

@api_view(['POST'])
def cancel_order_bulk_by_price_range_view(request):
    if request.method == 'POST':
        qdict = request.data
        #print("qdict: " + str(qdict))
        price_high = qdict['price_high']
        price_low = qdict['price_low']
        rc = cancel_order_bulk_by_price_range_frontend(price_high, price_low) 
        #print("") 
        #print("in cancel_order_view: ", rc)
        data = [{'result': rc['result'], 'price_high': rc['price_high'], 'price_low': rc['price_low']}]
        #print("data: " + str(data))
        return Response(data)


@api_view(['POST'])
def resize_pivot_view(request):
    if request.method == 'POST':
        qdict = request.data
        #print("qdict: " + str(qdict))
        order_id = qdict['order_id']
        resize = qdict['resize']
        rc = resize_pivot_frontend(order_id, resize) 
        #rc = "testing" 
        #print("") 
        #print("rc in resize_pivot_voew: ", rc) 
        data = [{'result': rc['result'], 'order_id': rc['order_id'], 'resize': resize}]
        #print("data: " + str(data))
        return Response(data)        

@api_view(['GET', 'POST'])
def sql_query_view(request):
    if request.method == 'POST':
        qdict = request.data
        #print("qdict: " + str(qdict))
        order_id = qdict['order_id']
        order_id_to_close = qdict['order_id_to_close']
        
        timestamp_epoch = get_current_timestamp()
        old_time = datetime.datetime.now()
        new_time = old_time - datetime.timedelta(hours=3)
        date_time = new_time.strftime("%d/%m/%Y, %H:%M:%S")
        #print(date_time )
        current_time_string = date_time
        #print(current_time_string)
        #CREATE TABLE radar_list (order_id integer primary key,order_status text 
        # not null,order_id_to_close integer not null,trigger_price_to_put_in_position 
        # real not null,trigger_price_to_close real not null,original_quantity integer not null, 
        # clientorderid text not null, repeat text not null default "Y", resize integer not null default 1); 
        sql = "select order_id, "
        sql += "order_status, "
        sql += "order_id_to_close, "
        sql += "trigger_price_to_put_in_position, "
        sql += "trigger_price_to_close, "
        sql += "original_quantity, "
        sql += "clientorderid, "
        sql += "repeat, "
        sql += "resize, "
        sql += "factor_gain "
        sql += "from radar_list "
        sql += "where order_id='" + str(order_id) + "' or "
        sql += "order_id_to_close='" + str(order_id_to_close) + "' order by trigger_price_to_put_in_position desc;" 

        #print(sql)
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "query_min_pivot")
        #print("res_sql: ", res_sql)
        res_dict = [{'order_id':a[0], 'order_status':a[1],'order_id_to_close':a[2],'trigger_price_to_put_in_position':a[3], 'trigger_price_to_close':a[4], 
                     'original_quantity':a[5], 'clientorderid':a[6], 'repeat':a[7], 'resize':a[8], 'factor_gain':a[9]} for a in res_sql] #convert list of tuples in list of dicts
        data = res_dict
        #print("data: " , data)
        return Response(data)        

@api_view(['GET', 'POST'])
def query_top_pivots_to_increase_view(request):
    if request.method == 'POST':
        qdict = request.data
        #print("qdict: " + str(qdict))
        b_tp = qdict['b_tp']
        b_tc = qdict['b_tc']
        
        timestamp_epoch = get_current_timestamp()
        old_time = datetime.datetime.now()
        new_time = old_time - datetime.timedelta(hours=3)
        date_time = new_time.strftime("%d/%m/%Y, %H:%M:%S")
        current_time_string = date_time
        
        sql = "select order_id, "
        sql += "order_status, "
        sql += "order_id_to_close, "
        sql += "trigger_price_to_put_in_position, "
        sql += "trigger_price_to_close, "
        sql += "original_quantity, "
        sql += "clientorderid, "
        sql += "repeat, "
        sql += "resize, "
        sql += "factor_gain "
        sql += "from radar_list " 
        sql += "where "
        sql += "( trigger_price_to_put_in_position <= " + str(b_tp) + " and ( trigger_price_to_close > " + str(b_tp) + " and trigger_price_to_close <= " + str(b_tc) + " )) "
        sql += "or "
        sql += "((trigger_price_to_put_in_position >= " + str(b_tp) + " and trigger_price_to_put_in_position < " + str(b_tc) + " ) and "
        sql += "(trigger_price_to_close >= " + str(b_tc) + " )) "
        sql += "order by trigger_price_to_put_in_position desc;"
        #print(sql)
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "query_min_pivot")
        #print("res_sql: ", res_sql)
        res_dict = [{'order_id':a[0], 'order_status':a[1],'order_id_to_close':a[2],'trigger_price_to_put_in_position':a[3], 'trigger_price_to_close':a[4], 
                     'original_quantity':a[5], 'clientorderid':a[6], 'repeat':a[7], 'resize':a[8], 'factor_gain':a[9]} for a in res_sql] #convert list of tuples in list of dicts
        data = res_dict
        #print("data: " , data)
        return Response(data)        

@api_view(['POST'])
def update_group_id_view(request):
    if request.method == 'POST':
        qdict = request.data
        #print("qdict: " + str(qdict))
        order_id = qdict['order_id']
        group_id = qdict['group_id']
        rc = update_group_id_frontend(order_id, group_id) 
        data = [{'result': rc['result'], 'order_id': rc['order_id']}]
        #print("data: " + str(data))
        return Response(data)

@api_view(['POST'])
def update_repeat_pivot_view(request):
    if request.method == 'POST':
        qdict = request.data
        #print("qdict: " + str(qdict))
        order_id = qdict['order_id']
        rc = update_repeat_pivot_frontend(order_id) 
        data = [{'result': rc['result'], 'order_id': rc['order_id']}]
        #print("data: " + str(data))
        return Response(data)        

@api_view(['GET', 'POST'])
def show_group_id_view(request):
    nada = 1
    if request.method == 'POST':
        qdict = request.data
        #print("qdict: " + str(qdict))
        price_begin = qdict['price_begin']
        price_end = qdict['price_end']
        
        sql = "select trigger_price_to_put_in_position pivot, "
        sql += "original_quantity size, "
        sql += "resize, "
        sql += "repeat, "
        sql += "trigger_price_to_close, "
        sql += "printf('%." + str(adaperp_decimals) + "f',100*(factor_gain-1)) f_gain, "
        sql += "order_id, "
        sql += "order_id_to_close, "
        sql += "group_id "
        sql += "from radar_list "
        sql += "where ( trigger_price_to_put_in_position >= " + str(price_end) + " and "
        sql += "trigger_price_to_put_in_position <= " + str(price_begin) + ") " 
        sql += "and order_status in ('NEW', 'IN_POSITION') "
        sql += "order by group_id, trigger_price_to_put_in_position desc"
       

        #print(sql)
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "query_show_group_id")
        #print("res_sql: ", res_sql)
        res_dict = [{'pivot':a[0], 'size':a[1],'resize':a[2],'repeat':a[3], 'tc':a[4], 
                     'f_gain':a[5], 'order_id':a[6], 'order_id_to_close':a[7],
                     'group_id':a[8]} for a in res_sql] #convert list of tuples in list of dicts
        data = res_dict
        #print("data: " , data)
        return Response(data) 

@api_view(['GET', 'POST'])
def drift_report_pivot_distance_view(request):
    if request.method == 'POST':
        qdict = request.data
        #print("qdict: " + str(qdict))
        high_price_pivot = qdict['price_end']
        low_price_pivot = qdict['price_begin']
        #r = round(float(desired_factor_gain), 5)
        #print("r:", r)
        #r = r -1
        #print("r:", r)
        #fg_percentage = round(100*(float(desired_factor_gain) - 1), adaperp_decimals)
        #print("fg_percentage: ", fg_percentage)
        
        #print("high_price_pivot:", high_price_pivot) 
        #print("low_price_pivot:", low_price_pivot)
        if high_price_pivot == "":
            high_price_pivot = 999 
            low_price_pivot = 0.1 
        
        timestamp_epoch = get_current_timestamp()
        old_time = datetime.datetime.now()
        new_time = old_time - datetime.timedelta(hours=3)
        date_time = new_time.strftime("%d/%m/%Y, %H:%M:%S")
        #print(date_time )
        current_time_string = date_time
        #print(current_time_string)

       # active_pivot_sql = "case when trigger_price_to_put_in_position in "
       # active_pivot_sql += "( select min(trigger_price_to_put_in_position) from radar_list where "
       # active_pivot_sql += "order_id_to_close != 0 and order_status in ('IN_POSITION') ) " 
       # active_pivot_sql += " then 'active' else 'n' end active_pivot, "

        active_pivot_sql = "case when trigger_price_to_put_in_position in "
        active_pivot_sql += "( select trigger_price_to_put_in_position from radar_list where trigger_price_to_close in "
        active_pivot_sql += "(select min(trigger_price_to_close) from radar_list where order_status = 'IN_POSITION' and order_id_to_close != 0 ) ) "
        active_pivot_sql += " then 'active' else 'n' end active_pivot, "
        '''
        drift_pivot_distance_sql = "case "  
        drift_pivot_distance_sql += "when f_gain - previous_pivot_distance > 0 then 'reduce f_gain ( cancel sell order and recreate with f_gain = '||previous_pivot_distance "
        drift_pivot_distance_sql += "when f_gain - previous_pivot_distance < 0 then 'create new pivot with price :'||pivot||' and distance:'||f_gain "
        drift_pivot_distance_sql += "when pivot=previous_pivot then 'duplicated, pivot=previous_pivot' "
        drift_pivot_distance_sql += "else 'other' end drift_pivot_distance "
        '''
        #not in use deviation = "ABS(previous_pivot_distance - " + str(fg_percentage) + ")/" + str(fg_percentage) + " "
        # not in use drift_pivot_distance_sql = "case "  
        #drift_pivot_distance_sql += "when pivot=previous_pivot then 'duplicated, pivot=previous_pivot' "
        #drift_pivot_distance_sql += "when " + deviation + " <= 0.01 then 'deviation < 1%, OK' "
        #not in use drift_pivot_distance_sql += "when " + deviation + " >=0  then " + deviation + " "
        #drift_pivot_distance_sql += "when " + deviation + " <= 0.01 then " + deviation + " "
        #drift_pivot_distance_sql += "when " + deviation + " >= 0.01 then 'HIGH, '||ABS(previous_pivot_distance - " + str(fg_percentage) + ")/" + str(fg_percentage) + " " 
        #drift_pivot_distance_sql += "when ABS(previous_pivot_distance - " + str(fg_percentage) + ")/" + str(fg_percentage) + " >= 0.01 then ABS(previous_pivot_distance - " + str(fg_percentage) + ")/" + str(fg_percentage)  + "||'H' "
        #no in use drift_pivot_distance_sql += "else 'other' end drift_pivot_distance "
    
        #new pivot_distance_deviation = "printf('%.5f', 100*ABS(previous_pivot_distance - " + str(fg_percentage) + ")/" + str(fg_percentage) + ") pivot_distance_deviation "

        sql_header = "select pivot, size, resize, repeat, trigger_price_to_close, f_gain, active_pivot, order_id, order_id_to_close, "
        sql_header += " previous_pivot, previous_pivot_distance, prev_tc, "
        
        #sql = sql_header
        #sql += "pivot_distance_deviation "
        #sql += "( "
        #sql += sql_header 
        #delta = 5
        delta = 5
        ## new
        #quasi_dup_percentage = 0.04
        #near_dup_high_percentage_low_threshold = 0.04
        #near_dup_high_percentage_high_threshold = 0.08
        #adjusted to accept f_gain 1.000625
        quasi_dup_percentage = 0.02
        near_dup_high_percentage_low_threshold = 0.02
        near_dup_high_percentage_high_threshold = 0.06

        result = "case "
        result += "when previous_pivot='nada' then 'nada' "
        result += "when pivot=previous_pivot then 'DUPLICATED, pivot=prev_pivot' "
        result += "when cast(previous_pivot_distance as real) <= " + str(quasi_dup_percentage) + " then 'QUASI DUPLICATED, DISTANCE% <= " +  str(quasi_dup_percentage) + "%' "
        result += "when cast(previous_pivot_distance as real) <= " + str(near_dup_high_percentage_high_threshold) + " then 'NEAR DUP High, ( " + str(near_dup_high_percentage_low_threshold) + "% < DISTANCE% <= " + str(near_dup_high_percentage_high_threshold) + "% )' "
        result += "when cast(pivot_distance_deviation as real) <= " + str(delta) + " then 'OK, DEVIATION% <= " + str(delta) + "%' "
        result += "when ( cast(pivot_distance_deviation as real) > " + str(delta) + " ) and ( cast(previous_pivot_distance as real) < f_gain )  then 'NEAR DUP Medium, (DEVIATION% > " + str(delta) + "% and DISTANCE% < f_gain% )' "
        result += "when cast(pivot_distance_deviation as real) > " + str(delta) + " then 'HIGH, DEVIATION% > " + str(delta) + "%' "
        #result += "when cast(pivot_distance_deviation as real) > 4 then 'HIGH, > 4%'"
        result += "else 'other' end result "
        
        result_gap = "case "
        result_gap += "when pivot=prev_tc then 'OK' "
        result_gap += "else 'GAP' end result_gap "

        sql = sql_header
        sql += "pivot_distance_deviation, "
        sql += result + ", "
        sql += result_gap
        sql += ", conditional "
        sql += "from ("
        sql += "select conditional, pivot, size, resize, repeat, trigger_price_to_close, f_gain, active_pivot, order_id, order_id_to_close, "
        sql += " previous_pivot, prev_tc, previous_pivot_distance, "
        ##### new
        #sql += "printf('%.5f', 100*ABS(previous_pivot_distance - " + str(fg_percentage) + ")/" + str(fg_percentage) + ") pivot_distance_deviation "
        sql += "printf('%." + str(adaperp_decimals) + "f', 100*ABS(previous_pivot_distance -  f_gain )/ f_gain ) pivot_distance_deviation "
        #new sql += pivot_distance_deviation
        sql += "from ("
        sql += "select trigger_price_to_put_in_position pivot, "
        sql += "conditional, "
        sql += "original_quantity size, "
        sql += "resize, "
        sql += "repeat, "
        sql += "trigger_price_to_close, "
        #sql += "printf('%.5f',100*((trigger_price_to_close/trigger_price_to_put_in_position)-1)) f_gain, "
        sql += "printf('%." + str(adaperp_decimals) + "f',100*(factor_gain-1)) f_gain, "
        sql += active_pivot_sql
        sql += "order_id, "
        sql += "order_id_to_close, "
        sql += "LAG ( trigger_price_to_put_in_position, 1, 'nada') OVER ( order by trigger_price_to_put_in_position ) previous_pivot, "
        sql += "LAG ( trigger_price_to_close, 1, 'nada') OVER ( order by trigger_price_to_close ) prev_tc, "
        sql += "printf('%." + str(adaperp_decimals) + "f', (( trigger_price_to_put_in_position/LAG( trigger_price_to_put_in_position, 1, 'nada') OVER ( order by trigger_price_to_put_in_position ) ) -1 )*100 ) previous_pivot_distance "
        sql += "from radar_list "
        sql += "where ( trigger_price_to_put_in_position >= " + str(low_price_pivot) + " and "
        sql += "trigger_price_to_put_in_position <= " + str(high_price_pivot) + ") " 
        sql += "and order_status in ('NEW', 'IN_POSITION') "
        sql += "order by trigger_price_to_put_in_position desc ) "
        sql += "order by pivot desc, previous_pivot desc"
        sql += ") order by pivot desc, previous_pivot desc"

        #print(sql)
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "query_min_pivot")
        #print("res_sql: ", res_sql)
        res_dict = [{'pivot':a[0], 'size':a[1],'resize':a[2],'repeat':a[3], 'tc':a[4], 
                     'f_gain':a[5], 'active_pivot':a[6], 'order_id':a[7], 'order_id_to_close':a[8],
                     'previous_pivot':a[9], 'previous_pivot_distance':a[10], 'prev_tc':a[11],
                     'pivot_distance_deviation':a[12], 'result':a[13], 'result_gap':a[14],
                     'conditional':a[15]} for a in res_sql] #convert list of tuples in list of dicts
        for item_dict in res_dict:
            if item_dict['conditional'] == "Y":
                item_dict['resize'] = "-" 
                item_dict['repeat'] = "-" 
                item_dict['f_gain'] = "-" 
                item_dict['previous_pivot'] = "-" 
                item_dict['result'] = "-" 
                item_dict['result_gap'] = "-" 
                item_dict['previous_pivot_distance'] = "-" 
                item_dict['pivot_distance_deviation'] = "-" 
        data = res_dict
        #print("data: " , data)
        return Response(data)

@api_view(['GET', 'POST'])
def pivot_frequency_all_view(request):
    if request.method == 'POST':
        data_dict = query_pivot_frequency_frontend(0) 
        return Response(data_dict)

@api_view(['GET', 'POST'])
def pivot_frequency_all_with_id_view(request):
    if request.method == 'POST':
        sql = "select order_id, order_status, order_id_to_close, trigger_price_to_put_in_position  "
        #sql += ",original_quantity, clientorderid, repeat, resize, factor_gain, group_id "
        sql += "from radar_list order by trigger_price_to_put_in_position limit 3" 
        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "query_min_pivot")
        #print("res_sql: ", res_sql)
        res_list_of_dicts = [{'order_id':a[0], 'order_status':a[1],'order_id_to_close':a[2],'tp':a[3]
                      } for a in res_sql] #convert list of tuples in list of dicts
        # Add an id to each dictionary
        for idx, item in enumerate(res_list_of_dicts, start=1):
            item["id"] = idx
        #print("res_list_of_dicts with id:", res_list_of_dicts)
         
        data_list_of_dicts = query_pivot_frequency_frontend(0) 
        # Add an id to each dictionary
        for idx, item in enumerate(data_list_of_dicts, start=1):
            item["id"] = idx
       
        to_return = res_list_of_dicts
        #to_return = data_list_of_dicts
        return Response(to_return)

@api_view(['GET', 'POST'])
def pivot_frequency_last7days_view(request):
    if request.method == 'POST':
        data_dict = query_pivot_frequency_frontend(7) 
        return Response(data_dict)

@api_view(['GET', 'POST'])
def zaraza_view(request):
    if request.method == 'POST':
        qdict = request.data
        #print("qdict: " + str(qdict))
        #qdict: {'id': 2, 'input': '2', 'option': 'DOWN', 'otherValues': 
        # {'order_id': 8563525399, 'order_status': 'IN_POSITION', 
        # 'order_id_to_close': 8569945135, 'tp': 0.2845, 'tc': 0.2848}} 
        data_to_modify = qdict['input']
        #print("data_to_modify:", data_to_modify)
        ori_data_dict = [{'count':'666'}] 
        data_dict = qdict['otherValues']
        #print("data_dict:", data_dict)
        data_dict['order_status'] = data_to_modify
        #data_dict = query_pivot_frequency_frontend(0) 
        #print("zaraza data_dict:", data_dict)
        #to_return = ori_data_dict
        to_return = [data_dict]
        return Response(to_return)

@api_view(['GET', 'POST'])
def pivot_frequency_last3days_view(request):
    if request.method == 'POST':
        data_dict = query_pivot_frequency_frontend(3) 
        return Response(data_dict)

@api_view(['GET', 'POST'])
def pivot_frequency_last24hs_view(request):
    if request.method == 'POST':
        data_dict = query_pivot_frequency_frontend(1) 
        return Response(data_dict)

@api_view(['GET', 'POST'])
def rp_graph_view(request):
    if request.method == 'GET':
        tablename = "TRACKER_PNL"
        # Query for the newest 1000 rows ordered by timestamp
        query_1 = "SELECT rp, datetime(timestamp_date,'unixepoch') FROM ( "
        query_1 += "SELECT rp, timestamp/1000 AS timestamp_date "
        query_1 += 'FROM ' + tablename + ' ORDER BY timestamp DESC LIMIT 100 ) subquery ORDER BY timestamp_date ASC;'

        # Query for the newest 10000 rows grouped by 10
        query_2 = 'SELECT AVG(rp), timestamp FROM (SELECT rp, timestamp, (ROW_NUMBER() OVER (ORDER BY timestamp DESC)-1) / 10 '
        query_2 += 'AS group_num FROM ' + tablename + '  ORDER BY timestamp DESC LIMIT 10000) GROUP BY group_num'
        
        #print(query_1)
        res_sql = exec_sql(sql = query_1, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "tracker_pnl")
        res_dict = [{'rp':a[0], 'timestamp_epoch':a[1]} for a in res_sql] #convert list of tuples in list of dicts
        data = res_dict
        #print(data)
        return Response(data)