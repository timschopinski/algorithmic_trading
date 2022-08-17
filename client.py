from binance.client import Client
from settings import API_KEY, SECRET_KEY,\
    TESTNET_SECRET_KEY, TESTNET_API_KEY


def get_binance_client():
    return Client(api_key=API_KEY, api_secret=SECRET_KEY, tld='com')


def get_binance_test_client():
    return Client(api_key=TESTNET_API_KEY, api_secret=TESTNET_SECRET_KEY, tld='com', testnet=True)