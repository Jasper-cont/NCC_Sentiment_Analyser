import yfinance as yf
import pandas as pd
import numpy as np

def calculate_put_call_ratio(options_data, options):
    
    temp_data = {
        'expirationDate' : [],
        'p c ratio': []
    }

    for expiry_date in options:
        temp_data['expirationDate'].append(expiry_date)
        puts_vol = options_data[(options_data['expirationDate'] == expiry_date) & (options_data['optionType'] == 'puts')]['volume'].sum()
        calls_vol = options_data[(options_data['expirationDate'] == expiry_date) & (options_data['optionType'] == 'calls')]['volume'].sum()

        if calls_vol > 0:
            temp_data['p c ratio'].append( puts_vol / calls_vol )
        else:
            temp_data['p c ratio'].append( 0 )

    p_c_r_data = pd.DataFrame(temp_data)
    return p_c_r_data


# def calculate_open_interest(options_data, options):
    temp_data = {
        'expirationDate' : [],
        'open interest': []
    }

    for expiry_date in options:
        temp_data['expirationDate'].append(expiry_date)
        open_interest = options_data[(options_data['expirationDate'] == expiry_date)]['openInterest'].sum()
        temp_data['open interest'].append( open_interest )

    open_interest_data = pd.DataFrame(temp_data)

    return open_interest_data

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

    calls['expirationDate'] = expiration_date
    calls['optionType'] = 'calls'
    puts['expirationDate'] = expiration_date
    puts['optionType'] = 'puts'

    # print(calls.head())
    # print(puts.head())

    options_data = pd.concat([options_data, calls], ignore_index=True)
    options_data = pd.concat([options_data, puts], ignore_index=True)

print(options_data.head())

put_call_ratio_data = calculate_put_call_ratio(options_data, options)

print(put_call_ratio_data)

# open_interest = calculate_open_interest(options_data, options)
open_interest = options_data.groupby('expirationDate')['openInterest'].sum().reset_index()

print(open_interest)

average_iv_by_date = options_data.groupby('expirationDate')['impliedVolatility'].mean().reset_index()

print(average_iv_by_date)