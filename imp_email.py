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
    with con:
        cur = con.cursor()
        multi_spike = []
        cur.execute("SELECT * FROM HISTORICAL_VOL order by DAY DESC")
        dict = {}
        for i in cur.fetchall():
            if str(i[1]) not in dict:
                dict[str(i[1])] = [i[2]]
            else:
                if len(dict[str(i[1])]) < 3:
                    dict[str(i[1])].append(i[2])
                else:
                    pass
        def signal():
            def get_percent(symbol):
                symbol = symbol.upper()
                return round(100 *((dict[symbol][0]-dict[symbol][2])/dict[symbol][2]),2)
            def checker():
                spiked = []
                for i in dict:
                    if get_percent(i) >30:
                        spiked.append([i,get_percent(i)])
                    else:
                        pass
                return spiked
            return checker()
            checker()
        spiked = signal()
        for i in spiked:
             multi_spike.append("%s spiked %s%%. \n"%(i[0],i[1]))
    message = """Good morning,\n(This is an automated message)\n\nThese are the stocks that have had an implied volatility spike:\n"""
    for i in range(len(alert_overbought)):
        message +='\n The implied volatility for %s spiked' %alert_overbought[i][0]
        message +=' %s%%'%((round(((alert_overbought[i][2]-alert_overbought[i][1])/alert_overbought[i][1]*100),2)))
        message += " from %s to %s"%(alert_overbought[i][1],alert_overbought[i][2])
    message += """\nThese are the stocks that have spiked over the last 3 days:\n\n"""
    for i in range(len(multi_spike)):
        message += multi_spike[i]

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

