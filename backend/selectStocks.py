import updateMomentumScores
import sqlite3
import requests
from bs4 import BeautifulSoup

'''
takes in the database cursor, # of stocks you want to select,
blackList of stocks
selects stock based on momentum score but gives stocks 
already owned priority to avoid excess turnover
updates SQL table with selected stocks, returns nothing
'''
def selectStocks(c, count, blackList):
	updateMomentumScores.updateMomentumScores()
	#selects count/2 number of stocks with highest momentum 
	c.execute('''SELECT ticker FROM stocks 
				 ORDER BY momentum DESC
			  ''')
	firstRows = c.fetchmany(int(count/2))
	c.execute('''SELECT ticker FROM stocks 
				 ORDER BY momentum DESC
			  ''')

	allRows = c.fetchall()
	#getting rid of stocks on blacklist
	for row in blackList:
		if row in firstRows:
			firstRows.remove(row)
		elif row in allRows:
			allRows.remove(row)
	#inserts/updates count/2 number of stocks into database with highest momentum
	c.executemany('UPDATE stocks SET selected=1 WHERE ticker=?', firstRows)
	#removes any stocks in selectedStocks (leftover from previous selections) that are not in top 150% of stocks
	for ticker in c.execute('SELECT ticker FROM stocks WHERE selected=1 ORDER by momentum DESC'):
		if ticker not in allRows:
			c.execute('UPDATE stocks SET selected=0 WHERE ticker=?', ticker)
	#if there are too many stocks selected, delete the ones with lowest momentum
	rowCount = c.execute('SELECT COUNT(*) FROM stocks WHERE selected=1').fetchone()[0]
	if rowCount > count:
		deleteAmt = rowCount - count
		deleteRows = []
		i = 1
		for ticker in c.execute('SELECT ticker FROM stocks WHERE selected=1 ORDER BY momentum DESC'):
			deleteRows.append(ticker)
			if i == deleteAmt:
				break
			i+=1
		c.executemany('UPDATE stocks SET selected=0 WHERE ticker=?', deleteRows)
		
	#if there are too few stocks selected, add more from list
	elif rowCount < count:
		addAmt = count - rowCount
		updates = []
		i = 0
		while addAmt > 0:
			c.execute('SELECT * from stocks WHERE selected=1 AND ticker=?',(allRows[i],))
			if c.fetchone() == None:
				updates.append((allRows[i],))
				addAmt-=1
			i+=1
		c.executemany('UPDATE stocks SET selected=1 WHERE ticker=?', updates)

'''
takes in text from web-scraped getMarketCap fxn
parses through it and converts it to millions or billions,
removes everything but numbers
returns int version of text
'''
def convertString(text):
	bn = False
	#checks if number in millions or billions
	if "bn" in text:
		bn = True
	#removes alphabet from number
	text=''.join(i for i in text if i.isdigit() or i==".")
	#converts number to integer in millions/billions 
	if bn:
		x = int(float(text) * 1000000000000)
	else:
		x = int(float(text) * 1000000)
	return x

'''
takes in cursor to database
web scrapes Financial Times
gets marketCap and freeFloat info for stocks in database
using webscraping and returns an array of two arrays 
of marketCaps, freeFloats
'''
def getMarketCapsAndFreeFloats(c):
	marketCaps = []
	freeFloats = []
	url = "https://markets.ft.com/data/equities/tearsheet/summary?s="
	for ticker in c.execute('SELECT ticker from selectedStocks ORDER by ticker'):
		r = requests.get(url + ticker[0])
		soup = BeautifulSoup(r.content, "html.parser")
		headerMarketCap = soup.find('th', text="Market cap")
		headerFreeFloat = soup.find('th', text="Free float")
		marketCap = headerMarketCap.find_next_sibling('td').text
		freeFloat = headerFreeFloat.find_next_sibling('td').text
		marketCaps.append(convertString(marketCap))
		freeFloats.append(convertString(freeFloat))
	return [marketCaps, freeFloats]

'''
takes in cursor, list of marketCaps, and list of freeFloats
return blackList of stocks based on which stocks have too high a weight
in selectedStocks from portfolio
'''
def createBlacklist(c, marketCaps, freeFloats):
	#figures out weight percentage of each stock in portfolio
	blackList = []
	weights = []
	total = 0
	i = 0

	#calculating weight of each stock by momentumScore*marketCap*freeFloat
	for row in c.execute('SELECT * FROM stocks ORDER BY ticker'):
		weight = row[2]*marketCaps[i]*freeFloats[i]
		weights.append((row[0], weight))
		total+=weight
		i+=1

	#getting weight percentages
	for i in range(len(weights)):
		weightPer = weights[i][1]/total * 100
		#if weight percentage too large then add stock to blackList
		if weightPer > 5:
			blackList.append(weights[i][0])
	return blackList

'''
takes in number of stocks in selection, list of market cap values & list 
of freeFloat values
updates selected stocks according to weights 
'''
def weightStocks(count):
	#opens connection to database, selects count number of stocks
	conn = sqlite3.connect("../mysite/db.sqlite3")
	conn.text_factory = str #treat TEXT like strings and vice versa
	c = conn.cursor()
	blackList = []
	#makes prelim list of selected stocks, puts some on blacklist if have too high 
	#a weight in portfolio
	selectStocks(c, count, blackList)
	marketCaps, freeFloats = getMarketCapsAndFreeFloats(c)
	blackList = createBlacklist(c, marketCaps, freeFloats)
	
	#delete blackList stocks from portfolio and reselect stocks
	c.executemany('UPDATE stocks SET selected=0 WHERE ticker=?', [x[0] for x in blackList])
	selectStocks(c, count, blackList)

	conn.commit()
	conn.close()

weightStocks(20)