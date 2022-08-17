from datetime import datetime
import logging
from client import get_binance_test_client
from binance import ThreadedWebsocketManager
from binance.exceptions import BinanceAPIException
import pandas as pd
from binance.client import Client
import numpy as np
import math
from logger.logger import get_logger
from test_enviroment.account.balance import get_current_balance
from visualization.simple_price_live_chart import SimpleLiveChart


class TradingBotAPSBS:

    """
    AVERAGE PRICE SPOT BUY SELL TRADING BOT #1
    The bot buys when the price goes up and sells
    when it goes down by given target_percentage % from the mid-price purchase price.
    after each transaction the bot calculates the
    mid-price purchase price.
    The bot ends trading when the price reaches the low or high limit
    the default is -oo and oo
    """

    def __init__(self, client: Client, symbol1: str, symbol2: 'str', target_percentage: float,
                 trade_quantity: float, high_limit: float = math.inf, low_limit: float = -math.inf,
                 *args, **kwargs):
        self._client = client
        self._symbol1 = symbol1
        self._symbol2 = symbol2
        self._pair = symbol1 + symbol2
        self._target_percentage = target_percentage     # %
        self._trade_quantity = trade_quantity
        self._high_limit = high_limit
        self._low_limit = low_limit
        self._twm = ThreadedWebsocketManager()
        self._mid_price = float(self._client.get_avg_price(symbol=self._pair)['price'])
        self._orders = []
        self.logger = get_logger('APSBS_data/APSBS.log')
        self.chart = kwargs.get('chart', None)

    def _get_current_pair_balance(self):
        return get_current_balance(self._client, self._symbol1, self._symbol2)

    def get_percentage(self, price: float):
        return math.fabs(100 - price * 100 / self._mid_price)

    def is_lower_than_mid_price(self, price: float):
        """ Returns True if the current price is down by target_percentage from the mid_price"""

        if price > self._mid_price:
            return False
        if self.get_percentage(price) > self._target_percentage:
            return True

    def is_higher_than_mid_price(self, price: float):
        """ Returns True if the current price is up by target_percentage from the mid_price"""

        if price < self._mid_price:
            return False
        if self.get_percentage(price) > self._target_percentage:
            return True

    def handle_order_message(self, order: dict):
        self.logger.info(f' {self._pair} {order["side"]} order for quantity of {order["origQty"]} at'
              f' average price {self.get_weighted_average_price(order)} has been executed successfully!')
        # self.logger.info(order)

    def get_weighted_average_price(self, order: dict):
        orders = order['fills']
        weighted_avg = 0
        for order in orders:
            weighted_avg += float(order['price']) * float(order['qty'])
        weighted_avg = weighted_avg / self._trade_quantity
        return weighted_avg

    def update_mid_price(self):
        self._mid_price = sum([self.get_weighted_average_price(order) for order in self._orders]) / len(self._orders)
        self.logger.info(f'mid price updated now is {self._mid_price}')

    def save_to_csv(self, order: dict):
        data = {
            'total_balance': [self._get_current_pair_balance()],
            'order_symbol': [self._pair],
            'order_side': [order['side']],
            'order_quantity': [self._trade_quantity],
            'order_type': [order['type']],
            'order_avg_price': [self.get_weighted_average_price(order)],
        }
        for asset in self._client.get_account()['balances']:
            symbol = asset['asset']
            if symbol == self._symbol1 or symbol == self._symbol2:
                data[symbol] = [asset['free']]
        # print(data)
        df1 = pd.DataFrame(data)
        df2 = pd.DataFrame(order)
        df1['time'] = pd.to_datetime(df2['transactTime'], unit='ms')
        df1.to_csv('APSBS_data/trades.csv', header=False, mode='a', index=False)
        df2['transactTime'] = pd.to_datetime(df2['transactTime'], unit='ms')
        df2.to_csv('APSBS_data/orders.csv', header=False, mode='a', index=False)

    def place_order(self, side: str):
        try:
            order = self._client.create_order(symbol='BTCUSDT', side=side, type='MARKET', quantity=self._trade_quantity)
            self._orders.append(order)
            self.handle_order_message(order)
            self.update_mid_price()
            self.chart.add_marker(0, self.get_weighted_average_price(order), side)
            self.save_to_csv(order)
        except BinanceAPIException:
            if side == 'BUY':
                asset = self._symbol2
            else:
                asset = self._symbol1
            self.logger.warning(f'Not enough {asset} to realize {side} order!')

    def open_strategy(self, time: datetime, price: float):
        if self.is_lower_than_mid_price(price):
            self.place_order('BUY')
        elif self.is_higher_than_mid_price(price):
            self.place_order('SELL')

    def validate_limit(self, price: float):
        """ Validates if the price reached any of the given limits """
        if price < self._low_limit:
            self._twm.stop()
            self.logger.critical(f'{self._pair} has reached the LOW LIMIT: {self._low_limit} $')
        elif price > self._high_limit:
            self._twm.stop()
            self.logger.critical(f'{self._pair} has reached the HIGH LIMIT: {self._high_limit} $')

    def handle_socket_message(self, time: datetime, price: float):
        logging.info('Time: {} | Symbol: {} | Price: {}'.format(time, self._pair, price))

    def handle_socket_data(self, data: dict):
        price = float(data['c'])
        volume = float(data['v'])
        time = pd.to_datetime(data['E'], unit='ms')
        self.handle_socket_message(time, price)
        self.validate_limit(price)
        self.open_strategy(time, price)
        if self.chart:
            self.chart.add_value(0, price)
            self.chart.add_value(1, volume)
            self.chart.render()

    def handle_intro_message(self):
        self.logger.critical(f'{datetime.utcnow()}  Starting The APSBS Trading Bot ...')
        self.logger.warning(f'Starting Balance is {self._get_current_pair_balance()} $'
                            f'Current Mid-Price is {self._mid_price}')

    def start(self):
        """init and start the WebSocket"""
        self.handle_intro_message()
        self._twm.start()
        self._twm.start_symbol_miniticker_socket(callback=self.handle_socket_data, symbol=self._pair)


def main():
    client = get_binance_test_client()
    price_volume_chart = SimpleLiveChart(
        file_path='APSBS_data/charts/simple_price_chart.png',
        number_of_plots=2,
        display=True,
        title1='BTCUSDT',
        x_label2='Time [s]',
        y_label1='Price [USDT]',
        y_label2='Volume',
        background_color1='grey',
        background_color2='green',
    )
    bot = TradingBotAPSBS(client, 'BTC', 'USDT', 0.1, 0.05, chart=price_volume_chart)
    bot.start()
    # bot.place_order('BUY')


if __name__ == '__main__':
    main()

