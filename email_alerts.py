import sqlite3 as lite
import smtplib
try:
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
except:
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
import datetime
from passwords import pswd

'''def send_watchlist(test = False):
    today = datetime.date.today()
    alert_overbought = []
    alert_oversold = []
    rsi_overbought = []
    rsi_oversold = []
    try:
        print (1)
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
        print (1)
    except:
        print (2)
        con = lite.connect('ALERT_DATA.db')
        print (2)
    cur = con.cursor()
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM ALERT_DATA WHERE SIGNAL != 0 ORDER BY Name Asc")
        rows = cur.fetchall()
        for name,signal,rsi,slowk,slowd in rows:
            if signal == -1:
                alert_overbought.append("%s is overbought with RSI at %s and the stochastics at %s and at %s"%(name,rsi,slowk,slowd))
            elif signal == 1:
                alert_oversold.append("%s is oversold with RSI at %s and the stochastics at %s and at %s"%(name,rsi,slowk,slowd))
            else:
                pass

        cur.execute("SELECT * FROM ALERT_DATA WHERE RSI NOT BETWEEN 35 AND 65 ORDER BY RSI DESC")
        rows = cur.fetchall()
        for name,signal,rsi,slowk,slowd in rows:
            if rsi > 65:
                rsi_overbought.append("%s is overbought with RSI at %s"%(name,rsi))
            elif rsi < 35:
                rsi_oversold.append("%s is oversold with RSI at %s"%(name,rsi))
            else:
                pass

    message = """Good evening,\n(This is an automated message)\n\nThese are the stocks that are currently overbought and oversold from your watchlist:\n"""
    for i in alert_overbought:
        message +='\n %s'%i
    message +="""\n\nThese are the stocks that are currently oversold from your watchlist:\n"""
    for i in alert_oversold:
        message += '\n %s'%i
    message +="""\n\nThese are the stocks that are currently overbought based only on RSI from your watchlist:\n"""
    for i in rsi_overbought:
        message += '\n %s'%i
    message +="""\n\nThese are the stocks that are currently oversold based only on RSI from your watchlist:\n"""
    for i in rsi_oversold:
        message += '\n %s'%i
    message += "\n\n If you have any adjustments you'd like to make to the alert settings or if you'd like to add symbols to the watchlist please let me know.\nYisroel Schaffel"



    fromaddr = "routmanapp@gmail.com"
    toaddr = "aronroutman@sbcglobal.net" ##
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Watchlist Alerts for %s"%today.strftime("%m-%d-%Y")


    body = message
    print (body)
    if test == True:
        pass
    else:
        msg.attach(MIMEText(body, 'plain'))


        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("routmanapp@gmail.com", pswd)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print ("Watchlist Email sent!")

def send_spy(test = False):
    today = datetime.date.today()
    alert_overbought = []
    alert_oversold = []
    rsi_overbought = []
    rsi_oversold = []
    try:
        print (1)
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
        print (1)
    except:
        print (2)
        con = lite.connect('ALERT_DATA.db')
        print (2)
    cur = con.cursor()
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM SPY_DATA WHERE SIGNAL != 0 ORDER BY Name Asc")
        for name,signal,rsi,slowk,slowd in cur.fetchall():
            if signal == -1:
                alert_overbought.append("%s is overbought with RSI at %s and the stochastics at %s and at %s"%(name,rsi,slowk,slowd))
            elif signal == 1:
                alert_oversold.append("%s is oversold with RSI at %s and the stochastics at %s and at %s"%(name,rsi,slowk,slowd))
            else:
                pass

        cur.execute("SELECT * FROM SPY_DATA WHERE RSI NOT BETWEEN 35 AND 65 ORDER BY RSI DESC")
        for name,signal,rsi,slowk,slowd in cur.fetchall():
            if rsi > 65:
                rsi_overbought.append("%s is overbought with RSI at %s"%(name,rsi))
            elif rsi < 35:
                rsi_oversold.append("%s is oversold with RSI at %s"%(name,rsi))
            else:
                pass

    message = """Good evening,\n(This is an automated message)\n\nThese are the stocks that are currently overbought and oversold from the S&P500:\n"""
    for i in alert_overbought:
        message +='\n %s'%i
    message +="""\n\nThese are the stocks that are currently oversold from the S&P500:\n"""
    for i in alert_oversold:
        message += '\n %s'%i
    message +="""\n\nThese are the stocks that are currently overbought based only on RSI from the S&P500:\n"""
    for i in rsi_overbought:
        message += '\n %s'%i
    message +="""\n\nThese are the stocks that are currently oversold based only on RSI from the S&P500:\n"""
    for i in rsi_oversold:
        message += '\n %s'%i
    message += "\n\n If you have any adjustments you'd like to make to the alert settings or if you'd like to add symbols to the watchlist please let me know.\nYisroel Schaffel"



    fromaddr = "routmanapp@gmail.com"
    toaddr = "aronroutman@sbcglobal.net" ##
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "SPY ALERTS for %s"%today.strftime("%m-%d-%Y")


    body = message
    print (body)
    msg.attach(MIMEText(body, 'plain'))

    if test == True:
        pass
    else:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("routmanapp@gmail.com", pswd)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print ("SPY Email sent!")


send_watchlist(test = True)
send_spy(test = True)'''