from client import get_binance_client
import pandas as pd


#  valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M


def get_history(symbol: str, interval: str, start: str, end=None):
    client = get_binance_client()
    timestamp = client._get_earliest_valid_timestamp(symbol='BTCUSDT', interval='1d')
    bars = client.get_historical_klines(symbol=symbol, interval=interval, start_str=start, end_str=end, limit=1000)
    df = pd.DataFrame(bars)
    df['Date'] = pd.to_datetime(df.iloc[:,0], unit='ms')
    df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore', 'Date']
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df.set_index('Date', inplace=True)
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df

