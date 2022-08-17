import pandas as pd


def get_current_balance(client, *args) -> float:
    """ Get account total balance in USD.
        Specify what crypto balances you want to get
        with passing additional symbols as *args.
     """

    account = client.get_account()
    df = pd.DataFrame(account['balances'])

    df.free = pd.to_numeric(df.free, errors='coerce')
    df.locked = pd.to_numeric(df.locked, errors='coerce')

    # balance = sum([float(client.get_asset_balance(asset=row.asset)['free']) * float(client.get_symbol_ticker(symbol=str(row.asset) + 'USDT')['price']) for row in df.iloc])

    balance = 0
    try:
        for symbol in args:
            if symbol not in ['BUSD', 'USDT']:
                price = float(client.get_symbol_ticker(symbol=symbol + 'USDT')['price'])
                balance += float(client.get_asset_balance(asset=symbol)['free']) * price
            else:
                balance += float(client.get_asset_balance(asset=symbol)['free'])
    except ValueError:
        raise ValueError('Invalid asset symbol')

    if args:
        return balance

    for row in df.iloc:
        if row.asset not in ['BUSD', 'USDT']:
            price = float(client.get_symbol_ticker(symbol=str(row.asset) + 'USDT')['price'])
            balance += float(client.get_asset_balance(asset=row.asset)['free']) * price
        else:
            balance += float(client.get_asset_balance(asset=row.asset)['free'])
    return balance
