from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from portfolio.models import Stocks
from stocks.callAPI import *
from datetime import *
import pygal
from pygal.style import CleanStyle

'''
view for stocks page
default stock is apple
'''
@login_required(login_url="/login/")
def stocks_view(request, ticker='AAPL'):

	if request.method == "POST":
		ticker = request.POST.get('tickerInput')
		api_obj = callAPI('TIME_SERIES_DAILY', ticker)
		print(api_obj)
		if 'Time Series (Daily)' not in api_obj:
			return redirect('stocks:error')
		else:
			return redirect("http://localhost:8000/stocks/"+ticker)
	#gets data for stock (default is apple)
	api_obj = callAPI('TIME_SERIES_DAILY', ticker)
	data = api_obj['Time Series (Daily)']

	#puts data in order so that chart will be correct
	orderedData = []
	for key in data:
		orderedData.append([datetime.strptime(key, "%Y-%m-%d"), data[key]['1. open']])
	orderedData = sorted(orderedData, key=lambda x: x[0])
	for elem in orderedData:
		elem[0] = datetime.strftime(elem[0], "%Y-%m-%d")

	#passing in name and other data into html form
	query = dict()
	querySet = Stocks.objects.filter(ticker=ticker)
	query['ticker'] = querySet[0].ticker
	query['name'] = querySet[0].name
	query['momentum'] = querySet[0].momentum
	query['price'] = orderedData[-1][1]
	query['difference'] = round(float(orderedData[-1][1]) - float(orderedData[-2][1]), 2)

	#line chart displaying prices for selected stock
	chart = pygal.Line(style=CleanStyle,
					   x_label_rotation=20,
					   show_minor_x_labels=False)
	dateList = [x[0] for x in orderedData]
	n = 10
	chart.x_labels = dateList
	chart.x_labels_major = dateList[::n]
	chart.add('price', [float(x[1]) for x in orderedData])
	chart.render_to_file('stocks/static/chart.svg')

	return render(request, 'stocks/stocks.html', {'query':query})


def error_view(request):
	return render(request, 'stocks/error.html')
