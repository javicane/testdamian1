import sqlite3
import json
import sys

#from binance_d.example_d.user.helpers_scripts.helpers_module import funcname

#db_file = "/home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/sierra.db"

#CREATE TABLE radar_list (order_id integer primary key,order_status text not null,order_id_to_close integer not null,trigger_price_to_put_in_position real not null,trigger_price_to_close real not null,original_quantity integer not null, clientorderid text not null);

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

        if sql_command == "insert":
            conn.commit()
            rows_inserted = cur.rowcount
            print("Record inserted successfully:", rows_inserted)
            result_to_return = rows_inserted 

        if sql_command == "delete":
            conn.commit()
            rows_deleted = cur.rowcount
            print("deleted rows: ", rows_deleted)
            result_to_return = rows_deleted

        if sql_command == "update":
            conn.commit()
            rows_updated = cur.rowcount
            print("updated rows: ", rows_updated)
            result_to_return = rows_updated

        if sql_command == "select" and fetch_type == "fetchone" and return_type == "return_raw":
            result = cur.fetchone()
            #print("select fetchone return_raw: " + str(result))
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