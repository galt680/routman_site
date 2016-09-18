import talib as ta
import Quandl as q
import numpy as np
import sqlite3 as lite
from tech import Tech
from flask import render_template
import smtplib
import datetime

def spy_watchlist():
	today = datetime.date.today()
	alerts = []
	alert_messages = []
	con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
	cur = con.cursor()
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM SPY_DATA WHERE SIGNAL != 0 ORDER BY RSI DESC")
		rows = cur.fetchall()
		for row in rows:
			alerts.append(row)

	for i in alerts:
		print i
		print ''
	return render_template('spy_watchlist.html',alerts = alerts)
