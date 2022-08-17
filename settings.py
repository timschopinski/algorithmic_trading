import os
from dotenv import load_dotenv
load_dotenv()


API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

TESTNET_API_KEY = os.getenv('TESTNET_API_KEY')
TESTNET_SECRET_KEY = os.getenv('TESTNET_SECRET_KEY')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')