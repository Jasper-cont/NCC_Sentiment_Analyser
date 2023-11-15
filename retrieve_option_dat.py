import yfinance as yf
import pandas as pd
import numpy as np

# Define the ticker symbol of the stock
ticker_symbol = 'EOSE'

# Create a Yahoo Finance stock object
stock = yf.Ticker(ticker_symbol)

# Get the options chain for the stock (you may specify expiration and strike parameters)
options = stock.options

# Print the option chain
print("Options Expiration Dates:")
print(options)

options_data = pd.DataFrame()

for expiration_date in options:
    opt = stock.option_chain(expiration_date)
    calls = opt.calls
    puts = opt.puts

    calls['ExpirationDate'] = expiration_date
    puts['ExpirationDate'] = expiration_date

    # print(calls.head())
    # print(puts.head())

    options_data = options_data.append(calls, ignore_index=True)
    options_data = options_data.append(puts, ignore_index=True)

print(options_data.head())