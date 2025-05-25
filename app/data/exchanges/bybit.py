import json
import time
import logging
import websocket
from kafka import KafkaProducer
from utils.list_of_cryptos import cryptos
import os

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

crypto_list = cryptos()

producer = KafkaProducer(
    bootstrap_servers=os.environ.get("KAFKA_BROKER", "kafka:9093"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"))

BYBIT_WS_URL = "wss://stream.bybit.com/v5/public/spot"

def on_message(ws, message):
    try:
        data = json.loads(message)
        if 'topic' in data and 'data' in data:
            if 'symbol' in data['data']:
                ticker_data = data['data']
                if 'lastPrice' in ticker_data:
                    crypto_message = {
                        "exchange": "bybit",
                        "symbol": ticker_data['symbol'].replace('USDT', ''),  
                        "price": float(ticker_data['lastPrice']),
                        "timestamp": time.time()
                    }
                    producer.send("MarketData", crypto_message)
    except Exception as e:
        log.error(f"Error processing message: {e}")

def on_error(ws, error):
    log.error(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    log.info(f"WebSocket closed: {close_status_code} - {close_msg}")
    log.info("Attempting to reconnect...")
    time.sleep(5)
    start_websocket()

def on_open(ws):
    try:
        streams = [f"tickers.{crypto.upper()}USDT" for crypto in crypto_list]
        subscription = {
            "op": "subscribe",
            "args": streams
        }
        ws.send(json.dumps(subscription))
        log.info(f"Subscribed to streams: {streams}")
    except Exception as e:
        log.error(f"Error on open: {e}")

def start_websocket():
    try:
        ws = websocket.WebSocketApp(
            BYBIT_WS_URL,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws.run_forever()
    except Exception as e:
        log.error(f"WebSocket client error: {e}")

start_websocket()

