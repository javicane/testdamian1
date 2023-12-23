sqlite> .schema
CREATE TABLE mirror_radar_list(
  order_id INT,
  order_status TEXT,
  order_id_to_close INT,
  trigger_price_to_put_in_position REAL,
  trigger_price_to_close REAL,
  original_quantity INT
);
CREATE TABLE test_radar_list(
  order_id INT,
  order_status TEXT,
  order_id_to_close INT,
  trigger_price_to_put_in_position REAL,
  trigger_price_to_close REAL,
  original_quantity INT
);
CREATE TABLE order_hist (current_timestamp integer not null,activatePrice text not null,avgPrice text not null,clientOrderId text not null,closePosition text not null,cumBase text not null,executedQty text not null,orderId text not null,origQty text not null,origType text not null,positionSide text not null,price text not null,priceRate text not null,reduceOnly text not null,side text not null,status text not null,stopPrice text not null,symbol text not null,timeInForce text not null,type text not null,updateTime text not null,workingType text not null);
CREATE TABLE radar_list (order_id integer primary key,order_status text not null,order_id_to_close integer not null,trigger_price_to_put_in_position real not null,trigger_price_to_close real not null,original_quantity integer not null, clientorderid text not null, repeat text not null default "Y", resize integer not null default 1, factor_gain real not null default 1.00125, group_id integer not null default 0, conditional text not null default "N");
CREATE TABLE kk(
  order_id INT,
  order_status TEXT,
  order_id_to_close INT,
  trigger_price_to_put_in_position REAL,
  trigger_price_to_close REAL,
  original_quantity INT,
  clientorderid TEXT
);
CREATE TABLE pnl_hist (order_id integer primary key,order_status text not null,order_id_to_close integer not null,trigger_price_to_put_in_position real not null,trigger_price_to_close real not null,original_quantity integer not null, clientorderid text not null, repeat text not null default "Y", resize integer not null default 1, factor_gain real not null default 1.00125, group_id integer not null default 0, conditional text not null default "N");
CREATE TABLE engines (name text);
CREATE TABLE tracker_pnl (order_id integer primary key, timestamp integer not null, rp integer);
CREATE TABLE r_list (order_id integer primary key,order_status text not null,order_id_to_close integer not null,trigger_price_to_put_in_position real not null,trigger_price_to_close real not null,original_quantity integer not null);
CREATE TABLE tracker_balance ( balance real not null, timestamp integer not null);
CREATE TABLE tracker_funding_fee ( fee real not null, timestamp integer not null);
CREATE TABLE tracker_entry_price( entry_price real not null, timestamp integer not null);
CREATE TABLE probe(
  order_id INT,
  order_status TEXT,
  order_id_to_close INT,
  trigger_price_to_put_in_position REAL,
  trigger_price_to_close REAL,
  original_quantity INT,
  clientorderid TEXT,
  repeat TEXT,
  resize INT,
  factor_gain REAL,
  group_id INT
);
CREATE TABLE conditional_pivots (main_trigger_price real not null, trigger_price_to_put_in_position real not null, trigger_price_to_close real not null, original_quantity integer not null, active text not null default "N", rule text not null default "EMPTY");