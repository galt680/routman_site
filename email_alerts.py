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

def send_watchlist(table_name,test = False):
    today = datetime.date.today()
    alert_overbought = []
    alert_oversold = []
    rsi_overbought = []
    rsi_oversold = []
    try:
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
    except:
        con = lite.connect('ALERT_DATA.db')
    cur = con.cursor()
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM %s WHERE SIGNAL != 0 ORDER BY Name Asc"%table_name)
        rows = cur.fetchall()
        for name,signal,rsi,slowk,slowd in rows:
            if signal == -1:
                alert_overbought.append("%s is overbought with RSI at %s and the stochastics at %s and at %s"%(name,rsi,slowk,slowd))
            elif signal == 1:
                alert_oversold.append("%s is oversold with RSI at %s and the stochastics at %s and at %s"%(name,rsi,slowk,slowd))
            else:
                pass

        cur.execute("SELECT * FROM %s WHERE RSI NOT BETWEEN 35 AND 65 ORDER BY RSI DESC"%table_name)
        rows = cur.fetchall()
        for name,signal,rsi,slowk,slowd in rows:
            if rsi > 65:
                rsi_overbought.append("%s is overbought with RSI at %s"%(name,rsi))
            elif rsi < 35:
                rsi_oversold.append("%s is oversold with RSI at %s"%(name,rsi))
            else:
                pass

    message = """Good evening,\n(This is an automated message)\n\nThese are the stocks that are currently overbought and oversold from %s:\n"""%table_name
    for i in alert_overbought:
        message +='\n %s'%i
    message +="""\n\nThese are the stocks that are currently oversold from %s:\n"""%table_name
    for i in alert_oversold:
        message += '\n %s'%i
    message +="""\n\nThese are the stocks that are currently overbought based only on RSI from %s:\n"""%table_name
    for i in rsi_overbought:
        message += '\n %s'%i
    message +="""\n\nThese are the stocks that are currently oversold based only on RSI from %s:\n"""%table_name
    for i in rsi_oversold:
        message += '\n %s'%i
    message += "\n\n If you have any adjustments you'd like to make to the alert settings or if you'd like to add symbols to the watchlist please let me know.\nYisroel Schaffel"



    fromaddr = "routmanapp@gmail.com"
    toaddr = "aronroutman@sbcglobal.net" ##
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "%s Alerts for %s"%(table_name,today.strftime("%m-%d-%Y"))


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


def send_watchlist_2017(test = False):
    today = datetime.date.today()
    alert_overbought = []
    alert_oversold = []
    rsi_overbought = []
    rsi_oversold = []
    try:
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
    except:
        con = lite.connect('ALERT_DATA.db')
    cur = con.cursor()
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM ALERT_DATA_2017 WHERE SIGNAL != 0 ORDER BY Name Asc")
        rows = cur.fetchall()
        for name,signal,rsi,slowk,slowd in rows:
            if signal == -1:
                alert_overbought.append("%s is overbought with RSI at %s and the stochastics at %s and at %s"%(name,rsi,slowk,slowd))
            elif signal == 1:
                alert_oversold.append("%s is oversold with RSI at %s and the stochastics at %s and at %s"%(name,rsi,slowk,slowd))
            else:
                pass

        cur.execute("SELECT * FROM ALERT_DATA_2017 WHERE RSI NOT BETWEEN 35 AND 65 ORDER BY RSI DESC")
        rows = cur.fetchall()
        for name,signal,rsi,slowk,slowd in rows:
            if rsi > 65:
                rsi_overbought.append("%s is overbought with RSI at %s"%(name,rsi))
            elif rsi < 35:
                rsi_oversold.append("%s is oversold with RSI at %s"%(name,rsi))
            else:
                pass

    message = """Good evening,\n(This is an automated message)\n\nThese are the stocks that are currently overbought and oversold from your 2017 positions watchlist:\n"""
    for i in alert_overbought:
        message +='\n %s'%i
    message +="""\n\nThese are the stocks that are currently oversold from your 2017 positions watchlist:\n"""
    for i in alert_oversold:
        message += '\n %s'%i
    message +="""\n\nThese are the stocks that are currently overbought based only on RSI from your 2017 positions watchlist:\n"""
    for i in rsi_overbought:
        message += '\n %s'%i
    message +="""\n\nThese are the stocks that are currently oversold based only on RSI from your 2017 positions watchlist:\n"""
    for i in rsi_oversold:
        message += '\n %s'%i
    message += "\n\n If you have any adjustments you'd like to make to the alert settings or if you'd like to add symbols to the 2017 positions watchlist please let me know.\nYisroel Schaffel"



    fromaddr = "routmanapp@gmail.com"
    toaddr = "aronroutman@sbcglobal.net" ##
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "2017 Positions Watchlist Alerts for %s"%today.strftime("%m-%d-%Y")


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
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
    except:
        con = lite.connect('ALERT_DATA.db')
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



