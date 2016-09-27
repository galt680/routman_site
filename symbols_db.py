import sqlite3 as lite
from tech import Tech
import timeit
	

symbols = [
		'AAL','AAPL','ABT','ABBV','ABX','ACAD','ADBE','ADP','AET','AGO','ALL','AMAT','AMD','AMGN','APA','AXP','BA','BAC','BAX','BCLYF',
		'BHI','BMY','BP','C','CAR','CBI','CELG','CMCSA','CNI','COP', 'CREE','CSCO','CREE','CTL','CLX','CTSH','CVS','CVX','DFS','DIS',
		'DO','DTV','DVN','ESRX','EXAS','F','FB','FCX','FITB','FLR','GE','GILD','GLW','GS','L_GSK','HAL','HP','HPQ','IBM','INTC','INTU',
		'JNJ','JPM','KEY','NYSE_KKR','KR','KRFT','KSU','L','LLY','LNKD','LOW','MCK','MET','MDT','MMM','MON','MRK','MSFT','MUR','MYL','NBL',
		'NE','NFX','NTRS','NVSEF','ORCL','OXY','P','PE','PEP','PFE','PG','PLUG','PM','PNC','PSX','PXD','QCOM','RRC','SCHW','STLD','STT',
		'T','TA_TEVA','TRV','TSO','TWTR','TXN','TYC','UBS','UNGS','UNH','URI','USB','UTX','VRX','VZ','WFC','X','YHOO','XOM','GOOG','JPM',
		'PCLN',
	]

dic = {}
for i in symbols:
	try:
		tech = Tech(i,time = "daily")
		dic[i] = {'signal':tech.signals(),
				  "RSI":tech.rsi(),
				  "Stochastic":tech.slow_stoch()}
		print "%s successful"%i
	except Exception as e:
		print e
		print "%s unsuccessful"%i
try:
	con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
except:
	con = lite.connect('ALERT_DATA.db')
print con
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS ALERT_DATA")
cur.execute("CREATE TABLE ALERT_DATA(NAME TEXT,SIGNAL INT,RSI INT,SLOWK INT,SLOWD INT)")
for i in dic:
	cur.execute("INSERT INTO ALERT_DATA(NAME,SIGNAL,RSI,SLOWK,SLOWD) VALUES (?,?,?,?,?)",(i,dic[i]['signal'],dic[i]['RSI'],dic[i]['Stochastic'][0],dic[i]['Stochastic'][0]))
con.commit()
stop = timeit.default_timer()
try:
	print "Task took %s minutes"%(int(stop - start)/60)
except:
	pass

	
	
# dic = {}
# for i in sp500:
	# i = i['symbol']
	# url = "http://www.ivolatility.com/options.j?ticker=%s&R=0&top_lookup__is__sent=1"%i
	# try:
		# driver.get(url)
		# current = float(driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/table[1]/tbody/tr[3]/td[1]/table[2]/tbody/tr[9]/td[2]/font").text.strip('%'))
		# dic[i] = {'Current Implied Volatility':current,}
		# time.sleep(uniform(2,5.5))
	# except:
		# print "%s unsuccessful"%i
