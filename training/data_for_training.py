import requests
import pandas as pd
import time

def get_binance_data(symbol, interval='1h', limit=1000, start_time=None, end_time=None):
    url = 'https://api.binance.com/api/v1/klines'
    
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit}
    
    if start_time:
        params['startTime'] = start_time
    if end_time:
        params['endTime'] = end_time

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        df = df[['timestamp', 'close']]
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error during the request: {e}")
        return pd.DataFrame()

def fetch_full_data(symbol, interval='1h', total_days=365):

    end_time = int(time.time() * 1000)
    start_time = int((time.time() - 60 * 60 * 24 * total_days) * 1000)

    all_data = []
    
    while start_time < end_time:
        data = get_binance_data(symbol, interval=interval, start_time=start_time, end_time=end_time)
        
        if data.empty:
            break
        
        all_data.append(data)
        start_time = int(data.index[-1].timestamp() * 1000) + 1 
        
    if all_data:
        full_data = pd.concat(all_data)
        return full_data
    else:
        return pd.DataFrame()


btc_data = fetch_full_data('BTCUSDT', total_days=500)
if not btc_data.empty:
    btc_data.to_csv('BTC_500days.csv')

eth_data = fetch_full_data('ETHUSDT', total_days=500)
if not eth_data.empty:
    eth_data.to_csv('ETH_500days.csv')

ltc_data = fetch_full_data('LTCUSDT', total_days=500)
if not ltc_data.empty:
    ltc_data.to_csv('LTC_500days.csv')




