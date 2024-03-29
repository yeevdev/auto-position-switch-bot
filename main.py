from utils.make_order import *
from binance.client import Client


API_KEY, API_SECRET = None, None  # binance API 키값
POSITION_MODE = None  # binance position mode(One Way, Hedge Mode)
SYMBOL = 'ETHUSD_PERP'
TICKER = 'ETH'
client = None  # python-binance Client






if __name__ == "__main__":
    with open("./binance.key") as f:
        lines = f.readlines()
        API_KEY = lines[0].strip()
        API_SECRET = lines[1].strip()

    client = Client(API_KEY, API_SECRET)
    POSITION_MODE = client.futures_coin_get_position_mode()

    #check_position_info(client)
    #print(check_account_info(client, TICKER))
    #close_long_position(client, TICKER)
    open_1x_short_position(client, TICKER, SYMBOL)
    #print(client.futures_coin_mark_price(symbol=SYMBOL))
    # print(get_min_qty(client,SYMBOL))
    # quantity = int(get_balance(client, TICKER) / get_min_qty(client, SYMBOL))
    # print(quantity)
    # print(get_min_qty(SYMBOL))