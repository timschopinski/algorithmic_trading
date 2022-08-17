from datetime import datetime, timedelta
import time

import binance

from client import get_binance_test_client, get_binance_client
from fear_and_greed import get_fear_and_greed_index_with_js
from trading.notifications.email_notification import send_email


class BuyFearAndGreedBot:
    """ This bot checks every day if the fear and greed index
        is below the given index trigger and buys the given symbol
         for the specified amount
         Example: if the specified amount is 50 and the symbol us BTCUSDT and the index trigger is 20,
         The bot will buy BTC for 50 USDT if the index is below 20
         Notice! The default amount is 100 and the default index trigger is 10 """

    def __init__(self, client: binance.Client, symbol: str, amount: float = 100, index_trigger: int = 50):
        self.client = client
        self.symbol = symbol
        self.amount = amount
        self.index_trigger = index_trigger

    @staticmethod
    def validate_index(index):
        if not index:
            send_email("BuyFearAndGreedBot Error", "Error getting index")
            raise ValueError("Invalid Fear and Greed Index")
        if type(index) is not int:
            send_email("BuyFearAndGreedBot Error", "Error getting index")
            raise ValueError("Invalid Fear and Greed Index")
        if index < 0 or index > 100:
            send_email("BuyFearAndGreedBot Error", "Error getting index")
            raise ValueError("Invalid Fear and Greed Index")
        print(f'{datetime.now()}     Index: {index}')

    def get_quantity(self):
        price = self.client.get_symbol_ticker(symbol=self.symbol)['price']
        return round(self.amount / float(price), 7)

    def start_trading(self):
        print('Starting BuyFearAndGreedBot ...')
        while True:
            try:
                index = get_fear_and_greed_index_with_js()
            except Exception as e:
                send_email("BuyFearAndGreedBot Error", "Error getting index")
                raise e
            self.validate_index(index)
            if index < self.index_trigger:
                try:
                    quantity = self.get_quantity()
                    print(quantity)
                    order = self.client.create_order(symbol=self.symbol, side="BUY", type="MARKET", quantity=quantity)
                    msg = f'[{datetime.now()}] BUY {order["executedQty"]} {self.symbol} for {order["cummulativeQuoteQty"]} USDT at price {order["fills"][0]["price"]}'
                    send_email("BuyFearAndGreedBot", msg)
                    print(msg)
                except Exception as e:
                    msg = f"[{datetime.now()}] Error buying {self.amount} {self.symbol}"
                    send_email("BuyFearAndGreedBot Error", msg)
                    time.sleep(5)
                    raise Exception(msg) from e

            time.sleep(3600 * 24)


def main():
    client = get_binance_client()
    strategy = BuyFearAndGreedBot(client, "BTCUSDT")
    strategy.start_trading()


if __name__ == "__main__":
    main()
