import json
import time
import logging
import requests
import websocket
from kafka import KafkaProducer
from utils.list_of_cryptos import cryptos
import os

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

crypto_list = cryptos()
symbols = [f"{crypto.upper()}-USDT" for crypto in crypto_list]

producer = KafkaProducer(
    bootstrap_servers=os.environ.get("KAFKA_BROKER", "kafka:9093"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

KUCOIN_WS_TOKEN_URL = "https://api.kucoin.com/api/v1/bullet-public"

def get_ws_details():
    try:
        response = requests.post(KUCOIN_WS_TOKEN_URL)
        res_json = response.json()
        if res_json["code"] == "200000":
            return res_json["data"]
        else:
            log.error(f"Failed to get WebSocket token: {res_json}")
    except Exception as e:
        log.error(f"Error fetching WebSocket token: {e}")
    return None

def on_message(ws, message):
    try:
        msg = json.loads(message)
        if msg.get("type") == "message" and msg.get("subject") == "trade.ticker":
            data = msg.get("data", {})
            topic = msg.get("topic", "")

            if ":" in topic:
                full_symbol = topic.split(":")[1]
                symbol = full_symbol.replace('-USDT', '')
            else:
                symbol = None

            price = data.get("price")

            if symbol and price:
                crypto_message = {
                    "exchange": "kucoin",
                    "symbol": symbol,
                    "price": float(price),
                    "timestamp": time.time()
                }
                producer.send("MarketData", crypto_message)
            else:
                log.warning(f"Incomplete ticker data: {data}, topic: {topic}")

        elif msg.get("type") in {"pong", "welcome", "ack"}:
            log.debug(f"Ignored system message: {msg}")
        else:
            log.debug(f"Unhandled message type: {msg}")

    except Exception as e:
        log.error(f"Error processing message: {e}")
        log.debug(f"Raw message: {message}")



def on_error(ws, error):
    log.error(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    log.info(f"WebSocket closed: {close_status_code} - {close_msg}")
    log.info("Attempting to reconnect...")
    time.sleep(5)
    start_websocket()

def on_open(ws):
    try:
        subscribe_msg = {
            "id": str(int(time.time() * 1000)),
            "type": "subscribe",
            "topic": "/market/ticker:{}".format(','.join(symbols)),
            "response": True
        }
        ws.send(json.dumps(subscribe_msg))
        log.info(f"Subscribed to ticker for: {symbols}")
    except Exception as e:
        log.error(f"Error on open: {e}")

def start_websocket():
    try:
        ws_details = get_ws_details()
        if not ws_details:
            return

        endpoint = ws_details["instanceServers"][0]["endpoint"]
        token = ws_details["token"]
        ws_url = f"{endpoint}?token={token}"

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

