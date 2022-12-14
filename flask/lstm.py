import math
import pandas_datareader as web
import numpy as np
from datetime import datetime,timedelta
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

i = 0

def predict(ticker,end_date,fp,df):
    global i 
    i += 1
    data = df.filter(['Close'])
    dataset = data.values
    training_data_len = math.ceil(len(dataset) * .8)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    train_data = scaled_data[0:training_data_len, :]
    x_train = []
    y_train = []
    for i in range(60, len(train_data)):
        x_train.append(train_data[i - 60:i, 0])
        y_train.append(train_data[i, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, batch_size=1, epochs=1)
    test_data = scaled_data[training_data_len - 60:, :]
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i - 60:i, 0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    rmse = np.sqrt(np.mean(predictions - y_test) ** 2)


    while rmse>3:
        model.fit(x_train, y_train, batch_size=1, epochs=1)
        test_data = scaled_data[training_data_len - 60:, :]
        x_test = []
        y_test = dataset[training_data_len:, :]
        for i in range(60, len(test_data)):
            x_test.append(test_data[i - 60:i, 0])
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)
        rmse = np.sqrt(np.mean(predictions - y_test) ** 2)



    quote = df
    new_df = quote.filter(['Close'])
    last_60_days = new_df[-60:].values
    last_60_days_scaled = scaler.transform(last_60_days)
    X_test = []
    X_test.append(last_60_days_scaled)
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    pred_price = model.predict(X_test)
    pred_price = scaler.inverse_transform(pred_price)
    val=pred_price[0][0]
    temp = {}
    temp["Ticker"] = ticker
    temp["Price"] = float(val)
    fp.append(temp)
    print(i)

def call(end_date,fp,tickers):
    i = 0
    for ticker in tickers:
        i += 1
        df = web.DataReader(ticker, data_source='yahoo', start='2018-01-01', end=end_date)
        predict(ticker,end_date,fp,df)
        print(i)
    return fp
