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

def send_impvol(test = False):
    try:
        con = lite.connect('/home/yaschaffel/mysite/IMP_VOL_TABLE.db')
    except:
        con = lite.connect('IMP_VOL_TABLE.db')
    with con:
        cur = con.cursor()
        today = datetime.date.today()
        alert_overbought = []
        cur.execute("SELECT * FROM IMP_VOL_TABLE WHERE TODAY_VALUE > 1.25*YESTERDAY_VALUE")
        for rows in cur.fetchall():
            alert_overbought.append(rows)
    message = """Good evening,\n(This is an automated message)\n\nThese are the stocks that have had an implied volatility spike:\n"""
    for i in range(len(alert_overbought)):
        message +='\n The implied volatility for %s spiked' %alert_overbought[i][0]
        message +=' %s%%'%((round(((alert_overbought[i][2]-alert_overbought[i][1])/alert_overbought[i][1]*100),2)))
        message += " from %s to %s"%(alert_overbought[i][1],alert_overbought[i][2])

    message += "\n\n If you have any adjustments you'd like to make to the alert settings or if you'd like to add symbols to the watchlist please let me know.\nYisroel Schaffel"

    fromaddr = "routmanapp@gmail.com"
    toaddr = "aronroutman@sbcglobal.net" 
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Implied volatility alerts for %s"%today.strftime("%m-%d-%Y")
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
        print ("IMP VOL Email sent!")
send_impvol()


''' message = """Good evening,\n(This is an automated message)\n\nThese are the stocks that have had an implied volatility spike:\n"""
    for i in len(range(alert_overbought)):
        message +='\n %s spiked'%alert_overbought[i][0]
        message +='\n %s%%'%(round(((alert_overbought[i][2]-alert_overbought[i][1])/alert_overbought[i][1]),2))

    message += "\n\n If you have any adjustments you'd like to make to the alert settings or if you'd like to add symbols to the watchlist please let me know.\nYisroel Schaffel"

    print message

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
        print ("SPY Email sent!")'''

