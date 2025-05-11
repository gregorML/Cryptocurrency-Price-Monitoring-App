import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping
from keras.optimizers import Adam
import joblib

def prepare_lstm_data(data, sequence_length, future_length):

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data.reshape(-1, 1))
    
    X, y = [], []

    for i in range(len(scaled_data) - sequence_length - future_length + 1):
        X.append(scaled_data[i : i + sequence_length])
        y.append(scaled_data[i + sequence_length : i + sequence_length + future_length])
    
    return np.array(X), np.array(y), scaler

def train_model(symbol, model_path, scaler_path, sequence_length, future_length, exchange='binance'):
    df = pd.read_csv(f"{symbol}_30days.csv")
    prices = df['close'].values
    X, y, scaler = prepare_lstm_data(prices, sequence_length, future_length)

    # Time-based split: 60% train, 20% val, 20% test
    total_len = len(X)
    train_end = int(total_len * 0.6)
    val_end = int(total_len * 0.8)

    X_train, y_train = X[:train_end], y[:train_end]
    X_val, y_val = X[train_end:val_end], y[train_end:val_end]
    X_test, y_test = X[val_end:], y[val_end:]

    print(f"Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")

    model = Sequential([
        Input(shape=(sequence_length, 1)),
        LSTM(64, activation='tanh', return_sequences=True),
        Dropout(0.3),
        LSTM(32, activation='tanh'),
        Dropout(0.3),
        Dense(future_length)
    ])
    opt = Adam(learning_rate=0.001)
    model.compile(optimizer=opt, loss='mae', metrics=['mse'])

    # Early stopping callback
    early_stop = EarlyStopping(monitor='val_loss', patience=2, restore_best_weights=True)

    model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=10,
        batch_size=16,
        verbose=1,
        callbacks=[early_stop]
    )

    test_loss, test_mse = model.evaluate(X_test, y_test, verbose=0)
    print(f"[TEST] MAE: {test_loss:.6f} | MSE: {test_mse:.6f}")

    model.save(model_path)
    joblib.dump(scaler, scaler_path)



n = 24
m = 24
train_model(symbol='BTC', model_path='model_BTC2.keras', scaler_path='scaler_BTC2.pkl', sequence_length = n, future_length = m)
train_model(symbol='ETH', model_path='model_ETH.keras', scaler_path='scaler_ETH.pkl', sequence_length = n, future_length = m)
train_model(symbol='LTC', model_path='model_LTC.keras', scaler_path='scaler_LTC.pkl', sequence_length = n, future_length = m)
