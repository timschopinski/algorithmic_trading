from client import get_binance_test_client
from binance import ThreadedWebsocketManager
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




#   Demonstration purpose
#   Simple random Trading Bot: Stream Market Data
#   and buy 0.1 BTC (with USDT) once condition x
#   (Price and/or Volume) has been met.
#   Condition x: Price (rounded down) is divisible by 10 without reminder


client = get_binance_test_client()
account = client.get_account()
print(account)
# init and start the WebSocket
twm = ThreadedWebsocketManager()
twm.start()

values = []

def place_order():
    order = client.create_order(symbol='BTCUSDT', side='BUY', type='MARKET', quantity=0.1)
    print(order)


def handle_socket_message(data):
    time = pd.to_datetime(data['E'], unit='ms')
    price = float(data['c'])
    symbol = data['s']
    print('Time: {} | Symbol: {} | Price: {}'.format(time, symbol, price))
    print(data)
    # create data
    # values = np.cumsum(np.random.randn(1000, 1))
    # use the plot function
    # if int(price) % 10 == 0:
    #     place_order()
    #     twm.stop()
    # values.append(price)

    plt.plot(values)
    plt.savefig('simple_bot_data/price_chart.png')



twm.start_symbol_miniticker_socket(callback=handle_socket_message, symbol='BTCUSDT')


