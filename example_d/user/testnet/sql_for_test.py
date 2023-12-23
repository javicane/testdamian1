import sqlite3
import json
import sys

#from binance_d.example_d.user.helpers_scripts.helpers_module import funcname

#db_file = "/home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/sierra.db"


def create_db_conn():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    db_file = "/home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/sierra.db"
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn    

def exec_sql(sql = None , sql_command = None, return_type = None, fetch_type = None, error_message = None):
    '''
    params:
        sql: string, sql query to execute
        sql_command: string, options: select, insert, update, delete, ddl
        return_type: string, only applies if operation is "select", options: return_raw(returns query result as is), return_dict(returns query result as dict)
        fetch_type: string, only applies if operation is "select"
    
    returns:
        if sql_command is "insert" returns the number of rows inserted
        if sql_command is "select" please see the explanation in the params sections above

    '''
    result_to_return = ""
    conn = create_db_conn()
    try:
        # this try except block is necessary because the connection is alive in case of exception in a query and the
        # tables involved gets locked

        cur = conn.cursor()
        cur.execute(sql)
 
        result_to_return = None

        if sql_command == "update":
            #count = cur.execute(sql)
            conn.commit()
            rows_updated = cur.rowcount
            print("updated rows: ", rows_updated)
            result_to_return = rows_updated

        if sql_command == "insert":
            conn.commit()
            rows_inserted = cur.rowcount
            print("Record inserted successfully:", rows_inserted)
            result_to_return = rows_inserted 

        if sql_command == "select" and fetch_type == "fetchone" and return_type == "return_raw":
            result = cur.fetchone()
            print("select fetchone return_raw: " + str(result))
            #returns a list of tuples 
            result_to_return = result

        #if sql_command == "select" and fetch_type == "fetchone" and return_type == "return_dict":
        #    result = cur.fetchone()
        #    result_to_return = json.loads(result) 

        if sql_command == "select" and fetch_type == "fetchall" and return_type == "return_dict":
            result = cur.fetchall()
            result_to_return = json.loads(result[0])

        if sql_command == "select" and fetch_type == "fetchall" and return_type == "return_raw":
            result = cur.fetchall()
            # returns list of tuples
            result_to_return = result

        if sql_command == "ddl":
            conn.commit()
            print("ddl executed")
            result_to_return = "ddl executed"
    
    except:
        err = "except in exec_sql, error_message: " + str(error_message) + ", sql: " + str(sql) + ", sys.exc_info(): " + str(sys.exc_info())
        conn.close()
        print(err)
        raise

    finally:
       conn.close()
       return result_to_return

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def test():
    sql = "DROP TABLE r_list;"
    exec_sql(sql = sql , sql_command = "ddl", error_message = "error in drop")
    
    sql = "CREATE TABLE if not exists r_list ("
    #sql = "CREATE TABLE r_list ("
    sql += "order_id integer primary key,"
    sql += "order_status text not null,"
    sql += "order_id_to_close integer not null,"
    sql += "trigger_price_to_put_in_position real not null,"
    sql += "trigger_price_to_close real not null,"
    sql += "original_quantity integer not null);"
    result = exec_sql(sql = sql, sql_command = "ddl", error_message = "create table r_list")
    print("result ddl is: " + str(result))
    
    sql = "insert into r_list ( order_id, order_status, order_id_to_close, trigger_price_to_put_in_position,"
    sql += "trigger_price_to_close, original_quantity) values (123456, 'NEW', 0, 1, 1.22222, 1)"
    result = exec_sql(sql = sql , sql_command = "insert", error_message = "insert dummy values")
    print("result insert is: " + str(result))
    
    sql = "insert into r_list ( order_id, order_status, order_id_to_close, trigger_price_to_put_in_position,"
    sql += "trigger_price_to_close, original_quantity) values (1234567, 'NEW', 0, 1, 1.23456, 1)"
    result = exec_sql(sql = sql , sql_command = "insert", error_message = "insert dummy values")
    print("result insert is: " + str(result))


    sql = "select * from r_list"
    result = exec_sql(sql = sql , sql_command = "select", fetch_type = "fetchall", return_type = "return_raw", error_message = "error in select * fetchall return_raw")
    print("result select fetchall return_raw is: " + str(result))
    
    sql ="update r_list set order_status ='IN_POSITION', order_id_to_close = 666 where order_id ='123456' and order_status='NEW'"
    result = exec_sql(sql = sql , sql_command = "update", error_message = "update error message")
    print("result update is: " + str(result))
    
    print("")
    
    sql ="update r_list set order_status ='IN_POSITION', order_id_to_close = 667 where order_id ='1234567' and order_status='NEW'"
    result = exec_sql(sql = sql , sql_command = "update", error_message = "update error message")
    print("result update is: " + str(result))
    
    print("")

    sql = "select * from r_list"
    result = exec_sql(sql = sql , sql_command = "select", fetch_type = "fetchone", return_type = "return_raw", error_message = "error in select * fetchone return_raw")
    print("result select fetchone return_raw is: " + str(result))

    print("")

    sql = "select * from r_list"
    result = exec_sql(sql = sql , sql_command = "select", fetch_type = "fetchall", return_type = "return_raw", error_message = "error in select * fetchone return_raw")
    print("result select fetchall return_raw is: " + str(result))

    print("")

    sql = "select order_id_to_close from r_list where order_id_to_close != 0 and order_status = 'IN_POSITION'"
    result = exec_sql(sql = sql , sql_command = "select", fetch_type = "fetchall", return_type = "return_raw", error_message = "error in select * fetchone return_raw")
    print("result select order_id_to_close return_raw is: " + str(result))

    if 1 == 1.0:
        print("1 = 1.0")

    order_id = 123456 
    order_status = "NEW"
    order_id_to_close = 666
    trigger_price_to_put_in_position = 1 
    trigger_price_to_close = 1.01
    original_quantity = 1 
    tuple1 = (order_id, order_status, order_id_to_close, trigger_price_to_put_in_position, trigger_price_to_close, original_quantity)
    sql = "insert into r_list ( order_id, order_status, order_id_to_close, trigger_price_to_put_in_position,"
    sql += "trigger_price_to_close, original_quantity) values " 
    sql += str(tuple1)
    #print("sql :  " + str(sql))
    #exec_sql(sql = sql, sql_command =)
    a = [1,2,3]
    b = [3,2,1,]
    if sorted(a) == sorted(b):
        print("iguales")
    else:
        print("no son iguales")


    # check if key:value exists in list of dicts:
    radar_list = [ {'order_id': 11, 'order_status': 'NEW'}, {'order_id': 12, 'order_status': 'NEW'}]
    print("radar_list:" + str(radar_list))
    if ('order_id', 11 ) in radar_list.items():
        print("OK exists 11")
    if ('order_id', 13 ) not in radar_list.items():
        print("OK not exists 13")

def get_dict():
    #https://docs.python.org/2/library/sqlite3.html
    conn = create_db_conn()
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("select * from r_list")
    print("")
    print("in get_dict")
    #print(cur.fetchone()["order_id"])
    print(cur.fetchone())
    cur.execute("select * from r_list")
    #print(cur.fetchall())
    result = cur.fetchall()
    print("str result is type: " + str(type(result)))
    print("result: " + str(result))
test()

#get_dict()