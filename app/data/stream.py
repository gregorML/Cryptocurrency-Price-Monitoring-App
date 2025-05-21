import json
import os
import time
from kafka import KafkaConsumer, KafkaProducer
from config.config import load_config

CONFIG_FILE = "config.json"f
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
last_alerts = {}    

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
    now = time.time()

    last_data = last_alerts.get(symbol)
    if last_data:
        last_spread = last_data[0]
        last_time = last_data[1]
    else:
        last_spread = None
        last_time = None

    delta = 0.001
    min_interval = 1.0

    if spread_pct >= spread_threshold and (last_spread is None or abs(spread_pct - last_spread) > delta or now - last_time > min_interval):
        
        timestamp = None

        for value in inputs.values():
            ts = value[1]
            if timestamp is None or ts > timestamp:
                timestamp = ts
                
        alert = {
            "symbol": symbol,
            "timestamp": timestamp,
            "spread_abs": spread_abs,
            "spread_pct": round(spread_pct, 4),
            "lowest_exchange": lowest_exchange,
            "lowest_price": lowest_price,
            "highest_exchange": highest_exchange,
            "highest_price": highest_price,
            "source_exchanges": list(inputs.keys())
        }
        producer.send("alerts", alert)
        last_alerts[symbol] = (spread_pct, now)

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

