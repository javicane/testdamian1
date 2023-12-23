import smtplib
import time
import datetime
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from binance_d.impl.utils.timeservice import get_current_timestamp
from binance_d.example_d.user.helpers_scripts.sql import exec_sql

# Gmail account credentials
gmail_user = 'sierramatic@gmail.com'
gmail_password = 'ybbffoywplpodtyd'
# Recipient email address
to = 'sierramatic@gmail.com'

def check_now_view():
    timestamp_epoch = get_current_timestamp()
    old_time = datetime.datetime.now()
    new_time = old_time - datetime.timedelta(hours=3)
    date_time = new_time.strftime("%d/%m/%Y, %H:%M:%S")
    current_time_string = date_time
    data_dict = dict(id=35)
    #sql = "select min(trigger_price_to_close) from radar_list where order_status = 'IN_POSITION';"
    #nearest_pnl = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error sql nearest_pnl")[0]
        
    sql = "select max(trigger_price_to_put_in_position) from radar_list where order_status ='NEW'"
    nearest_price_to_put_in_position = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error sql nearest price")[0]

    #sql = "select trigger_price_to_put_in_position from radar_list where trigger_price_to_close in "
    #sql += "(select min(trigger_price_to_close) from radar_list where order_status = 'IN_POSITION');"
    #active_pivot = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error sql active_pivot")[0]
        
    sql = "select trigger_price_to_put_in_position, original_quantity, resize, trigger_price_to_close from radar_list where "
    sql += "order_status = 'IN_POSITION' and "
    sql += "trigger_price_to_close in "
    sql += "(select min(trigger_price_to_close) from radar_list where order_status = 'IN_POSITION');"
    res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "error sql ")
    if not res_sql:
        #print("res_sql empty:", res_sql)
        active_pivot = 666
        nearest_pnl = 666
        size = 666
        resize = 666
    else:
        active_pivot = res_sql[0]
        nearest_pnl = res_sql[3]
        size = res_sql[1]
        resize = res_sql[2]

    sql = "select round(entry_price,5) from tracker_entry_price;"
    res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchone", error_message = "query tracker_entry_price")
    entry_price = res_sql[0]
    #pivots to entry
    sql = "select count(*) from radar_list where "
    sql += "trigger_price_to_close <= (select min(trigger_price_to_close) from radar_list "
    sql += "where trigger_price_to_close >= " + str(entry_price) + ") and "
    sql += "trigger_price_to_close >= " + str(nearest_pnl)
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

    with open("/tmp/supervisord_websocket_user.out.log", "rb") as file:
        try:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
        except OSError:
            file.seek(0)
        last_line_websocket = file.readline().decode()[:-1]
        #print(last_line + "---")
    #print(last_line_websocket + "---")

    #data = [OrderedDict([('id', 35), ('date_now', current_time_string), ('timestamp_epoch', timestamp_epoch), 
    #                     ('nearest_pnl', nearest_pnl),
    #                     ('nearest_price_to_put_in_position', nearest_price_to_put_in_position)])]
    try: 
        tc = nearest_pnl
        tp = nearest_price_to_put_in_position
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
    data = [{'date_now': current_time_string, 'timestamp_epoch': timestamp_epoch, 
            'to_goal': to_goal,
            'pivots_to_entry': pivots_to_entry,
            'size': size,
            'resize': resize,
            'nearest_pnl': nearest_pnl,
            'nearest_price_to_put_in_position': nearest_price_to_put_in_position,
            'active_pivot': active_pivot,
            'last_line_websocket': last_line_websocket,
            'pivot_count_in_position': pivot_count_in_position,
            'pivot_count_total': pivot_count_total}]

    return data

def send_mail_now():
# Recipient email address
    to = 'damianbogan@gmail.com'
# Create message container
    msg = MIMEMultipart()

# Set message attributes
    msg['From'] = gmail_user
    msg['To'] = to
    current_timestamp = int(time.time())
    #msg['Subject'] = 'sierra status' + str(current_timestamp)
    msg['Subject'] = 'sierra control - status' 
    print("ct", current_timestamp)
# Add message body
    content = check_now_view()
    body = 'This is from sierra , mail ' + str(current_timestamp) + ", "
    body += '\n' + str(check_now_view())
    time.sleep(1)
    body += '\n' + str(check_now_view())
    time.sleep(1)
    body += '\n' + str(check_now_view())
    time.sleep(1)
    body += '\n' + str(check_now_view())
    msg.attach(MIMEText(body, 'plain'))

# Create SMTP session and send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        text = msg.as_string()
        server.sendmail(gmail_user, to, text)
        print('Email sent successfully')
    except Exception as e:
        print('Something went wrong:', e)
    finally:
        server.quit()
    return True

def infinite_loop():
    while True:
    # Create message container
        msg = MIMEMultipart()
    
    # Set message attributes
        msg['From'] = gmail_user
        msg['To'] = to
        current_timestamp = int(time.time())
        #msg['Subject'] = 'sierra status' + str(current_timestamp)
        msg['Subject'] = 'sierra control' 
        print("ct", current_timestamp)
    # Add message body
        content = check_now_view()
        body = 'This is from sierra , mail ' + str(current_timestamp) + ", "
        body += '\n' + str(check_now_view())
        time.sleep(5)
        body += '\n' + str(check_now_view())
        time.sleep(5)
        body += '\n' + str(check_now_view())
        time.sleep(5)
        body += '\n' + str(check_now_view())
        msg.attach(MIMEText(body, 'plain'))
    
    # Create SMTP session and send email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_user, gmail_password)
            text = msg.as_string()
            server.sendmail(gmail_user, to, text)
            print('Email sent successfully')
        except Exception as e:
            print('Something went wrong:', e)
        finally:
            server.quit()
        time.sleep(10)    

if __name__ == "__main__":
    infinite_loop()