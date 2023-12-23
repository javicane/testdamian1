import json

def get_pivot_order_size():
    pivot_order_size_config_file = "/home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/config_scripts/pivot_order_size.json"
    with open(pivot_order_size_config_file) as conf:
        data_dict = json.load(conf)
    pivot_order_size = data_dict['pivot_order_size']
    print("pivot_order_size: " + str(pivot_order_size))
    print("pivot_order_size type: " + str(type(pivot_order_size)))
    return pivot_order_size


#pivot_order_size = get_pivot_order_size()
#print("pivot_order_size: " + str(pivot_order_size))
#print("pivot_order_size type: " + str(type(pivot_order_size)))