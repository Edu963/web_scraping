
from polygon import RESTClient
client = RESTClient(api_key ="ZYebyBIQG_Rmc4KZBPZ64SN0gOo1ylju")

ticker = "AAPL"
aggs = []
a = client.get_ticker_details(ticker=ticker)
aggs.append(a)

print(aggs)
print (a.market_cap)