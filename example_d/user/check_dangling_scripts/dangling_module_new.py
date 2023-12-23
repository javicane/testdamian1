from difflib import SequenceMatcher

def naver():
    open_orders_list = [{'clientOrderId': 'goto_in_position1653456812156', 'orderId': '6517336318', 'side': 'SELL', 'status': 'NEW'}  
    ] 
    list_radar = [ 4, 1, 2, 3 ] #  order_id_to_close != 0 and order_status = 'IN_POSITION'" 
    list_current = [ 4, 2, 1, 5, 8] # all open_orders where side == "SELL" and status == "NEW": 
    list_radar_sorted = sorted(list_radar)
    list_current_sorted = sorted(list_current)
    print(list_radar_sorted)
    print(list_current_sorted)

    if list_radar_sorted == list_current_sorted:
        print("ok iguales")
    else:
        x_list_radar = [ i for i in set(list_radar) if i not in list_current ]
        x_list_current = [ i for i in set(list_current) if i not in  list_radar ]
        
        print("sobrantes en list_radar:" + str(x_list_radar))
        print("sobrantes en list_current:" + str(x_list_current))
        print("...analizando sobrantes en radar_list")
    for tag, i, j, k, l in SequenceMatcher(None, list_radar_sorted, list_current_sorted).get_opcodes():
        print(tag, i , j, k , l)
        print("...............")
naver()