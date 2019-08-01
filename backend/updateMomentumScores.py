import useAPI
import calcMomentum
from scipy import stats
import sqlite3
import time


'''
takes in cursor, timePeriod for momentum values in months
returns list of tuples (ticker(str), momentum(float))
'''
def getAllMomentums(c, timePeriod):
	momentums = []
	for row in c.execute('SELECT * FROM stocks order BY ticker'):
		data = useAPI.callAPI("TIME_SERIES_WEEKLY_ADJUSTED", row[0])
		if data == None:
			print('data retrieval error') 
			time.sleep(20)
			continue
		else:
			momentum = calcMomentum.calcMomentum(data, timePeriod)
		if momentum == False:
			print('momentum date error')
			time.sleep(20)
			continue
		else:
			time.sleep(20)
			momentums.append(calcMomentum.calcMomentum(data, timePeriod))
		  #free version of API only allows 5 calls/minute so must throttle speed
	return momentums

'''
takes in lists of six, twelve month momentums
returns list of momentum scores
'''
def calcMomentumScores(momentumsSix, momentumsTwelve):
	momentumScores = []
	zScoresSix = stats.zscore(momentumsSix)
	zScoresTwelve = stats.zscore(momentumsTwelve)

	#momentum_z = average of z-score for six/twelve month momentum
	for i in range(len(zScoresSix)):
		momentumZ = (zScoresSix[i] + zScoresTwelve[i])/2
		#winsorizes mom_z at +/- 3
		if momentumZ > 3:
			momentumZ = 3.0
		elif momentumZ < -3:
			momentumZ = -3.0 
		'''momentum score = 1 + momentum_Z     x>0 
						   (1-momentum_z)^-1   x<0 ''' 
		if momentumZ>0:
			momentumScore = 1 + momentumZ
		else:
			momentumScore = (1-momentumZ)**-1
		momentumScores.append(momentumScore)
	return momentumScores

'''
takes in cursor for database and list of momentum z-scores
does not return anything, updates SQL database
'''
def updateMomentumDatabase(c, momentumScores):
	count = 0
	updates = []
	#updates temporary table with ticker and calculated momentum
	for row in c.execute('SELECT * FROM stocks order BY ticker'):
		updates.append((row[0], momentumScores[count]))
		if count == len(momentumScores)-1:
			break
		count+=1
	c.executemany('INSERT INTO updates VALUES (?, ?)', updates)
	#updates momentum values using temporary table
	c.execute('''UPDATE stocks 
					SET momentum = (SELECT momentum 
									FROM updates 
									WHERE ticker = stocks.ticker)
					WHERE EXISTS   (SELECT momentum 
									FROM updates 
									WHERE ticker = stocks.ticker)
			 ''', )


def updateMomentumScores():
	#create database connection and temporary table to hold momentums 
	conn = sqlite3.connect("../mysite/db.sqlite3")
	conn.text_factory = str #treat TEXT like strings and vice versa
	c = conn.cursor()
	c.execute('''CREATE TEMPORARY TABLE updates
                (ticker TEXT PRIMARY KEY,
                 momentum REAL)
                 ''')
	momentumsSix = getAllMomentums(c, 6)
	momentumsTwelve = getAllMomentums(c, 12)
	momentumScores = calcMomentumScores(momentumsSix, momentumsTwelve)
	updateMomentumDatabase(c, momentumScores)
	#deletes temporary table
	c.execute('DROP table updates')

	conn.commit()
	conn.close()

updateMomentumScores()