from kafka import KafkaConsumer
import json
import psycopg2
import time
import os
from database import db_connect

consumer = KafkaConsumer(
    "MarketData",
    bootstrap_servers=os.environ.get("KAFKA_BROKER", "kafka:9093"),
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def insert_to_db(timestamp, exchange, symbol, price):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO market_prices (timestamp, exchange, symbol, price) VALUES (%s, %s, %s, %s)", 
                (timestamp, exchange, symbol, price))
    conn.commit()


for message in consumer:
    data = message.value
    exchange = data['exchange']
    symbol = data['symbol']
    price = data['price']
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['timestamp']))
    insert_to_db(timestamp, exchange, symbol, price)


