#!/bin/bash
cd "$(dirname "$0")/.."

export PYTHONPATH=/app:$PYTHONPATH

echo "⏳ Waiting for PostgreSQL..."
python3 -c 'import socket; import time; s=None
while s is None:
  try:
    s = socket.create_connection(("postgres", 5432), timeout=2)
  except:
    time.sleep(3)
print("✅ PostgreSQL is ready!")'

echo "⏳ Waiting for Kafka..."
python3 -c 'import socket; import time; s=None
while s is None:
  try:
    s = socket.create_connection(("kafka", 9093), timeout=2)
  except:
    time.sleep(3)
print("✅ Kafka is ready!")'

python3 data/create_tables.py &
python3 data/exchanges/binance.py &
python3 data/exchanges/bybit.py &
python3 data/exchanges/kucoin.py &
python3 data/db_save.py &
python3 data/stream.py &
python3 data/alerts.py &

streamlit run app.py
wait
