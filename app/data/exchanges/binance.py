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
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

BINANCE_WS_URL = "wss://stream.binance.com:9443/stream?streams="

def build_stream_url():
    streams = [f"{crypto.lower()}usdt@ticker" for crypto in crypto_list]
    stream_path = "/".join(streams)
    return BINANCE_WS_URL + stream_path

def on_message(ws, message):
    try:
        data = json.loads(message)
        if 'data' in data and 's' in data['data']:
            ticker_data = data['data']
            crypto_message = {
                "exchange": "binance",
                "symbol": ticker_data['s'].replace('USDT', ''),
                "price": float(ticker_data['c']),
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
    log.info("WebSocket connection opened.")

def start_websocket():
    try:
        ws_url = build_stream_url()
        ws = websocket.WebSocketApp(
            ws_url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws.run_forever()
    except Exception as e:
        log.error(f"WebSocket client error: {e}")
        
start_websocket()

