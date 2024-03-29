from binance import Client


class Bot:
    def __init__(self, api_key, api_secret, ticker, symbol):
        self.ticker = ticker
        self.symbol = symbol
        self.client = Client(api_key, api_secret)

    def get_server_time(self):
        server_time = self.client.get_server_time()
        server_time = server_time['serverTime']

        return server_time

    def check_position_info(self):
        has_positions = False

        try:
            positions = self.client.futures_coin_position_information(timestamp=self.get_server_time())

            for position in positions:
                symbol = position['symbol']
                position_amt = float(position['positionAmt'])

                if position_amt != 0:
                    if symbol == self.symbol:
                        has_position = True
                        break

        except Exception as e:
            print("포지션 조회 실패: ", e)

        return has_positions

    def check_open_orders(self):
        has_open_orders = False

        try:
            orders = self.client.futures_coin_get_open_orders(symbol=self.symbol, timestamp=self.get_server_time())

            for order in orders:
                if order['symbol'] == self.symbol:
                    if order['closePosition']:
                        has_open_orders = True

        except Exception as e:
            print("주문 조회 실패: ", e)

        return has_open_orders

    def get_balance(self):
        asset_balance = 0.0

        try:
            account_info = self.client.futures_coin_account_balance(timestamp=self.get_server_time())

            for balance in account_info:
                if balance['asset'] == self.ticker:
                    asset_balance = float(balance['balance'])
                    break

        except Exception as e:
            print("잔고 조회 실패: ", e)

        return asset_balance

    def get_market_price(self):
        market_price = 0.0

        try:
            market_price = self.client.futures_coin_mark_price(symbol=self.symbol)
            market_price = float(market_price[0]['markPrice'])

        except Exception as e:
            print("가격 조회 실패: ", e)

        return market_price

    def get_contract_size(self):
        contract_size = 0.0

        try:
            exchange_info = self.client.futures_coin_exchange_info()
            for symbol_info in exchange_info['symbols']:
                if symbol_info['symbol'] == self.symbol:
                    contract_size = float(symbol_info['contractSize'])

        except Exception as e:
            print("계약 크기 조회 실패: ", e)

        return contract_size

    def get_calculated_order_qty(self):
        min_qty = self.get_contract_size() / self.get_market_price()
        quantity = int(self.get_balance() / min_qty)

        return quantity

    def open_1x_short_position(self):
        quantity = self.get_calculated_order_qty()

        try:
            self.client.futures_coin_change_leverage(symbol=self.symbol, leverage=1)
            order = self.client.futures_coin_create_order(
                symbol=self.symbol,
                side='SELL',
                positionSide='SHORT',
                type='MARKET',
                quantity=quantity
            )

            print(f"주문이 제출되었습니다. 수량: {quantity} Cont")

        except Exception as e:
            print("주문 제출 실패: ", e)
