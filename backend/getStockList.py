#get list of all Russell 3000 companies & indexes, 
#creates my SQl databse, puts companies into mySQL database
import PyPDF2
import sqlite3

'''
takes in pdf file path string
returns a list of company and tickers
'''
def parsePDF(pdf):
	pdfFileObject = open(pdf, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
	count = pdfReader.numPages
	text = ""

	#gets all pages from pdf and turns into one string with companies and tickers
	for i in range(count-1):
		page = pdfReader.getPage(i)
		page = page.extractText()
		text = text + page

	#remove all extraneous information from pdf and splits into list
	#with company first and ticker for that company second
	text = text.replace("Company","")
	text = text.replace("Ticker", "")
	text = text.replace("Membership list", "")
	text = text.replace("Russell US Indexes", "")
	text = text.replace("ftserussell.com", "")
	text = text.replace("June 25, 2018", "")  #update each year
	text = text.split("\n")

	#remove all whitespace
	for i in range(len(text)):
		text[i] = text[i].strip()

	#get rid of empty elements or elements with page numbers
	i = 0
	while i < len(text):
		if (text[i] == "") or text[i].isdigit():
			text.remove(text[i])
			i-=1
		i+=1
	pdfFileObject.close()
	return text

'''
loads stock list with primary key as ticker and name of company
returns database
'''
def loadDataIntoDatabase(conn, data):
	c = conn.cursor()
	stocks = []
	for i in range(0, len(data)-1, 2):
		t = (data[i+1], data[i])
		stocks.append(t)
	c.executemany('INSERT OR IGNORE INTO stocks (ticker, name) VALUES (?, ?)', stocks)
	return c

#main function, returns database
def getStockList():
	pdf = "russell3000MembershipList.pdf" #file path to pdf, pdf must be updated once a year
	data = parsePDF(pdf)
	conn = sqlite3.connect("../mysite/db.sqlite3") 
	conn.text_factory = str #treat TEXT like strings and vice versa
	loadDataIntoDatabase(conn, data)
	conn.commit()
	conn.close()

