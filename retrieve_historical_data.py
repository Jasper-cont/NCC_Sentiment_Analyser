import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def get_historical_data(ticker, start_date, end_date):

    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def calculate_changes(data):

    data['Price Change'] = data['Close'] - data['Open']

    data['Volume Change'] = data['Volume'].pct_change()

    return data

def calculate_rsi(data, window=14):

    data['Daily Change'] = data['Close'].diff()

    data['Gain'] = data['Daily Change'].apply(lambda x: x if x > 0 else 0)
    data['Loss'] = data['Daily Change'].apply(lambda x: -x if x < 0 else 0)

    avg_gain = data['Gain'].rolling(window=window, min_periods=1).mean()
    avg_loss = data['Loss'].rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss

    data['RSI'] = 100 - (100 / (1 + rs))

    return data

offset = 100                    # Days ago
ticker = 'EOSE'
end_date = pd.to_datetime('today')
start_date = end_date - pd.DateOffset(offset)  

historical_data = get_historical_data(ticker, start_date, end_date)

data_with_changes = calculate_changes(historical_data)

data_with_rsi = calculate_rsi(data_with_changes)

data_with_rsi['Next Daily Change'] = data_with_rsi['Daily Change'].shift(-1)

data_with_rsi = data_with_rsi[1:-1]

X_train, X_test, y_train, y_test = train_test_split(data_with_rsi.drop('Next Daily Change', axis=1), data_with_rsi['Next Daily Change'], test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)

print(y_pred)

mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae}')