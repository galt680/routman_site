import talib as ta
import Quandl as q
import numpy as np
import sqlite3 as lite
from tech import Tech
from flask import render_template
import os.path


def symbol_alerts():
	alerts = []
	try:
		con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
	except:
		con = lite.connect('ALERT_DATA.db')
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM ALERT_DATA WHERE SIGNAL != 0 ORDER BY RSI DESC")
		rows = cur.fetchall()
		for row in rows:
			alerts.append(row)

	for i in alerts:
		print i
		print ''
	return render_template('watch_list.html',alerts = alerts)