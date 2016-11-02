import talib as ta
import quandl as q
import numpy as np
import sqlite3 as lite
import os.path
from tech import Tech
from flask import render_template

#symbols.py generates the data for watch_list.html


def symbol_alerts():
	#create empty lists to hold the data
	alerts = []
	rsi_overbought = []
	rsi_oversold = []
	#tests whether the program is running locally or in the cloud and connects to the appropriate sqlite database
	try:
		con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
	except:
		con = lite.connect('ALERT_DATA.db')


	with con:
		cur = con.cursor()

		#uses the cursor to get all data from db where the signal
		#-RSI above 60; both stochastics above 70-
		#isn't 0, if it's 1 it means oversold and if -1 its overbought
		#returns results to alerts list

		cur.execute("SELECT * FROM ALERT_DATA WHERE SIGNAL != 0 ORDER BY RSI DESC")
		for row in cur.fetchall():
			alerts.append(row)

		#uses cursor to get all where RSI is > 65 and returns to rsi_only listo
		cur.execute("SELECT * FROM ALERT_DATA WHERE RSI > 65 ORDER BY RSI DESC")
		rows = cur.fetchall()
		for row in rows:
		    print row
		    rsi_overbought.append(row)
		#uses cursor to get all where RSI is < 35 and returns to rsi_only list
		cur.execute("SELECT * FROM ALERT_DATA WHERE RSI < 35 ORDER BY RSI DESC")
		rows = cur.fetchall()
		for row in rows:
		    print row
		    rsi_oversold.append(row)

	for i in alerts:
		print i
		print ''
	return render_template('watch_list.html',alerts = alerts,rsi_overbought = rsi_overbought, rsi_oversold = rsi_oversold)