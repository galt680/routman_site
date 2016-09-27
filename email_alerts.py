import sqlite3 as lite
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import datetime
from passwords import pswd


def send_alert():
	today = datetime.date.today()
	alert_overbought = []
	alert_oversold = []
	rsi_only = []
	con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')#/home/yaschaffel/mysite/ALERT_DATA.db
	cur = con.cursor()
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM ALERT_DATA WHERE SIGNAL != 0 ORDER BY Name Asc")
		rows = cur.fetchall()
		for name,signal,rsi,slowk,slowd in rows:
			if signal == -1:
				alert_overbought.append("%s is overbought with RSI at %s and the stochastics at %s and at %s"%(name,rsi,slowk,slowd))
			else:
				pass
		for name,signal,rsi,slowk,slowd in rows:
			if signal == 1:
				alert_oversold.append("%s is oversold with RSI at %s and the stochastics at %s and at %s"%(name,rsi,slowk,slowd))
			else:
				pass
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM ALERT_DATA WHERE RSI > 65 ORDER BY RSI DESC")
		rows = cur.fetchall()
        for name,signal,rsi,slowk,slowd in rows:
            rsi_only.append("%s is overbought with RSI at %s"%(name,rsi))
	if len(alert_oversold) <= len(alert_overbought):
		message = """Good evening,\n(This is an automated message)\n\nThese are the stocks that are currently overbought from your watchlist:\n"""
		for i in alert_overbought:
			message +='\n %s'%i
		message +="""\n\nThese are the stocks that are currently oversold from your watchlist:\n"""
		for i in alert_oversold:
			message += '\n %s'%i
		message +="""\n\nThese are the stocks that are currently overbought based only on RSI from your watchlist:\n"""
		for i in rsi_only:
			message += '\n %s'%i
		message += "\n\n If you have any adjustments you'd like to make to the alert settings or if you'd like to add symbols to the watchlist please let me know.\nYisroel Schaffel"

	else:
		message = """Good evening,\n(This is an automated message)\n\nThese are the stocks that are currently oversold from your watchlist:\n"""
		for i in alert_oversold:
			message +='\n %s'%i
		message +="""\n\nThese are the stockst that are currently overbought from your watchlist:\n"""
		for i in alert_overbought:
			message += '\n %s'%i
		message +="""\n\nThese are the stocks that are currently overbought based only on RSI from your watchlist:\n"""
		for i in rsi_only:
			message += '\n %s'%i
		message += "\n\n If you have any adjustments you'd like to make to the alert settings or if you'd like to add symbols to the watchlist please let me know.\nYisroel Schaffel"

	fromaddr = "routmanapp@gmail.com"
	toaddr = "aronroutman@sbcglobal.net" ##
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Alerts for %s"%today.strftime("%m-%d-%Y")


	body = message
	print body
	msg.attach(MIMEText(body, 'plain'))


	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("routmanapp@gmail.com", pswd)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	print "Email sent!"
send_alert()