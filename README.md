# Option-Chain-Assessment

This project provides a Python-based solution for obtaining option chain data and calculating margin requirements and premiums using the Upstox API. <br />This script demonstrates how to authenticate with Upstox, retrieve option chain data, and perform calculations on the data. The project is divided into three main steps, explained below.<br />

# Prerequisites
- Upstox Account and API Credentials: Create an account on Upstox (or any supported trading platform) and set up an API application to obtain the client_id, client_secret, and access token.<br />
- Python Packages:<br />
* requests: For making API requests.<br />
pandas: For data manipulation.<br />
Install dependencies using pip install requests pandas.<br />

# Steps<br />
Step 1: Obtain Access Token<br />
To access the Upstox API, you need to authenticate and retrieve an access token. Replace the placeholders in the code with your own client_id, client_secret, code, and redirect_uri.
