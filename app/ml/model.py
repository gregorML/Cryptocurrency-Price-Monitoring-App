import os
import joblib
from tensorflow.keras.models import load_model
import streamlit as st
import pandas as pd
import requests

@st.cache_resource
def load_model_and_scaler(symbol):
    model_path = f'models/model_{symbol}.keras'
    scaler_path = f'models/scaler_{symbol}.pkl'
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        st.error(f"Missing model or scaler for {symbol}. Please check if the files are available.")
        return None, None
    model = load_model(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def predict_future_prices(start_prices, model, scaler, sequence_length):
    start_prices = scaler.transform(start_prices)
    start_prices = start_prices.reshape(1, sequence_length, 1)
    pred = model.predict(start_prices, verbose=0)
    pred = pred[0].reshape(sequence_length, 1)
    pred = scaler.inverse_transform(pred)
    return pred
    
def data_for_prediction(symbol, interval='1h', limit=1000, start_time=None, end_time=None):
    url = 'https://api.binance.com/api/v1/klines'
    symbol = symbol + "USDT"
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
        st.error(f"Error during the request: {e}")
        return pd.DataFrame()
