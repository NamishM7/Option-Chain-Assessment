# step-1.1: obtaining the option chain data (login and authorization)

# create an account in any of the trading platforms and get the access token (for eg., I have used upstox)
# then create an app in the platform and get the client id and client secret
# then use the below code to get the access token

import requests
url = 'https://api.upstox.com/v2/login/authorization/token'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = {
    'code': 'mDwsFV',  # Replace with your code
    'client_id': 'c24820ce-2045-4aa4-96fb-f27cf2347435', # Replace with your client id
    'client_secret': 'sqkwgdx9cv', # Replace with your client secret
    'redirect_uri': 'https://www.google.com/',  # Replace with your redirect uri
    'grant_type': 'authorization_code'
}
response = requests.post(url, headers=headers, data=data)
access_token = response.json().get('access_token')
print("Access Token:", access_token)

#example access token: eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiIySENOVDciLCJqdGkiOiI2NzI4NzVmNWNhZjc2ZDUzNzg0YzVmZTEiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzMwNzA0ODg1LCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzA3NTc2MDB9.dvsuVgETqm336-xBKWgD6N1fPc1fiqSqUBdVvKkgXJ4

# the above provides us with the access token after authentication


# step-1.2: getting the response data using the access token

import requests
url = 'https://api.upstox.com/v2/option/chain'
params = {
    'instrument_key': 'NSE_INDEX|Nifty 50',
    'expiry_date': '2024-03-28'
}
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {access_token}'
    # replace with your access token
}
response = requests.get(url, params=params, headers=headers)
print(response.json()) #prints the response data

# Here is a sample output of the response data:
response_json = {
  "status": "success",
  "data": [
    {
      "expiry": "2024-02-15",
      "pcr": 1684.0638,
      "strike_price": 19500,
      "underlying_key": "NSE_INDEX|Nifty 50",
      "underlying_spot_price": 22122.25,
      "call_options": {
        "instrument_key": "NSE_FO|37263",
        "market_data": {
          "ltp": 2291.8,
          "close_price": 2259.9,
          "volume": 1200,
          "oi": 2350,
          "bid_price": 2292.85,
          "bid_qty": 50,
          "ask_price": 2302.25,
          "ask_qty": 800,
          "prev_oi": 0
        },
        "option_greeks": {
          "vega": 0,
          "theta": 0,
          "gamma": 0,
          "delta": 1,
          "iv": 0
        }
      },
      "put_options": {
        "instrument_key": "NSE_FO|37264",
        "market_data": {
          "ltp": 0.7,
          "close_price": 1.5,
          "volume": 12367100,
          "oi": 3957550,
          "bid_price": 0.65,
          "bid_qty": 382600,
          "ask_price": 0.7,
          "ask_qty": 88300,
          "prev_oi": 14400
        },
        "option_greeks": {
          "vega": 0.2278,
          "theta": -0.5966,
          "gamma": 0,
          "delta": -0.0026,
          "iv": 31.43
        }
      }
    }
  ]
}

# step-2: creating a function to extract the option chain data
# function 1

import pandas as pd
def get_option_chain_data(response_json):
    options_data = []
    
    # Loop through each option entry in the response
    for option in response_json['data']:
        instrument_name = option['call_options']['instrument_key']
        strike_price = option['strike_price']
        
        # Get the highest ask price for call options (CE)
        call_ask_price = option['call_options']['market_data']['ask_price']
        
        # Get the highest bid price for put options (PE)
        put_bid_price = option['put_options']['market_data']['bid_price']
        
        # Append extracted data to the list
        options_data.append({
            'instrument_name': instrument_name,
            'strike_price': strike_price,
            'call_ask_price': call_ask_price,
            'put_bid_price': put_bid_price
        })
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(options_data)
    return df


df_option_chain = get_option_chain_data(response_json)
print(df_option_chain)


# step-3: Retrieves the margin requirement 
# Calculates the premium earned by multiplying the bid/ask price by the lot size for each contract

# function 2
import requests
import pandas as pd

def calculate_margin_and_premium(data: pd.DataFrame, lot_size=75) -> pd.DataFrame:
    # Assuming margin API endpoint exists at Upstox (replace with actual if available)
    margin_api_url = "https://api.upstox.com/v2/margin/calculate"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'  # Replace with your access token
    }
    
    # Define a function to get margin requirement from the API
    def get_margin(strike_price, side):
        params = {
            'strike_price': strike_price,
            'transaction_type': 'Sell',
            'option_type': side
        }
        response = requests.get(margin_api_url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get('margin', 0)
        else:
            return 0  # Default to 0 if API call fails

    # Add margin_required and premium_earned columns
    data['margin_required'] = data.apply(lambda x: get_margin(x['strike_price'], x['side']), axis=1)
    data['premium_earned'] = data['bid/ask'] * lot_size  # Calculate premium based on bid/ask price and lot size

    return data

# Example usage:
# Assuming df_option_chain is the DataFrame returned by get_option_chain_data
df_option_chain = pd.DataFrame({
    'instrument_name': ['NSE_INDEX|Nifty 50'],
    'strike_price': [19500],
    'side': ['CE'],
    'bid/ask': [2302.25]
})

df_final = calculate_margin_and_premium(df_option_chain)
print(df_final)