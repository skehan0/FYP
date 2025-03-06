# import requests

# # Search symbol
# async def fetch_symbol(str: keyword):    
#     url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&symbol={ticker}&apikey={API_KEY}"
#     r = requests.get(url)
#     data = r.json()
#     print(data)


# # Global Market Open and Close Status
# async def fetch_market_status(): 
#     url = f"https://www.alphavantage.co/query?function=MARKET_STATUS&symbol={ticker}&apikey={API_KEY}"
#     r = requests.get(url)
#     data = r.json()
#     print(data)