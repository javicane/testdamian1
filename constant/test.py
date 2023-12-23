import os
'''
if(os.path.exists("binance_d/privateconfig.py")):
    from binance_d.privateconfig import *
    g_api_key = p_api_key
    g_secret_key = p_secret_key
else:
    g_api_key = ""
    g_secret_key = ""
    g_api_key = "ooKQU3PHpavaKi"
    g_secret_key = "AEyyfIC422gu1B5DW"
    print("in binance_d.constant.test.py (g_api_key, g_secret_key): " + str(g_api_key) + ", " + str(g_secret_key))
'''
#input("in constant.test, pec")
from binance_d.privateconfig import p_api_key, p_secret_key 

g_api_key = p_api_key
g_secret_key = p_secret_key

g_account_id = 12345678