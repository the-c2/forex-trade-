import alpaca_trade_api as tradeapi
import time

# Replace with your Alpaca API keys
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
BASE_URL = 'https://paper-api.alpaca.markets'

# Initialize API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Trading parameters
symbol = 'AAPL'
buy_threshold = 170.00
sell_threshold = 180.00
quantity = 1

def get_price(symbol):
    barset = api.get_latest_trade(symbol)
    return barset.price

def place_order(symbol, qty, side):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type='market',
        time_in_force='gtc'
    )
    print(f"{side.capitalize()} order placed for {qty} shares of {symbol}")

# Main loop
while True:
    try:
        price = get_price(symbol)
        print(f"Current price of {symbol}: ${price}")

        position = api.get_position(symbol) if symbol in [p.symbol for p in api.list_positions()] else None

        if price <= buy_threshold and not position:
            place_order(symbol, quantity, 'buy')
        elif price >= sell_threshold and position:
            place_order(symbol, quantity, 'sell')

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(60)  # Check every minute
    