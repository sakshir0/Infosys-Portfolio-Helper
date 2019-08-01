import json
import requests
from portfolio.models import Stocks
#for alpha vantage API

def readAPIKey(filepath):
	with open("../backend/APIKey.txt", 'r') as f:
		return f.read().replace("\n","")
	f.close()

def callAPI(function, symbols):
	apiKey = readAPIKey("APIKey.txt")
	param = {"function": function, "symbols": symbols, "apikey": apiKey}
	response = requests.get(url='https://www.alphavantage.co/query?', params=param)
	data = json.loads(response.text)
	return data


