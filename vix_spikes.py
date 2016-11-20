from flask import Flask,request,render_template
import pandas as pd
import sqlite3 as lite


	
def vix_decider():
	try:
		con = lite.connect('/home/yaschaffel/mysite/IMP_VOL_TABLE.db')
	except:
		con = lite.connect('IMP_VOL_TABLE.db')
	cur = con.cursor()
	cur.execute("select count(*)from HISTORICAL_VOL where NAME = 'AAPL'")
	length = cur.fetchall()[0][0]-2 
	
	return render_template('vix_decider.html',length = length)
	
	
def vix_spikes_page():
	thresh = int(request.form['threshold'])
	days = int(request.form['days'])
	
	print days,thresh
	
	try:
		con = lite.connect('/home/yaschaffel/mysite/IMP_VOL_TABLE.db')
	except:
		con = lite.connect('IMP_VOL_TABLE.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM HISTORICAL_VOL order by DAY DESC")
	dict = {}

	for i in cur.fetchall():
		if str(i[1]) not in dict:
			dict[str(i[1])] = ([i[2]])
		else:
			if len(dict[str(i[1])]) < days:
				dict[str(i[1])].append((i[2]))
			else:
				pass
	for i in dict:
		dict[i] = pd.Series(dict[i])
	
	def signal():
		def get_percent(symbol):
			symbol = symbol.upper()
			return round(100*dict[symbol].iloc[::-1].pct_change(periods = (days-1))[0],2)
		def checker():
			spiked = []
			for i in dict:
				if get_percent(i) > thresh:
					spiked.append([i,get_percent(i)])
				else:
					pass
			return spiked
		return checker()


	spiked = signal()
	print spiked
	print len(dict['UA.C'])
	return render_template('imp_spikes.html',spiked = spiked, days = days)
