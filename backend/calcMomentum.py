#calculates momentum of one stock
from datetime import *
import math

'''
takes in data as json object
returns volality as float using weekly adjusted prices for past 3 yrs
'''
def calcVolatility(data):
	currYear = datetime.today().year
	mean = 0.0
	prices = []
	returns = []
	variance = 0.0
	print(data)
	#get closing price for last 3 years with most recent price first
	for key in data["Weekly Adjusted Time Series"]:
		date = datetime.strptime(key, "%Y-%m-%d")
		if date.year < (currYear-3):
			break
		prices.append(float(data["Weekly Adjusted Time Series"][key]['5. adjusted close']))

	if len(prices) == 0:
		return None
	#calculate returns from week to week
	for i in range(len(prices)-1):
		change = (prices[i]-prices[i+1])/prices[i+1]
		mean+=change
		returns.append(change)
	
	mean = mean/len(returns)

	#calculate std deviation of returns
	for elem in returns:
		deviation = elem - mean
		variance +=math.pow(deviation,2)

	variance = variance/(len(returns)-1)
	return math.sqrt(variance)

'''
takes in data as json object, time period in months
returns tuple of two strings: 
(most recent available date in data, 
date with time period subtracted (inexact))
if cannot find a date in timePeriod then returns false
'''
def getDates(data, timePeriod):
	maxDate = datetime.min
	#if todays date not in database of prices.
	if datetime.today() not in data["Weekly Adjusted Time Series"]:
		for key in data["Weekly Adjusted Time Series"]:
		 	date = datetime.strptime(key, "%Y-%m-%d")
		 	if date > maxDate:
		 		maxDate = date
	else: maxDate = datetime.today()
	#finds estimate of previous date given subtracted time period
	prevDate = maxDate - timedelta(timePeriod*365/12)
	maxDate = datetime.strftime(maxDate, "%Y-%m-%d")
	count = 7
	#goes through data and finds date closest to estimate of previous date in the available data
	while datetime.strftime(prevDate, "%Y-%m-%d") not in data["Weekly Adjusted Time Series"]:
		prevDate = prevDate -timedelta(1)
		if count==0:
			return False,False
		count-=1
	prevDate = datetime.strftime(prevDate, "%Y-%m-%d")
	print(prevDate,maxDate)
	return maxDate,prevDate

'''
takes in data as json object, volatility/riskFreeRate as floats
and time period in months
returns momemtum as float
'''
def calcRiskAdjustedMomentum(data, volatility, riskFreeRate, timePeriod):
	maxDate, prevDate = getDates(data, timePeriod)
	if maxDate == False:
		return False
	currPrice = float(data["Weekly Adjusted Time Series"][maxDate]["5. adjusted close"])
	oldPrice = float(data["Weekly Adjusted Time Series"][prevDate]["5. adjusted close"])
	returns = (currPrice - oldPrice)/oldPrice
	return (returns-riskFreeRate)/volatility

'''
takes in data as json object, time period in months
returns momentum as float for that stock
if unable to calculate momentum returns false
'''
def calcMomentum(data,timePeriod):  
	riskFreeRate = 0.289            ####### store in SQL database later ########
	volatility = calcVolatility(data)
	if volatility == None:
		return False
	else:
		momentum = calcRiskAdjustedMomentum(data, volatility, riskFreeRate, timePeriod)
	return momentum
