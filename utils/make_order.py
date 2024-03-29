import main


def check_open_orders(client, symbol):
    try:
        orders = client.futures_coin_get_open_orders(symbol=symbol)
        return orders
    except Exception as e:
        print("주문 조회 실패: ", e)


def get_quantity(client, symbol):
    server_time = client.get_server_time()
    positions = client.futures_coin_position_information(timestamp=server_time['serverTime'])

    for position in positions:
        symbol = position['symbol']
        position_amt = float(position['positionAmt'])

        if position_amt != 0:
            if position['symbol'] is symbol:
                return position_amt


def check_position_info(client):
    server_time = client.get_server_time()
    positions = client.futures_coin_position_information(timestamp=server_time['serverTime'])

    for position in positions:
        symbol = position['symbol']
        position_amt = float(position['positionAmt'])

        if position_amt != 0:
            entry_price = float(position['entryPrice'])
            unrealized_pnl = float(position['unRealizedProfit'])
            print(f"{symbol}: Position Amount: {position_amt}, Entry Price: {entry_price}, Unrealized PNL: {unrealized_pnl}")


def check_account_info(client, ticker):
    server_time = client.get_server_time()
    account_info = client.futures_coin_account_balance(timestamp=server_time['serverTime'])

    my_balance = 0.0
    for balance in account_info:
        if balance['asset'] == ticker:
            my_balance = balance['balance']
            break

    return my_balance


def get_balance(client, ticker):
    server_time = client.get_server_time()
    account_info = client.futures_coin_account_balance(timestamp=server_time['serverTime'])

    my_balance = 0.0
    for balance in account_info:
        if balance['asset'] == ticker:
            my_balance = float(balance['balance'])
            break

    import math
    floor_number = math.floor(my_balance * 10000) / 10000
    print(floor_number)

    return floor_number


def close_long_position(client, symbol):
    try:
        quantity = get_quantity(client, symbol)  # 해당 포지션 수량(전체)
        order = client.futures_coin_create_order(
            symbol=symbol,
            side='SELL',
            positionSide='LONG',
            type='MARKET',
            quantity=quantity
        )
    except Exception as e:
        print("주문 제출 실패: ", e)


def get_symbol_price(client, symbol):
    try:
        ticker = client.futures_coin_mark_price(symbol=symbol)
        return float(ticker[0]['markPrice'])
    except Exception as e:
        print(f"Failed to get price for {symbol}: {e}")
        return None


def get_contract_size(client, symbol):
    try:
        exchange_info = client.futures_coin_exchange_info()
        for symbol_info in exchange_info['symbols']:
            if symbol_info['symbol'] == symbol:
                contract_size = float(symbol_info['contractSize'])
                return contract_size
    except Exception as e:
        print(f"Failed to get contract size for {symbol}: {e}")
        return None


def get_min_qty(client, symbol):
    raw_qty = get_contract_size(client, symbol) / get_symbol_price(client, symbol)
    import math
    min_qty = math.ceil(raw_qty * 10000) / 10000
    return raw_qty


def open_1x_short_position(client, ticker, symbol):
    try:
        client.futures_coin_change_leverage(symbol=symbol, leverage=1)
        quantity = int(get_balance(client, ticker) / get_min_qty(client, symbol))
        print(quantity)
        order = client.futures_coin_create_order(
            symbol=symbol,
            side='SELL',
            positionSide='SHORT',
            type='MARKET',
            quantity=quantity
        )
    except Exception as e:
        print("주문 제출 실패: ", e)

