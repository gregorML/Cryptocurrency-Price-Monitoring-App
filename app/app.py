import streamlit as st
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import datetime
import time

# Import functions from separate modules
from data.database import get_price_history, get_anomalies
from ml.model import load_model_and_scaler, predict_future_prices, data_for_prediction
from config.config import load_config, save_config
from utils.utils import timestamp_validation
from utils.list_of_cryptos import cryptos

# Streamlit page configuration
st.set_page_config(page_title="Real-Time Crypto Monitoring", layout="wide", page_icon="📈")
cryptos = cryptos()
st.title("📊 Real-Time Crypto Monitoring")

# Define tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Price History",
    "🔮 Prediction",
    "⚠️ Alerts",
    "⚙️ Settings"
])

# Tab 1: Price History
with tab1:
    col1, col2 = st.columns([3, 1])
    with col2:
        with st.container():
            st.subheader("Settings")
            symbol = st.selectbox("Select symbol:", cryptos, key="symbol")
            available_exchanges = ['binance', 'bybit', 'kucoin']
            exchanges = st.multiselect(
                "Select exchanges:",
                available_exchanges,
                default=['binance'],
                key="exchanges")
            today = datetime.date.today()
            default_start_time = datetime.time(0, 0)
            default_end_time = datetime.time(23, 0)
            col11, col21 = st.columns(2)
            with col11:
                start_date = st.date_input("Start date:", value=today, key='sd1')
            with col21:
                start_time = st.time_input("Start time:", value=default_start_time, key='sh1')
            col31, col41 = st.columns(2)
            with col31:
                end_date = st.date_input("End date:", value=today, key='ed1')
            with col41:
                end_time = st.time_input("End time:", value=default_end_time, key='eh1')
            start_timestamp, end_timestamp = timestamp_validation(start_date, start_time, end_date, end_time)

    with col1:
        st.header("📈 Price History")
        with st.container():
            if 'chart_count' not in st.session_state:
                st.session_state.chart_count = 0
            if exchanges and start_timestamp and end_timestamp:
                df_history = get_price_history(exchanges, symbol, start_timestamp, end_timestamp)
                if df_history is not None and not df_history.empty:
                    fig = px.line(
                        df_history,
                        x="timestamp",
                        y="price",
                        color="exchange",
                        title=f"Price of {symbol} (USD) Across Exchanges",
                        template="plotly_white"
                    )
                    fig.update_traces(connectgaps=False)
                    fig.update_layout(
                        xaxis_title="Time",
                        yaxis_title="Price (USD)",
                        font=dict(size=12),
                        legend_title="Exchange"
                    )
                    st.plotly_chart(fig, key=f"chart_{st.session_state.chart_count}")
                    st.session_state.chart_count += 1
                else:
                    st.warning("No data to display.")
            else:
                st.info("Select at least one exchange and valid timestamps.")

