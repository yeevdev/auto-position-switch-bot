from binance import Client


class Bot:
    def __init__(self, api_key, api_secret, ticker, symbol):
        self.api_key = api_key
        self.api_secret = api_secret
        self.ticker = ticker
        self.symbol = symbol

