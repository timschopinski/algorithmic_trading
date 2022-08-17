from client import get_binance_client
import pandas as pd
from historical_data import get_history
from binance import ThreadedWebsocketManager, BinanceSocketManager, AsyncClient
from settings import API_KEY, SECRET_KEY
import time

client = get_binance_client()

#  Basic
# print(client.ping())
# print(client.get_system_status())
# account = client.get_account()
#
# #  Api limits
# # client.get_exchange_info()['rateLimits']
#
# df = pd.DataFrame(account['balances'])
# df.free = pd.to_numeric(df.free, errors='coerce')
# df.locked = pd.to_numeric(df.locked, errors='coerce')
#
# print(df.loc[df.free > 0])

#  Current prices

# print(client.get_symbol_ticker(symbol='BTCUSDT'))
#  get all prices
# prices = client.get_all_tickers()
# df = pd.DataFrame(prices)
# print(df)


#  get historical data

# timestamp = client._get_earliest_valid_timestamp(symbol='BTCUSDT', interval='1d')
# timestamp = pd.to_datetime(timestamp, unit='ms')
# print(timestamp)

# bars = client.get_historical_klines(symbol='BTCUSDT', interval='1d', start_str=timestamp, limit=1000)
# df = pd.DataFrame(bars)
# df['Date'] = pd.to_datetime(df.iloc[:,0], unit='ms')
# df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore', 'Date']
# df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
# print(df)

# getting history
# from datetime import timedelta, datetime
# now = datetime.utcnow()
# two_hours_before = now - timedelta(hours=2)
# print(get_history('BTCUSDT', '1m', str(two_hours_before)))

# loading from csv
#
# df = pd.read_csv('marekt_data/BTCUSDT-1h-2022-08-04.csv', header=None)
# df['Date'] = pd.to_datetime(df.iloc[:,0], unit='ms')
# df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume',
#               'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore', 'Date']
# df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
# df.set_index('Date', inplace=True)
# for column in df.columns:
#     df[column] = pd.to_numeric(df[column], errors='coerce')
# print(df)


#  streaming market data


# def stream_data(msg):
#     """ define how to process incoming WebSocket messages """
#     print(msg)
#
#
# twm = ThreadedWebsocketManager(api_key=API_KEY, api_secret=SECRET_KEY)
# twm.start()
# symbol = 'BTCUSDT'
#
# df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Complete'])
#
# def stream_candles(msg):
#     """ define how to process incoming WebSocket messages """
#     event_time = pd.to_datetime(msg['E'], unit='ms')
#     start_time = pd.to_datetime(msg['k']['t'], unit='ms')
#     first = float(msg['k']['o'])
#     high = float(msg['k']['h'])
#     low = float(msg['k']['l'])
#     close = float(msg['k']['c'])
#     volume = float(msg['k']['v'])
#     complete = msg['k']['x']
#     symbol = msg['s']
#
#     print('Time: {} | Symbol: {} | Price: {}'.format(event_time, symbol, close))
#     df.loc[start_time] = [first, high, low, close, volume, complete]
#
# def handle_socket_message(msg):
#     time = pd.to_datetime(msg['E'], unit='ms')
#     price = msg['c']
#     symbol = msg['s']
#     print('Time: {} | Symbol: {} | Price: {}'.format(time, symbol, price))
#
#
# # twm.start_symbol_miniticker_socket(callback=handle_socket_message, symbol=symbol)
# twm.start_kline_socket(callback=stream_candles, symbol=symbol, interval='1m')
#
# twm.stop()
# time.sleep(1)
# print(df)
# twm.join()

# twm.stop()




#  creating a test order
#
# order = client.create_test_order(symbol='BTCEUR', side='BUY', type='MARKET', quantity=0.1)
# print(order)


