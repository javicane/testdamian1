import random
import sys
#market_price = 10
#tokens = 100
#decimals_quantity = 0
#buys = []
def generate_pivot_list(pivot_list):
    distance_percentage = 0.0625/2
    factor_gain = (distance_percentage / 100 ) + 1    
    print("factor_gain: ", factor_gain)
    #distance_percentage = 0.25
    initial_price = 0.36569
    pivots_number = 3 
    size = 1  
    create_multiple_pivots(pivot_list, distance_percentage, initial_price, pivots_number, size, factor_gain)
    print(pivot_list)
    return pivot_list

def create_multiple_pivots(pivot_list, distance_percentage, initial_price, pivots_number, size, factor_gain):
    distance = 1 - (distance_percentage/100)
    price = initial_price
    for counter_pivots in range(1, pivots_number + 1):
        price = round(price, 5)
        price = round(price * distance, 5)
        print("pivot number : " + str(counter_pivots) + ", price: " + str(price) + ", distance_percentage: " + str(distance_percentage) + ", size: " + str(size))
        my_dict = exec_transaction_pivot(price, size, factor_gain)
        pivot_list.append(my_dict)

def exec_transaction_pivot(p_price, p_size, factor_gain):
    print("in " + " args p_price, p_size, factor_gain: " + str(p_price) + ", " + str(p_size) + ", factor_gain: " + str(factor_gain))
    tp = p_price
    tc = get_trigger_price_to_close(p_price, factor_gain)
    size = p_size
    fg = factor_gain
    my_dict = dict(tp=tp, tc=tc, size=size)
    return my_dict
    



def get_trigger_price_to_close(price, factor_gain):
    trigger_price = round(float(factor_gain) * float(price), 5)
    print(".... trigger_price: " + str(trigger_price))
    return trigger_price


def procesar_pivot():
    pivot_list = []
    pivot_list = generate_pivot_list(pivot_list)
        #[{'tp': 0.36558, 'tc': 0.36569, 'size': 1}, {'tp': 0.36547, 'tc': 0.36558, 'size': 1}, {'tp': 0.36536, 'tc': 0.36547, 'size': 1}] order matters
    loan = 0
    position_size = 0
    sum_buy_price = 0
    contract_unit = 10
    market_price = 10
    tokens = 100
    balance_initial = market_price * ( tokens + position_size )
    market_price_initial = market_price
    print("balance_initial:", balance_initial)
    print("market_price_initial:", market_price_initial)
    counter = 0
    market_price_old = 0.4
    acum_10000 = 0
    acum_9000 = 0
    acum_8000 = 0
    acum_7000 = 0
    acum_6000 = 0
    acum_5000 = 0
    acum_4000 = 0
    acum_3000 = 0
    acum_2000 = 0
    acum_1000 = 0
    my_list = ["A", "B", "C", "D"]
    #print(random.choices(my_list, cum_weights=(0.1, 0.2, 0.3, 0.4), k=9))
    #print(random.choices(my_list, cum_weights=(0.5, 0.6, 0.7, 1), k=9))
    decimals_quantity = 5
    my_list = [10, 9, round(random.uniform(1,10000)/10000, decimals_quantity)]
    trades_per_year  = 365*24*60*60  # 1 trade per second
    w_sum = 2**10
    print("w_sum:", w_sum)
    #print(random.choices(my_list, weights=(1/trades_per_year, 2/trades_per_year, (trades_per_year-w_sum)/trades_per_year), k=30))
    rule_number_10 = 3 # quantity of variators of 10%
    rule_number_5 = 4 # quantity of variators of 5%
    rule_number_1 = 10 # quantity of variators of 1%
    rule_number_less_1 = 20 # quantity of variators of less than 1%
    rule_max_consecutive_number_10 = 2
    rule_max_consecutive_number_5 = 3
    total_variators = 27
    variators_list = []
    # process rule_number_10
    for i in range(0, rule_number_10):
        variators_list.append(10)
    print(variators_list)
    for i in range(0, rule_number_5):
        variators_list.append(5)
    print(variators_list)
    random.shuffle(variators_list) 
    print(variators_list)
    for variator_value in variators_list:
        #
    '''
    1 trade per second
    trades per year = 365*24*60*60 = 31536000 = T
    1 10% per year
    2 9%
    4 8%
    8 7%
    16 %6
    32 %5
    64 %4
    128 3
    256 2
    512 1
    1024 0.5
    resto = T-(1+2+4+8+16+32+64+128+256+512+1024)/T
    '''
    '''
    for i in range(1, 1):
        decimals_quantity = 5
        #market_price = round(random.uniform(5,10), decimals_quantity)
        #r = round(random.uniform(1.00001, 1.1), decimals_quantity)
        r = round(random.uniform(10000, 1), decimals_quantity)
        if r >= 9000:
            acum_10000 += 1    
        elif r >= 8000 and r < 9000:
            acum_9000 += 1
        elif r >= 7000 and r < 8000:
            acum_8000 += 1
        elif r >= 6000 and r < 7000:
            acum_7000 += 1
        elif r >= 5000 and r < 6000:
            acum_6000 += 1
        elif r >= 4000 and r < 5000:
            acum_5000 += 1
        elif r >= 3000 and r < 4000:
            acum_4000 += 1
        elif r >= 2000 and r < 3000:
            acum_3000 += 1
        elif r >= 1000 and r < 2000:
            acum_2000 += 1
        elif r < 1000:
            acum_1000 += 1
    #    print("r:", r)
    print("acum_10000", acum_10000)
    print("acum_9000", acum_9000)
    print("acum_8000", acum_8000)
    print("acum_7000", acum_7000)
    print("acum_6000", acum_6000)
    print("acum_5000", acum_5000)
    print("acum_4000", acum_4000)
    print("acum_3000", acum_3000)
    print("acum_2000", acum_2000)
    print("acum_1000", acum_1000)
    '''
        #market_price = round(r*market_price_old, decimals_quantity)
        #market_price_old = market_price
        #print("market_price:", market_price)
    '''
    for buy_dict in buys:
        print("buy_dict:", buy_dict)
        print(buy_dict['tokens'])
    
        print("market_price:", market_price) 
        market_price = buy_dict['market_price']
        counter += 1
        diff_market_price = market_price - market_price_initial
        print("diff_market_price:", diff_market_price)
        market_price_old = market_price
        position_size = position_size + buy_dict['tokens']
        sum_buy_price = sum_buy_price + buy_dict['market_price']
        tokens = tokens - buy_dict['tokens']
        contract_buy_value = contract_unit/buy_dict['market_price'] 
        print("tokens+position_size:", tokens + position_size)
        capital = buy_dict['market_price'] * tokens
        position_value = buy_dict['market_price'] * position_size
        print("position_value:", position_value)
        print("capital:", capital)
        print("position_size:", position_size)
        balance = buy_dict['market_price'] * ( tokens + position_size)
        print("balance:", balance)
        pnl = position_value + capital - balance_initial
        print("pnl:", pnl)
        
        print("....")
    print("counter:", counter)
    print("position_size:", position_size)
    print("sum_buy_price:", sum_buy_price)
    print("avg_buy_price:", sum_buy_price/position_size)
    print("balance:", (market_price * ( tokens + position_size)))
    '''
    #round(random.uniform(5,10), decimals_quantity)
    #    market_price = (round(random.uniform(5,10), decimals_quantity))
    
def main():
    pivot_list = procesar_pivot()
    print("pivot_list:", pivot_list)
    
main()