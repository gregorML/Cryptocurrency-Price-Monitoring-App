# Cryptocurrency Price Monitoring App 🚀

A real-time cryptocurrency price monitoring application built with Apache Kafka, PostgreSQL, and Streamlit.

---

## 📦 Key Technologies

- **Kafka & Zookeeper** – Stream processing for real-time data
- **PostgreSQL** – Database for storing market data
- **Streamlit** – Web application for visualization and alerts
- **Docker & Docker Compose** – Containerized environment setup
- **WebSockets** – Low-latency data transmission between services

---

## 🗂️ Project Structure

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

## ⚙️ Running the Project

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

## 🧠 What Does the App Do?

- Fetches real-time data from exchanges: **Binance**, **Bybit**, **KuCoin**
- Stores data in a **PostgreSQL** database
- Provides real-time price monitoring and alerts via a **Streamlit dashboard**
- Uses LSTM models trained on 500 days of hourly data to predict price movements up to 24 hours ahead for selected cryptocurrencies (⚠️ Note: These predictions should be interpreted with caution, as short-term price movements are inherently difficult to predict accurately)
- Kafka and WebSocket integration enables ultra-low-latency processing and detection of price discrepancies across exchanges

---

## 🛠️ Requirements

- Docker and Docker Compose (for containerized setup)
- Python 3.9 (for local development outside Docker)

---
