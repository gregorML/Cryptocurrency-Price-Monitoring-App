Cryptocurrency Price Monitoring App 🚀
A real-time cryptocurrency price monitoring application built with Apache Kafka, PostgreSQL, and Streamlit.
📦 Key Technologies

Kafka & Zookeeper – Stream processing for real-time data
PostgreSQL – Database for storing market data
Streamlit – Web application for visualization and alerts
Docker & Docker Compose – Containerized environment setup

🗂️ Project Structure
├── app/                  # Main Streamlit application
│   ├── config/           # Configuration files (JSON, .py)
│   ├── data/             # Data processing and database connection logic
│   ├── ml/               # Machine learning model for price predictions
│   ├── models/           # Saved models and scalers
│   ├── scripts/          # Application startup scripts
│   └── utils/            # Helper functions
├── training/             # Scripts for training ML models
├── docker-compose.yml    # Ecosystem configuration
├── Dockerfile            # Application container build
├── requirements.txt      # Python dependencies
└── README.md             # This file :)

⚙️ Running the Project

Clone the repository:

git clone https://github.com/gregorML/Cryptocurrency-Price-Monitoring-App.git
cd Cryptocurrency-Price-Monitoring-App


Start the application using Docker:

docker-compose up --build


Access the application at: http://localhost:8501

🧠 What Does the App Do?

Fetches real-time data from exchanges: Binance, Bybit, KuCoin
Stores data in a PostgreSQL database
Provides real-time price monitoring and alerts via a Streamlit dashboard
Uses machine learning models (.keras) for price change predictions

🛠️ Requirements

Docker and Docker Compose (for containerized setup)
Python 3.9 (for local development outside Docker)


