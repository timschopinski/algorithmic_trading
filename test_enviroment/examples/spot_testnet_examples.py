from client import get_binance_test_client
import pandas as pd
client = get_binance_test_client()
from binance.exceptions import BinanceAPIException

# account data

account = client.get_account()
df = pd.DataFrame(account['balances'])

df.free = pd.to_numeric(df.free, errors='coerce')
df.locked = pd.to_numeric(df.locked, errors='coerce')

print(df)


def get_current_btc_price():
    return client.get_symbol_ticker(symbol='BTCUSDT')


# get account total balance in USDT
def get_current_balance(account) -> float:
    df = pd.DataFrame(account['balances'])

    df.free = pd.to_numeric(df.free, errors='coerce')
    df.locked = pd.to_numeric(df.locked, errors='coerce')

    balance = 0
    for row in df.iloc:
        if row.asset not in ['BUSD', 'USDT']:
            price = float(client.get_symbol_ticker(symbol=str(row.asset) + 'USDT')['price'])
            balance += float(client.get_asset_balance(asset=row.asset)['free']) * price
        else:
            balance += float(client.get_asset_balance(asset=row.asset)['free'])
    return balance


# placing buy order
# try:
#     order = client.create_order(symbol='BTCUSDT', side='BUY', type='MARKET', quantity=1000)
#     print(order)
# except BinanceAPIException:
#     print('invalid amount!')

# placing sell order

# order = client.create_order(symbol='BTCUSDT', side='SELL', type='MARKET', quantity=0.1)
# print(order)


#  place a limit buy order
# print(get_current_btc_price())
# print(get_current_balance())
# order1 = client.create_order(symbol='BTCUSDT', side='BUY', type='LIMIT', quantity=0.1, timeInForce='GTC', price=22700)
# print(client.get_all_orders(symbol='BTCUSDT'))
# print(order1)

# get open orders

# open_orders = client.get_open_orders(symbol='BTCUSDT')
# print(open_orders)