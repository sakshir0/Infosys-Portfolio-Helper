import json
import requests
#for alpha vantage API

def readAPIKey(filepath):
	with open("../backend/APIKey.txt", 'r') as f:
		return f.read().replace("\n","")
	f.close()

def callAPI(function, symbol):
	apiKey = readAPIKey("APIKey.txt")
	param = {"function": function, "symbol": symbol, "apikey": apiKey}
	response = requests.get(url='https://www.alphavantage.co/query?', params=param)
	data = json.loads(response.text)
	return data


