import yfinance as yf
import pandas as pd

def get_historical_data(ticker, start_date, end_date):
    # Download historical data from Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def calculate_changes(data):
    # Calculate price change
    data['Price Change'] = data['Close'] - data['Open']

    # Calculate volume change
    data['Volume Change'] = data['Volume'].pct_change()

    return data

def calculate_rsi(data, window=14):
    # Calculate daily price changes
    data['Daily Change'] = data['Close'].diff()

    # Calculate average gain and average loss over the specified window
    data['Gain'] = data['Daily Change'].apply(lambda x: x if x > 0 else 0)
    data['Loss'] = data['Daily Change'].apply(lambda x: -x if x < 0 else 0)

    avg_gain = data['Gain'].rolling(window=window, min_periods=1).mean()
    avg_loss = data['Loss'].rolling(window=window, min_periods=1).mean()

    # Calculate relative strength (RS)
    rs = avg_gain / avg_loss

    # Calculate RSI
    data['RSI'] = 100 - (100 / (1 + rs))

    return data


# Define the ticker symbol and date range
ticker = 'EOSE'
end_date = pd.to_datetime('today')
start_date = end_date - pd.DateOffset(7)  # 7 days ago

# Get historical data
historical_data = get_historical_data(ticker, start_date, end_date)

# Calculate changes
data_with_changes = calculate_changes(historical_data)

# Calculate RSI
data_with_rsi = calculate_rsi(data_with_changes)

print(data_with_rsi)

# Display the result
# print(data_with_rsi[['Close', 'RSI']])
