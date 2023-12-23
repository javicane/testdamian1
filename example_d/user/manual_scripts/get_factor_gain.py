import json

def get_factor_gain():
    factor_gain_config_file = "/home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/config_scripts/factor_gain.json"
    with open(factor_gain_config_file) as conf:
        data_dict = json.load(conf)
    factor_gain = data_dict['factor_gain']
    print("factor_gain: " + str(factor_gain))
    print("factor_gain type: " + str(type(factor_gain)))
    return factor_gain


#factor_gain = get_factor_gain()
#print("factor_gain: " + str(factor_gain))
#print("factor_gain type: " + str(type(factor_gain)))