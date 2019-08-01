from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from portfolio.callAPI import *
from portfolio.models import Stocks

@login_required(login_url="/login/")
def portfolio_view(request):
	stocks = []
	querySet = Stocks.objects.filter(selected=1)
	for obj in querySet:
		stocks.append(obj.ticker)
	stocks = ",".join(stocks)
	json_obj = callAPI('BATCH_QUOTES_US', stocks)
	for index in range(len(json_obj['Stock Batch Quotes'])):
		diff = float(json_obj['Stock Batch Quotes'][index]["5. price"]) - float(json_obj['Stock Batch Quotes'][index]["2. open"])
		json_obj['Stock Batch Quotes'][index]["9. difference"] = round(diff, 2)
	return render(request, 'portfolio/portfolio.html', {'data': json_obj["Stock Batch Quotes"]})

@login_required(login_url="/login/")
def about_view(request):
	return render(request, 'portfolio/about.html')

