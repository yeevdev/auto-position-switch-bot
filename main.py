from binance_client import Bot
import time


API_KEY, API_SECRET = None, None  # binance API 키값
SYMBOL = 'ETHUSD_PERP'
TICKER = 'ETH'

if __name__ == "__main__":
    with open("./binance.key") as f:
        lines = f.readlines()
        API_KEY = lines[0].strip()
        API_SECRET = lines[1].strip()

    bot = Bot(API_KEY, API_SECRET, TICKER, SYMBOL)

    initial_position_state = bot.check_position_info()
    initial_order_state = bot.check_open_orders()
    while True:
        if initial_order_state and initial_order_state:
            if not bot.check_position_info():
                if not bot.check_open_orders():
                    bot.open_1x_short_position()
        time.sleep(5)
