# Real-Time Cryptocurrency Price Monitoring System

## Overview
This project is a real-time cryptocurrency price monitoring system that collects, processes, and visualizes price data from multiple exchanges (Binance, ByBit, KuCoin) using Apache Kafka as the core message broker. It includes features for price prediction using LSTM models, anomaly detection for price differences across exchanges, and an interactive web interface built with Streamlit. The entire system is containerized using Docker Compose for easy deployment and scalability.

The system allows users to:

- Monitor real-time cryptocurrency prices
- Visualize historical price data
- Receive alerts for significant price discrepancies between exchanges
- View price predictions based on trained LSTM models
- Configure system settings dynamically

---

## Technologies Used

- **Kafka & Zookeeper** – Stream processing for real-time data
- **PostgreSQL** – Database for storing market data
- **Streamlit** – Web application for visualization and alerts
- **Docker & Docker Compose** – Containerized environment setup
- **WebSockets** – Low-latency data transmission between services
- **LSTM** - RNN model built with Keras for price prediction

---

## Features
- Real-Time Data Collection: Fetches live price data from Binance, ByBit, and KuCoin via WebSocket APIs.
- Apache Kafka Integration: Streams data through Kafka topics (MarketData and Alerts) for efficient processing.
- Price Anomaly Detection: Identifies significant price differences across exchanges and generates alerts.
- LSTM-Based Price Prediction: Provides short-term (24-hour) and long-term (14-day) price forecasts for BTC, ETH, and LTC.
- Interactive Web Interface: Built with Streamlit, featuring tabs for:
  - Price History: Visualize historical price data.
  - Prediction: Display LSTM model predictions.
  - Alerts: Show price discrepancy alerts.
  - Settings: Configure refresh rates and anomaly thresholds.
- Containerized Deployment: Uses Docker Compose to run Kafka, Zookeeper, PostgreSQL, and Streamlit in isolated containers.
- PostgreSQL Storage: Stores price data and alerts for historical analysis.

---

## LSTM Models
- Short-Term Model: Trained on 500 days of hourly data, predicts next 24 hours.
- Long-Term Model: Trained on 2000 days of daily data, predicts next 14 days.
- Models are trained for BTC, ETH, and LTC with MAE (0.02–0.08) and MSE (0.006–0.012) on normalized data.

---

## Project Structure

```
├── app/                  # Main Streamlit application
│   ├── config/           # Configuration files (JSON, .py)
│   ├── data/             # Data processing and database connection logic
│   ├── ml/               # LSTM models for price predictions
│   ├── models/           # Saved models and scalers
│   ├── scripts/          # Application startup scripts
│   └── utils/            # Helper functions
├── training/             # Scripts for training LSTM models
├── docker-compose.yml    # Ecosystem configuration
├── Dockerfile            # Application container build
├── requirements.txt      # Python dependencies
└── README.md
```

---

## Running the Project

1. **Clone the repository:**
```bash
git clone https://github.com/gregorML/Cryptocurrency-Price-Monitoring-App.git
cd Cryptocurrency-Price-Monitoring-App
```

2. **Start the application using Docker:**
```bash
docker-compose up --build
```

3. **Access the application at:**
[http://localhost:8501](http://localhost:8501)

---

## Requirements

- Docker and Docker Compose (for containerized setup)
- Python 3.9 (for local development outside Docker)

---
