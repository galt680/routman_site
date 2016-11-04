import talib as ta
try:
    import quandl as q
except:
    import Quandl as q
import numpy as np
import sqlite3 as lite
from tech import Tech
from flask import render_template
import smtplib
import datetime
print 3
def spy_watchlist():
    today = datetime.date.today()
    alerts = []
    rsi_overbought = []
    rsi_oversold = []
    try:
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
    except:
        con = lite.connect('ALERT_DATA.db')
    cur = con.cursor()
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM SPY_DATA WHERE SIGNAL != 0 ORDER BY RSI DESC")
        for row in cur.fetchall():
            alerts.append(row)
        cur.execute("SELECT * FROM SPY_DATA WHERE RSI > 65 ORDER BY RSI DESC")
        for row in cur.fetchall():
            rsi_overbought.append(row)
        cur.execute("SELECT * FROM SPY_DATA WHERE RSI < 35 ORDER BY RSI ASC")
        for row in cur.fetchall():
            rsi_oversold.append(row)

    for i in alerts:
        print i
        print ''
    return render_template('spy_watchlist.html',alerts = alerts, rsi_overbought = rsi_overbought, rsi_oversold = rsi_oversold)
