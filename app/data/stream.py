import json
import os
import time
from kafka import KafkaConsumer, KafkaProducer
from config.config import load_config

CONFIG_FILE = "config.json"

producer = KafkaProducer(
    bootstrap_servers=os.environ.get("KAFKA_BROKER", "kafka:9093"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

consumer = KafkaConsumer(
    'MarketData',
    bootstrap_servers=os.environ.get("KAFKA_BROKER", "kafka:9093"),
    group_id='price_checking',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

latest_ticks = {} 


def analyze(symbol):
    inputs = latest_ticks[symbol]
    if len(inputs) < 2:
        return

    sorted_prices = sorted(inputs.items(), key=lambda x: x[1][0])
    lowest_exchange, (lowest_price, _) = sorted_prices[0]
    highest_exchange, (highest_price, _) = sorted_prices[-1]

    spread_abs = highest_price - lowest_price
    spread_pct = spread_abs / lowest_price

    spread_threshold = load_config()

    if spread_pct >= spread_threshold:
        timestamp = max(ts for _, (_, ts) in inputs.items())
        alert = {
            "symbol": symbol,
            "timestamp": timestamp,
            "spread_abs": spread_abs,
            "spread_pct": spread_pct,
            "lowest_exchange": lowest_exchange,
            "lowest_price": lowest_price,
            "highest_exchange": highest_exchange,
            "highest_price": highest_price,
            "source_exchanges": list(inputs.keys())
        }
        producer.send("alerts", alert)

for message in consumer:
    data = message.value
    exchange = data['exchange']
    symbol = data['symbol']
    price = data['price']
    timestamp = data['timestamp']

    if symbol not in latest_ticks:
        latest_ticks[symbol] = {}
    latest_ticks[symbol][exchange] = (price, timestamp)

    analyze(symbol)

