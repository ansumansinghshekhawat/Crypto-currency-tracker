import streamlit as st
import requests

# Set page title
st.set_page_config(page_title="Crypto Tracker", page_icon="💰")

st.title("Real-Time Crypto Tracker")
st.write("This app fetches live prices from the CoinGecko API.")

# 1. Create a dropdown for the user to choose a coin
option = st.selectbox(
    'Which coin do you want to check?',
    ('bitcoin', 'ethereum', 'dogecoin', 'solana', 'cardano'))

# 2. Function to fetch data
def get_data(coin):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return data[coin]['usd']
    except Exception as e:
        return "Error fetching data"

# 3. Display the data when a button is clicked
if st.button('Get Latest Price'):
    price = get_data(option)
    if isinstance(price, float) or isinstance(price, int):
        st.metric(label=f"Current Price of {option.upper()}", value=f"${price:,}")
        st.success("Data updated successfully!")
    else:
        st.error("Could not retrieve price. Please try again later.")

st.divider()
st.info("Note: This data is provided by the free CoinGecko API.")


import pandas as pd

def get_historical_data(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=7&interval=daily"
    response = requests.get(url)
    data = response.json()
    prices = data['prices']
    
    # Convert list of lists into a DataFrame
    df = pd.DataFrame(prices, columns=['time', 'price'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    return df

st.subheader(f"{option.capitalize()} Price Trend (Last 7 Days)")
history_df = get_historical_data(option)
st.line_chart(history_df.set_index('time'))

# Move the selection to a sidebar
st.sidebar.header("Dashboard Settings")
option = st.sidebar.selectbox(
    'Which coin do you want to check?',
    ('bitcoin', 'ethereum', 'dogecoin', 'solana', 'cardano'))

currency = st.sidebar.selectbox('Select Currency', ('usd', 'inr', 'eur'))

def get_data(coin, curr):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={curr}"
    # ... rest of your logic, just replace 'usd' with curr ...

