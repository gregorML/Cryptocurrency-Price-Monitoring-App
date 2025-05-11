import psycopg2
import pandas as pd
import os

def db_connect():
    conn = psycopg2.connect(
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", 5432))
    return conn

def get_price_history(exchanges, symbol, start_timestamp, end_timestamp):
    conn = db_connect()
    try:
        query = """
            SELECT timestamp, price, exchange 
            FROM market_prices 
            WHERE symbol = %s 
              AND exchange IN %s 
              AND timestamp BETWEEN %s AND %s
            ORDER BY timestamp DESC
        """
        params = (symbol, tuple(exchanges), start_timestamp, end_timestamp)
        df = pd.read_sql(query, conn, params=params)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        print(f"Error while fetching data: {e}")
        return None
    finally:
        conn.close()

def get_anomalies(symbol, spread_pct, start_timestamp, end_timestamp):
    conn = db_connect()
    try:
        query = """
            SELECT symbol, timestamp, spread_abs, spread_pct, 
                   lowest_exchange, lowest_price, highest_exchange, highest_price 
            FROM alerts
            WHERE 
                symbol = %s
                AND spread_pct >= %s
                AND timestamp BETWEEN %s AND %s
            ORDER BY timestamp DESC 
            LIMIT 30
        """
        params = (symbol, spread_pct, start_timestamp, end_timestamp)
        df = pd.read_sql(query, conn, params=params)
        df = df.rename(columns={
            'symbol': 'Symbol',
            'timestamp': 'Time',
            'spread_abs': 'Absolute Change',
            'spread_pct': 'Percentage Change (%)',
            'lowest_exchange': 'Lowest Exchange',
            'lowest_price': 'Lowest Price',
            'highest_exchange': 'Highest Exchange',
            'highest_price': 'Highest Price'
        })
        df['Time'] = pd.to_datetime(df['Time']).dt.strftime('%Y-%m-%d %H:%M:%S')
        return df
    except Exception as e:
        print(f"Error while fetching data: {e}")
        return None
    finally:
        conn.close()