# Tab 2: Prediction
with tab2:
    st.header("🔮 Cryptocurrency Price Forecast")
    col1, col2 = st.columns([1, 1])
    with col1:
        symbol = st.selectbox("Select Cryptocurrency", cryptos, key='symbol_crypto')
    with col2:
        forecast_length = st.selectbox("Select Cryptocurrency", ['Short-Term', 'Long-Term'], key='forecast')
    
    if forecast_length == 'Short-Term':
        freq = '1h'
        sequence_length = 24
        n_days = 1
    else:
        freq = '1d'
        sequence_length = 14
        n_days = 14
        
    chart_container = st.empty()
    with chart_container:
        try:
            st.write(f"Loading model for {symbol}...")
            model, scaler = load_model_and_scaler(symbol, forecast_length)
            if not model or not scaler:
                st.error("Failed to load model or scaler for the selected cryptocurrency.")
            if 'chart_count' not in st.session_state:
                st.session_state.chart_count = 0
                
            end_time = int(time.time() * 1000)
            start_time = int((time.time() - 60 * 60 * 24 * n_days) * 1000)
            
            if start_time >= end_time:
                st.error("Invalid time range for data retrieval.")
                
            df = data_for_prediction(symbol, start_time=start_time, end_time=end_time, interval = freq)
            df['close'] = pd.to_numeric(df['close'], errors='coerce')
            
            if df is None or df.empty or len(df) < sequence_length:
                st.error("Insufficient or no historical data available for prediction.")
                
            start_prices = df['close'].values[-sequence_length:]
            start_prices = start_prices.reshape(-1, 1)
            
            predicted_prices = predict_future_prices(start_prices, model, scaler, sequence_length=sequence_length)
            
            last_time = df.index[-1]
            history_times = df.index[-sequence_length:]
            future_times = pd.date_range(start=last_time, periods=sequence_length, freq=freq)

            
            df_history = pd.DataFrame({
                'timestamp': history_times,
                'price': start_prices.flatten(),
                'type': ['History'] * len(history_times)
            })
            df_future = pd.DataFrame({
                'timestamp': future_times,
                'price': predicted_prices.flatten(),
                'type': ['Prediction'] * len(future_times)
            })
            
            df_plot = pd.concat([df_history, df_future], ignore_index=True)
            df_plot.sort_values(by="timestamp", inplace=True)

            fig = px.line(
                df_plot,
                x="timestamp",
                y="price",
                color="type",
                title=f"Price Prediction for {symbol}",
                template="plotly_white",
                color_discrete_map={'History': 'red', 'Prediction': 'green'}
            )
            fig.update_layout(
                xaxis_title="Time",
                yaxis_title="Price",
                font=dict(size=12),
                legend_title="Data Type"
            )
            st.plotly_chart(fig, key=f"chart_{st.session_state.chart_count}")
            st.session_state.chart_count += 1
            
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

# Tab 3: Alerts
with tab3:
    col1, col2 = st.columns([3, 1])
    with col2:
        with st.container():
            st.subheader("Settings")
            symbol = st.selectbox("Select Symbol:", cryptos, key="symbol3")
            current_value = load_config()
            threshold = st.slider("Monitoring Threshold (%):", min_value=0.001, max_value=float(1), value=float(0.01), step=float(0.001), key='threshold3')
            st.write(f"Selected threshold: {threshold:.3f}")
            save_config(threshold / 100)
            threshold2 = st.slider("Display Threshold (%):", min_value=0.001, max_value=float(1), value=float(0.01), step=float(0.001), key='threshold32')
            st.write(f"Selected threshold: {threshold2:.3f}")
            today = datetime.date.today()
            default_start_time = datetime.time(9, 0)
            default_end_time = datetime.time(17, 0)
            col11, col21 = st.columns(2)
            with col11:
                start_date = st.date_input("Start Date:", value=today, key='sd3')
            with col21:
                start_time = st.time_input("Start Time:", value=default_start_time, key='sh3')
            col31, col41 = st.columns(2)
            with col31:
                end_date = st.date_input("End Date:", value=today, key='ed3')
            with col41:
                end_time = st.time_input("End Time:", value=default_end_time, key='eh3')
            start_timestamp, end_timestamp = timestamp_validation(start_date, start_time, end_date, end_time)

    with col1:
        st.header("⚠️ Alerts")
        if start_timestamp and end_timestamp:
            df_anomalies = get_anomalies(symbol, threshold2, start_timestamp, end_timestamp)
            if df_anomalies is not None:
                st.dataframe(df_anomalies, use_container_width=True, hide_index=True)
            else:
                st.warning("No anomalies to display.")

# Tab 4: Settings
with tab4:
    st.header("⚙️ Settings")
    refresh_rate = st.slider("Refresh rate (seconds):", min_value=5, max_value=60, value=60, step=5, key='refresh_rate')

# Auto-refresh
st_autorefresh(interval=refresh_rate * 1000, key="auto_refresh")