def send_watchlist_weekly(test = False):
    today = datetime.date.today()
    alert_overbought = []
    alert_oversold = []
    rsi_overbought = []
    rsi_oversold = []
    try:
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
    except:
        con = lite.connect('ALERT_DATA.db')
    cur = con.cursor()
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM ALERT_DATA_WEEKLY WHERE SIGNAL != 0 ORDER BY Name Asc")
        rows = cur.fetchall()
        for name,signal,rsi,slowk,slowd in rows:
            if signal == -1:
                alert_overbought.append("%s is overbought with RSI at %s and the stochastics at %s and at %s"%(name,rsi,slowk,slowd))
            elif signal == 1:
                alert_oversold.append("%s is oversold with RSI at %s and the stochastics at %s and at %s"%(name,rsi,slowk,slowd))
            else:
                pass

        cur.execute("SELECT * FROM ALERT_DATA_WEEKLY WHERE RSI NOT BETWEEN 35 AND 65 ORDER BY RSI DESC")
        rows = cur.fetchall()
        for name,signal,rsi,slowk,slowd in rows:
            if rsi > 65:
                rsi_overbought.append("%s is overbought with RSI at %s"%(name,rsi))
            elif rsi < 35:
                rsi_oversold.append("%s is oversold with RSI at %s"%(name,rsi))
            else:
                pass

    message = """Good evening,\n(This is an automated message)\n\nThese are the stocks that are currently overbought and oversold from your watchlist on the weekly chart:\n"""
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
    msg['Subject'] = "Weekly Watchlist Alerts for %s"%today.strftime("%m-%d-%Y")


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
        print ("Weekly Watchlist Email sent!")



def send_spy_weekly(test = False):
    today = datetime.date.today()
    alert_overbought = []
    alert_oversold = []
    rsi_overbought = []
    rsi_oversold = []
    try:
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
    except:
        con = lite.connect('ALERT_DATA.db')
    cur = con.cursor()
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM WEEKLY_SPY_DATA WHERE SIGNAL != 0 ORDER BY Name Asc")
        for name,signal,rsi,slowk,slowd in cur.fetchall():
            if signal == -1:
                alert_overbought.append("%s is overbought with RSI at %s and the stochastics at %s and at %s"%(name,rsi,slowk,slowd))
            elif signal == 1:
                alert_oversold.append("%s is oversold with RSI at %s and the stochastics at %s and at %s"%(name,rsi,slowk,slowd))
            else:
                pass

        cur.execute("SELECT * FROM WEEKLY_SPY_DATA WHERE RSI NOT BETWEEN 35 AND 65 ORDER BY RSI DESC")
        for name,signal,rsi,slowk,slowd in cur.fetchall():
            if rsi > 65:
                rsi_overbought.append("%s is overbought with RSI at %s"%(name,rsi))
            elif rsi < 35:
                rsi_oversold.append("%s is oversold with RSI at %s"%(name,rsi))
            else:
                pass

    message = """Good evening,\n(This is an automated message)\n\nThese are the stocks that are currently overbought and oversold from the S&P500 on the weekly chart:\n"""
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
    msg['Subject'] = "Weekly SPY ALERTS for %s"%today.strftime("%m-%d-%Y")


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
con = lite.connect("watchlists.db")
cur = con.cursor()
for i in [i[0] for i in cur.execute("SELECT * FROM _emails_to_send")]:        
	send_watchlist(i,test = True)
send_spy_weekly()
send_spy()

