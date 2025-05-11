from kafka import KafkaConsumer
import json
import psycopg2
import time
import os
from database import db_connect

consumer = KafkaConsumer(
    "alerts",
    bootstrap_servers=os.environ.get("KAFKA_BROKER", "kafka:9093"),
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)


def insert_alert(symbol, timestamp, spread_abs, spread_pct,
                 lowest_exchange, lowest_price, highest_exchange, highest_price, source_exchanges):
    conn = db_connect()
    cur = conn.cursor()
    query = """
        INSERT INTO alerts (
            symbol, timestamp, spread_abs, spread_pct,
            lowest_exchange, lowest_price, highest_exchange, highest_price, source_exchanges
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(query, (
        symbol, timestamp, spread_abs, spread_pct,
        lowest_exchange, lowest_price, highest_exchange, highest_price, source_exchanges
    ))
    conn.commit()


for message in consumer:

    data = message.value

    symbol = data['symbol']
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['timestamp']))
    spread_abs = data['spread_abs']
    spread_pct = data['spread_pct']
    lowest_exchange = data['lowest_exchange']
    lowest_price = data['lowest_price']
    highest_exchange = data['highest_exchange']
    highest_price = data['highest_price']
    source_exchanges = data['source_exchanges']

    insert_alert(
        symbol=symbol,
        timestamp=timestamp,
        spread_abs=spread_abs,
        spread_pct=spread_pct,
        lowest_exchange=lowest_exchange,
        lowest_price=lowest_price,
        highest_exchange=highest_exchange,
        highest_price=highest_price,
        source_exchanges=source_exchanges
    )


