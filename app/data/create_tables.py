import psycopg2
from database import db_connect

def create_tables():
    try:
        conn = db_connect()
        cur = conn.cursor()
        
        cur.execute("""SELECT to_regclass('public.market_prices');""")
        table_exists_market_prices = cur.fetchone()[0]

        if not table_exists_market_prices:
            create_table_query_market_prices = """
            CREATE TABLE IF NOT EXISTS market_prices (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                price DECIMAL NOT NULL,
                exchange VARCHAR(255) NOT NULL,
                symbol VARCHAR(255) NOT NULL
            );
            """
            cur.execute(create_table_query_market_prices)
        else:
            print("Table 'market_prices' already exists.")

        cur.execute("""SELECT to_regclass('public.alerts');""")
        table_exists_alerts = cur.fetchone()[0]

        if not table_exists_alerts:
            create_table_query_alerts = """
            CREATE TABLE IF NOT EXISTS alerts (
                id SERIAL PRIMARY KEY,
                symbol VARCHAR(50) NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                spread_abs FLOAT NOT NULL,
                spread_pct FLOAT NOT NULL,
                lowest_exchange VARCHAR(50) NOT NULL,
                lowest_price FLOAT NOT NULL,
                highest_exchange VARCHAR(50) NOT NULL,
                highest_price FLOAT NOT NULL,
                source_exchanges VARCHAR(50) NOT NULL
            );
            """
            cur.execute(create_table_query_alerts)
        else:
            print("Table 'alerts' already exists.")
        conn.commit()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

create_tables()

