import unittest

from unittest.mock import patch, MagicMock
from binance_d.example_d.user.process_module import process_event, process_pnl, process_goto_in_position 


class TestProcessModule(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.nada = 1


    @classmethod
    def tearDownClass(self):
        self.nada = 1

#nombre reales de eventos:
#    "x":"NEW",                  // Execution Type
#    "X":"NEW",                  // Order Status
#    "x":"NEW","X":"NEW","
#    "x":"TRADE","X":"FILLED"

#sqlite> select * from test_radar_list;
#1|IN_POSITION|6311530344|0.89|0.893|97
#2|IN_POSITION|6386198761|0.61|0.6262|3
#sqlite> .schema radar_list
#CREATE TABLE radar_list (order_id integer primary key,order_status text not null,order_id_to_close integer not null,trigger_price_to_put_in_position real not null,trigger_price_to_close real not null,original_quantity integer not null);
#sqlite> 
    @patch('binance_d.example_d.user.process_module.get_radar_list')
    @patch('binance_d.example_d.user.process_module.process_pnl')
    @patch('binance_d.example_d.user.process_module.process_goto_in_position')
    def test_new_new_but_exists_in_radar_list(self, mock_process_goto_in_position, mock_process_pnl, mock_get_radar_list):
        my_dict = dict(order_id=1,order_status='IN_POSITION',order_id_to_close=6311530344,trigger_price_to_put_in_position=0.89,
                       trigger_price_to_close=0.893, original_quantity=97)
        my_list = []
        my_list.append(my_dict)
        mock_get_radar_list.return_value = my_list

        event_dict = { 
                      'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'NEW', 
                      'orderId': '1', 'orderStatus': 'NEW', 
                      'origQty': '1.0', 'price': '0.1', 'realizedprofit': '0.0', 'clientOrderId': 'dummy'
                      }
        #rc = process_event(event_dict)              
        #self.assertIn("ERROR DETECTED NEW NEW existing in radar_list", rc) # OK 

    @patch('binance_d.example_d.user.process_module.get_radar_list')
    @patch('binance_d.example_d.user.process_module.process_pnl')
    @patch('binance_d.example_d.user.process_module.process_goto_in_position')
    def test_initial_pivot(self, mock_process_goto_in_position, mock_process_pnl, mock_get_radar_list):
        my_dict = dict(order_id=1,order_status='IN_POSITION',order_id_to_close=6311530344,trigger_price_to_put_in_position=0.89,
                       trigger_price_to_close=0.893, original_quantity=97)
        my_list = []
        my_list.append(my_dict)
        mock_get_radar_list.return_value = my_list

        event_dict = { 
                      'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'NEW', 
                      'orderId': '222', 'orderStatus': 'NEW', 
                      'origQty': '1.0', 'price': '0.1', 'realizedprofit': '0.0', 'clientOrderId': 'dummy'
                      }
        #rc = process_event(event_dict)              
        #self.assertIn("DETECTED initial pivot or something to analize", rc) # OK

    @patch('binance_d.example_d.user.process_module.get_radar_list')
    @patch('binance_d.example_d.user.process_module.process_pnl')
    @patch('binance_d.example_d.user.process_module.process_goto_in_position')
    def test_fake(self, mock_process_goto_in_position, mock_process_pnl, mock_get_radar_list):

        my_dict = dict(order_id=1,order_status='IN_POSITION',order_id_to_close=6311530344,trigger_price_to_put_in_position=0.89,
                       trigger_price_to_close=0.893, original_quantity=97)
        my_list = []
        my_list.append(my_dict)
        mock_get_radar_list.return_value = my_list

        event_dict = { 
                      'clientOrderId': 'damian',  
                      'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'NEW', 
                      'orderId': '1', 'orderStatus': 'NEW', 
                      'origQty': '1.0', 'price': '0.1', 'realizedprofit': '0.0'
                      }
        #rc = process_event(event_dict)              
        #self.assertIn("DETECTED FAKE ORDER", rc)   # OK 

    @patch('binance_d.example_d.user.process_module.get_radar_list')
    @patch('binance_d.example_d.user.process_module.process_pnl')
    @patch('binance_d.example_d.user.process_module.process_goto_in_position')
    def test_trade_filled_rp_non_zero_exists_in_radar_list_IN_POSITION_and_order_id_to_close_match_event_order_id(self, mock_process_goto_in_position, mock_process_pnl, mock_get_radar_list):
        mock_process_pnl.return_value = "PNL"
        my_dict = dict(order_id=1,order_status='IN_POSITION',order_id_to_close=6311530344,trigger_price_to_put_in_position=0.89,
                       trigger_price_to_close=0.893, original_quantity=97)
        my_list = []
        my_list.append(my_dict)
        mock_get_radar_list.return_value = my_list
                             
        event_dict = { 
                      'clientOrderId': 'dummy',
                      'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'TRADE', 
                      'orderId': '6311530344', 'orderStatus': 'FILLED', 
                      'origQty': '1.0', 'price': '0.1', 'realizedprofit': '1.0'
                      }
        #rc = process_event(event_dict)              
        #self.assertIn("PNL", rc)   #OK


    @patch('binance_d.example_d.user.process_module.get_radar_list')
    @patch('binance_d.example_d.user.process_module.process_pnl')
    @patch('binance_d.example_d.user.process_module.process_goto_in_position')
    def test_trade_filled_rp_non_zero_exists_in_radar_list_IN_POSITION_and_order_id_to_close_not_match_event_order_id(self, mock_process_goto_in_position, mock_process_pnl, mock_get_radar_list):
        mock_process_pnl.return_value = "PNL"
        my_dict = dict(order_id=1,order_status='IN_POSITION',order_id_to_close=6311530344,trigger_price_to_put_in_position=0.89,
                       trigger_price_to_close=0.893, original_quantity=97)
        my_list = []
        my_list.append(my_dict)
        mock_get_radar_list.return_value = my_list
                             
        event_dict = { 
                      'clientOrderId': 'dummy',
                      'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'TRADE', 
                      'orderId': '1', 'orderStatus': 'FILLED', 
                      'origQty': '1.0', 'price': '0.1', 'realizedprofit': '1.0'
                      }
        #rc = process_event(event_dict)              
        #self.assertIn("ERROR, radar_list [order_id_to_close] not match event_order_id", rc)   #OK

    @patch('binance_d.example_d.user.process_module.get_radar_list')
    @patch('binance_d.example_d.user.process_module.process_pnl')
    @patch('binance_d.example_d.user.process_module.process_goto_in_position')
    def test_trade_filled_rp_non_zero_exists_not_exists_in_radar_list(self, mock_process_goto_in_position, mock_process_pnl, mock_get_radar_list):
        mock_process_pnl.return_value = "PNL"
        my_dict = dict(order_id=1,order_status='IN_POSITION',order_id_to_close=6311530344,trigger_price_to_put_in_position=0.89,
                       trigger_price_to_close=0.893, original_quantity=97)
        my_list = []
        my_list.append(my_dict)
        mock_get_radar_list.return_value = my_list
                             
        event_dict = { 
                      'clientOrderId': 'dummy',
                      'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'TRADE', 
                      'orderId': '222', 'orderStatus': 'FILLED', 
                      'origQty': '1.0', 'price': '0.1', 'realizedprofit': '1.0'
                      }
        #rc = process_event(event_dict)              
        #self.assertIn("ERROR , event_order_id not exists in radar_list", rc)   #OK

    @patch('binance_d.example_d.user.process_module.get_radar_list')
    @patch('binance_d.example_d.user.process_module.process_pnl')
    @patch('binance_d.example_d.user.process_module.process_goto_in_position')
    def test_trade_filled_rp_non_zero_exists_in_radar_list_not_IN_POSITION_and_order_id_to_close_match_event_order_id(self, mock_process_goto_in_position, mock_process_pnl, mock_get_radar_list):
        mock_process_pnl.return_value = "PNL"
        my_dict = dict(order_id=1,order_status='NEW',order_id_to_close=6311530344,trigger_price_to_put_in_position=0.89,
                       trigger_price_to_close=0.893, original_quantity=97)
        my_list = []
        my_list.append(my_dict)
        mock_get_radar_list.return_value = my_list
                             
        event_dict = { 
                      'clientOrderId': 'dummy',
                      'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'TRADE', 
                      'orderId': '6311530344', 'orderStatus': 'FILLED', 
                      'origQty': '1.0', 'price': '0.1', 'realizedprofit': '1.0'
                      }
        #rc = process_event(event_dict)              
        #self.assertIn("ERROR, order_status must be IN_POSITION", rc)   #OK

#################
# tests for rp == 0

    @patch('binance_d.example_d.user.process_module.get_radar_list')
    @patch('binance_d.example_d.user.process_module.process_pnl')
    @patch('binance_d.example_d.user.process_module.process_goto_in_position')
    def test_trade_filled_rp_zero_exists_in_radar_list_NEW(self, mock_process_goto_in_position, mock_process_pnl, mock_get_radar_list):

        mock_process_pnl.return_value = "PNL"
        mock_process_goto_in_position.return_value = "GOTO_IN_POSITION"
        my_dict = dict(order_id=1,order_status='NEW',order_id_to_close=0,trigger_price_to_put_in_position=0.89,
                       trigger_price_to_close=0.893, original_quantity=97)
        my_list = []
        my_list.append(my_dict)
        mock_get_radar_list.return_value = my_list
                             
        event_dict = { 
                      'clientOrderId': 'dummy',
                      'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'TRADE', 
                      'orderId': '1', 'orderStatus': 'FILLED', 
                      'origQty': '1.0', 'price': '0.1', 'realizedprofit': '0.0'
                      }
        #rc = process_event(event_dict)              
        #self.assertEqual("GOTO_IN_POSITION", rc)   #OK

    @patch('binance_d.example_d.user.process_module.get_radar_list')
    @patch('binance_d.example_d.user.process_module.process_pnl')
    @patch('binance_d.example_d.user.process_module.process_goto_in_position')
    def test_trade_filled_rp_zero_exists_in_radar_list_not_NEW(self, mock_process_goto_in_position, mock_process_pnl, mock_get_radar_list):

        mock_process_pnl.return_value = "PNL"
        mock_process_goto_in_position.return_value = "GOTO_IN_POSITION"
        my_dict = dict(order_id=1,order_status='KK',order_id_to_close=0,trigger_price_to_put_in_position=0.89,
                       trigger_price_to_close=0.893, original_quantity=97)
        my_list = []
        my_list.append(my_dict)
        mock_get_radar_list.return_value = my_list
                             
        event_dict = { 
                      'clientOrderId': 'dummy',
                      'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'TRADE', 
                      'orderId': '1', 'orderStatus': 'FILLED', 
                      'origQty': '1.0', 'price': '0.1', 'realizedprofit': '0.0'
                      }
        #rc = process_event(event_dict)              
        #self.assertEqual("ERROR, order_status must be NEW", rc)   #OK

    @patch('binance_d.example_d.user.process_module.get_radar_list')
    @patch('binance_d.example_d.user.process_module.process_pnl')
    @patch('binance_d.example_d.user.process_module.process_goto_in_position')
    def test_trade_filled_rp_zero_not_exists_in_radar_list(self, mock_process_goto_in_position, mock_process_pnl, mock_get_radar_list):

        mock_process_pnl.return_value = "PNL"
        mock_process_goto_in_position.return_value = "GOTO_IN_POSITION"
        my_dict = dict(order_id=1,order_status='KK',order_id_to_close=0,trigger_price_to_put_in_position=0.89,
                       trigger_price_to_close=0.893, original_quantity=97)
        my_list = []
        my_list.append(my_dict)
        mock_get_radar_list.return_value = my_list
                             
        event_dict = { 
                      'clientOrderId': 'dummy',
                      'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'TRADE', 
                      'orderId': '222', 'orderStatus': 'FILLED', 
                      'origQty': '1.0', 'price': '0.1', 'realizedprofit': '0.0'
                      }
        #rc = process_event(event_dict)              
        #self.assertEqual("ERROR , event_order_id not exists in radar_list", rc)   #OK

    @patch('binance_d.example_d.user.process_module.get_radar_list')
    def test_new_new_order_id_to_close_exists_in_radar_list_IN_POSITION(self, mock_get_radar_list):

        my_dict = dict(order_id=1,order_status='IN_POSITION',order_id_to_close=333,trigger_price_to_put_in_position=0.89,
                       trigger_price_to_close=0.893, original_quantity=97)
        my_list = []
        my_list.append(my_dict)
        mock_get_radar_list.return_value = my_list
                             
        event_dict = { 
                      'clientOrderId': 'dummy',
                      'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'NEW', 
                      'orderId': '333', 'orderStatus': 'NEW', 
                      'origQty': '1.0', 'price': '0.1', 'realizedprofit': '0.0'
                      }
        rc = process_event(event_dict)              
        self.assertEqual("DETECTED new new in_position order_id_to_close , this is the creation of a new order_id_to_close", rc)

    @patch('binance_d.example_d.user.process_module.get_radar_list')
    def test_new_new_order_id_to_close_exists_in_radar_list_not_IN_POSITION(self, mock_get_radar_list):

        my_dict = dict(order_id=1,order_status='NEW',order_id_to_close=333,trigger_price_to_put_in_position=0.89,
                       trigger_price_to_close=0.893, original_quantity=97)
        my_list = []
        my_list.append(my_dict)
        mock_get_radar_list.return_value = my_list
                             
        event_dict = { 
                      'clientOrderId': 'dummy',
                      'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'NEW', 
                      'orderId': '333', 'orderStatus': 'NEW', 
                      'origQty': '1.0', 'price': '0.1', 'realizedprofit': '0.0'
                      }
        #rc = process_event(event_dict)              
        #self.assertEqual("ERROR, order_status new new order_id_to_close_exists not IN_POSITION", rc)

    @patch('binance_d.example_d.user.process_module.get_radar_list')
    def test_new_new_order_id_to_close_not_exists_in_radar_list(self, mock_get_radar_list):

        my_dict = dict(order_id=1,order_status='NEW',order_id_to_close=333,trigger_price_to_put_in_position=0.89,
                       trigger_price_to_close=0.893, original_quantity=97)
        my_list = []
        my_list.append(my_dict)
        mock_get_radar_list.return_value = my_list
                             
        event_dict = { 
                      'clientOrderId': 'dummy',
                      'eventType': 'ORDER_TRADE_UPDATE', 'executionType': 'NEW', 
                      'orderId': '222', 'orderStatus': 'NEW', 
                      'origQty': '1.0', 'price': '0.1', 'realizedprofit': '0.0'
                      }
        #rc = process_event(event_dict)              
        #self.assertEqual("ERROR, radar_list [order_id_to_close] not match event_order_id", rc)
    #### 
    # test process_pnl

    @patch('binance_d.example_d.user.process_module.exec_transaction_pivot')
    def test_process_pnl_ok(self, mock_exec_transaction_pivot):
        #previamente hice esto en la tabla real: insert into radar_list ( order_id, order_status, order_id_to_close, trigger_price_to_put_in_position,trigger_price_to_close, original_quantity) 
        # values (3, "IN_POSITION", 333,0.61, 0.6262,3);
        mock_exec_transaction_pivot.return_value = "OK"
        radar_list_dict = dict(order_id=3,order_status='IN_POSITION',order_id_to_close=333,trigger_price_to_put_in_position=0.61,
                               trigger_price_to_close=0.6262, original_quantity=3)
        event_order_id = '3' 

        #rc = process_pnl(event_order_id, radar_list_dict)              
        #self.assertEqual("OK, pivot recreated", rc)   #OK
        #mock_exec_transaction_pivot.assert_called_once()

    @patch('binance_d.example_d.user.process_module.exec_transaction_pivot')
    def test_process_pnl_error(self, mock_exec_transaction_pivot):
        #previamente hice esto en la tabla real: insert into radar_list ( order_id, order_status, order_id_to_close, trigger_price_to_put_in_position,trigger_price_to_close, original_quantity) 
        # values (3, "IN_POSITION", 333,0.61, 0.6262,3);
        mock_exec_transaction_pivot.return_value = "OK"
        radar_list_dict = dict(order_id=3,order_status='IN_POSITION',order_id_to_close=333,trigger_price_to_put_in_position=0.61,
                               trigger_price_to_close=0.6262, original_quantity=3)
        event_order_id = '4' 

        #rc = process_pnl(event_order_id, radar_list_dict)              
        #self.assertEqual("ERROR in process_pnl exec_sql", rc)   #OK

####
#test process_goto_in_position
    #output = silent_limit_no_oco_sell_long(p_price, p_size)
    #output_dict =  create_dict_from_output(output)
    #@patch('binance_d.example_d.user.process_module.create_dict_from_output')
    #@patch('binance_d.example_d.user.process_module.silent_limit_no_oco_sell_long')
    #def test_process_goto_in_position_ok(self, mock_silent_limit_no_oco_sell_long, mock_create_dict_from_output):
    def test_process_goto_in_position_ok(self):
        #previamente hice esto en la tabla real: insert into radar_list ( order_id, order_status, order_id_to_close,
        #  trigger_price_to_put_in_position,trigger_price_to_close, original_quantity) values (3, "NEW", 0, 0.1, 1, 1);
        radar_list_dict = dict(order_id=3,order_status='NEW',order_id_to_close=0,trigger_price_to_put_in_position=0.1,
                               trigger_price_to_close=1.0, original_quantity=1)

        my_dict = {'activatePrice': 'None', 'avgPrice': '0.0', 'clientOrderId': '7dtD7WA7MgtYGB4YNAZItg', 'closePosition': 'False',
                        'cumBase': '0.0', 'executedQty': '0.0', 'orderId': '6443889218', 'origQty': '1.0', 'origType': 'LIMIT', 'positionSide': 'LONG',
                        'price': '1.0', 'priceRate': 'None', 'reduceOnly': 'True', 'side': 'SELL', 'status': 'NEW', 'stopPrice': '0.0', 'symbol': 'ADAUSD_PERP',
                         'timeInForce': 'GTC', 'type': 'LIMIT', 'updateTime': '1652801027591', 'workingType': 'CONTRACT_PRICE'}
        #mock_silent_limit_no_oco_sell_long.return_value = "dummy" 
        #mock_create_dict_from_output.return_value = my_dict
        event_order_id = '3'

        #rc = process_goto_in_position(event_order_id, radar_list_dict)              
        #self.assertEqual("OK process_goto_in_position", rc)   #OK

if __name__ == '__main__':
    unittest.main()        