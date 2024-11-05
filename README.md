# Option-Chain-Assessment

This project provides a Python-based solution for obtaining option chain data and calculating margin requirements and premiums using the Upstox API. <br />This script demonstrates how to authenticate with Upstox, retrieve option chain data, and perform calculations on the data. The project is divided into three main steps, explained below.<br />

## Prerequisites
 Upstox Account and API Credentials: Create an account on Upstox (or any supported trading platform) and set up an API application to obtain the client_id, client_secret, and access token.<br /><br />
 Python Packages:<br />
* requests: For making API requests.<br />
* pandas: For data manipulation.<br />
* Install dependencies using pip install requests pandas.<br />

## Steps<br />
* Step 1: Obtain Access Token<br />
To access the Upstox API, you need to authenticate and retrieve an access token. Replace the placeholders in the code with your own client_id, client_secret, code, and redirect_uri.
```
import requests

url = 'https://api.upstox.com/v2/login/authorization/token'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = {
    'code': 'YOUR_CODE',
    'client_id': 'YOUR_CLIENT_ID',
    'client_secret': 'YOUR_CLIENT_SECRET',
    'redirect_uri': 'YOUR_REDIRECT_URI',
    'grant_type': 'authorization_code'
}

response = requests.post(url, headers=headers, data=data)
access_token = response.json().get('access_token')
print("Access Token:", access_token)
```
<br />This code returns an access token after successful authentication.<br /><br />
* Step 2: Retrieve Option Chain Data<br />
Using the access token, we retrieve the option chain data for a specified instrument and expiry date. Replace access_token and any parameters as necessary.<br />
```
import requests

url = 'https://api.upstox.com/v2/option/chain'
params = {
    'instrument_key': 'NSE_INDEX|Nifty 50',
    'expiry_date': '2024-03-28'
}
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

response = requests.get(url, params=params, headers=headers)
print(response.json())
```

