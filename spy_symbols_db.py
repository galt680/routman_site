
import timeit

start = timeit.default_timer()
from tech import Tech
import finsymbols
sp500 = finsymbols.get_sp500_symbols()


dic = {}
for i in sp500:
	i = i['symbol']
	try:
		tech = Tech(i)
		dic[i] = {'signal':tech.signals(),
				  "RSI":tech.rsi(),
				  "Stochastic":tech.slow_stoch()}

	except:
		print "%s unsuccessful"%i

try:
	con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
except:
	con = lite.connect('ALERT_DATA.db')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS SPY_DATA")
cur.execute("CREATE TABLE SPY_DATA(NAME TEXT,SIGNAL INT,RSI INT,SLOWK INT,SLOWD INT)")
for i in dic:
	cur.execute("INSERT INTO SPY_DATA(NAME,SIGNAL,RSI,SLOWK,SLOWD) VALUES (?,?,?,?,?)",(i,dic[i]['signal'],dic[i]['RSI'],dic[i]['Stochastic'][0],dic[i]['Stochastic'][0]))
con.commit()

stop = timeit.default_timer()

print "Task took %s minutes"%((stop - start)/60)