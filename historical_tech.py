import holidays
from datetime import timedelta, date, datetime
import sqlite3 as lite
from tech import Tech
import datetime
import random
from dateutil import parser
import finsymbols
import pickle
today = date.today()
def market_day():
    not_holiday = today not in holidays.UnitedStates()
    isntweekend = today.isoweekday()
    if not_holiday and (isntweekend != 7) and (isntweekend != 1):
        return True
    else:
        return False






def make_watchlist():
    date = (datetime.datetime.today()- datetime.timedelta(hours = 6)).strftime('%Y-%m-%d')
    symbols = [
            'AAL','AAPL','ABT','ABBV','ABX','ACAD','ADBE','ADP','AET','AGO','ALL','AMAT','AMD','AMGN','APA','AXP','BA','BAC','BAX','BCLYF',
            'BHI','BMY','BP','C','CAR','CBI','CELG','CMCSA','CNI','COP', 'CREE','CSCO','CREE','CTL','CLX','CTSH','CVS','CVX','DFS','DIS',
            'DO','DTV','DVN','ESRX','EXAS','F','FB','FCX','FITB','FLR','GE','GILD','GLW','GS','L_GSK','HAL','HP','HPQ','IBM','INTC','INTU',
            'JNJ','JPM','KEY','NYSE_KKR','KR','KRFT','KSU','L','LLY','LNKD','LOW','MCK','MET','MDT','MMM','MON','MRK','MSFT','MUR','MYL','NBL',
            'NE','NFX','NTRS','NVSEF','ORCL','OXY','P','PE','PEP','PFE','PG','PLUG','PM','PNC','PSX','PXD','QCOM','RRC','SCHW','STLD','STT',
            'T','TA_TEVA','TRV','TSO','TWTR','TXN','TYC','UBS','UNGS','UNH','URI','USB','UTX','VRX','VZ','WFC','X','YHOO','XOM','GOOG','JPM',
            'PCLN','SPY'
        ]



    dic = {}
    for i in symbols:
        try:
            tech = Tech(i,time = "daily")
            dic[i] = {'signal':tech.signals(),
                      "RSI":tech.rsi(),
                      "Stochastic":tech.slow_stoch()}
            print ("%s successful"%i)
        except Exception as e:
            print (e)
            print ("%s unsuccessful"%i)
    try:
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA_HISTORY.db')
    except:
        con = lite.connect('ALERT_DATA_HISTORY.db')

    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS HISTORY(DAY DATE,NAME TEXT,SIGNAL INT,RSI INT,SLOWK INT,SLOWD INT)")
    for i in dic:
        cur.execute("INSERT INTO HISTORY(DAY,NAME,SIGNAL,RSI,SLOWK,SLOWD) VALUES (?,?,?,?,?,?)",(date,i,dic[i]['signal'],dic[i]['RSI'],dic[i]['Stochastic'][0],dic[i]['Stochastic'][0]))
    con.commit()
    con.close()

def make_spy():
    date = (datetime.datetime.today()- datetime.timedelta(hours = 6)).strftime('%Y-%m-%d')
    sp500 = finsymbols.get_sp500_symbols()
    dic = {}
    for i in sp500:
        i = i['symbol']
        try:
            tech = Tech(i,time = "daily")
            dic[i] = {'signal':tech.signals(),
                      "RSI":tech.rsi(),
                      "Stochastic":tech.slow_stoch()}
            print ("%s successful"%i)
        except Exception as e:
            print (e)
            print ("%s unsuccessful"%i)
    try:
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA_HISTORY.db')
    except:
        con = lite.connect('ALERT_DATA_HISTORY.db')

    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS SPY_HISTORY(DAY DATE,NAME TEXT,SIGNAL INT,RSI INT,SLOWK INT,SLOWD INT)")
    for i in dic:
        cur.execute("INSERT INTO SPY_HISTORY(DAY,NAME,SIGNAL,RSI,SLOWK,SLOWD) VALUES (?,?,?,?,?,?)",(date,i,dic[i]['signal'],dic[i]['RSI'],dic[i]['Stochastic'][0],dic[i]['Stochastic'][0]))
    con.commit()
    con.close()




def make_watchlist_weekly():
    date = (datetime.datetime.today()- datetime.timedelta(hours = 6)).strftime('%Y-%m-%d')
    symbols = [
            'AAL','AAPL','ABT','ABBV','ABX','ACAD','ADBE','ADP','AET','AGO','ALL','AMAT','AMD','AMGN','APA','AXP','BA','BAC','BAX','BCLYF',
            'BHI','BMY','BP','C','CAR','CBI','CELG','CMCSA','CNI','COP', 'CREE','CSCO','CREE','CTL','CLX','CTSH','CVS','CVX','DFS','DIS',
            'DO','DTV','DVN','ESRX','EXAS','F','FB','FCX','FITB','FLR','GE','GILD','GLW','GS','L_GSK','HAL','HP','HPQ','IBM','INTC','INTU',
            'JNJ','JPM','KEY','NYSE_KKR','KR','KRFT','KSU','L','LLY','LNKD','LOW','MCK','MET','MDT','MMM','MON','MRK','MSFT','MUR','MYL','NBL',
            'NE','NFX','NTRS','NVSEF','ORCL','OXY','P','PE','PEP','PFE','PG','PLUG','PM','PNC','PSX','PXD','QCOM','RRC','SCHW','STLD','STT',
            'T','TA_TEVA','TRV','TSO','TWTR','TXN','TYC','UBS','UNGS','UNH','URI','USB','UTX','VRX','VZ','WFC','X','YHOO','XOM','GOOG','JPM',
            'PCLN','SPY'
        ]



    dic = {}
    for i in symbols:
        try:
            tech = Tech(i,time = "weekly")
            dic[i] = {'signal':tech.signals(),
                      "RSI":tech.rsi(),
                      "Stochastic":tech.slow_stoch()}
            print ("%s successful"%i)
        except Exception as e:
            print (e)
            print ("%s unsuccessful"%i)
    try:
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA_HISTORY.db')
    except:
        con = lite.connect('ALERT_DATA_HISTORY.db')

    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS WEEKLY_HISTORY(DAY DATE,NAME TEXT,SIGNAL INT,RSI INT,SLOWK INT,SLOWD INT)")
    for i in dic:
        cur.execute("INSERT INTO WEEKLY_HISTORY(DAY,NAME,SIGNAL,RSI,SLOWK,SLOWD) VALUES (?,?,?,?,?,?)",(date,i,dic[i]['signal'],dic[i]['RSI'],dic[i]['Stochastic'][0],dic[i]['Stochastic'][0]))
    con.commit()
    con.close()

def make_spy_weekly():
    date = (datetime.datetime.today()- datetime.timedelta(hours = 6)).strftime('%Y-%m-%d')
    sp500 = finsymbols.get_sp500_symbols()
    dic = {}
    for i in sp500:
        i = i['symbol']
        try:
            tech = Tech(i,time = "weekly")
            dic[i] = {'signal':tech.signals(),
                      "RSI":tech.rsi(),
                      "Stochastic":tech.slow_stoch()}
            print ("%s successful"%i)
        except Exception as e:
            print (e)
            print ("%s unsuccessful"%i)
    try:
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA_HISTORY.db')
    except:
        con = lite.connect('ALERT_DATA_HISTORY.db')

    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS SPY_HISTORY_WEEKLY(DAY DATE,NAME TEXT,SIGNAL INT,RSI INT,SLOWK INT,SLOWD INT)")
    for i in dic:
        cur.execute("INSERT INTO SPY_HISTORY_WEEKLY(DAY,NAME,SIGNAL,RSI,SLOWK,SLOWD) VALUES (?,?,?,?,?,?)",(date,i,dic[i]['signal'],dic[i]['RSI'],dic[i]['Stochastic'][0],dic[i]['Stochastic'][0]))
    con.commit()
    con.close()


def make_watchlist_2017():
    date = (datetime.datetime.today()- datetime.timedelta(hours = 6)).strftime('%Y-%m-%d')
    try:
        pickle_in = (open("/home/yaschaffel/mysite/symbols_list.pickle","rb"))
    except:
        pickle_in = open("symbols_list.pickle","rb")
    positions_2017 = (pickle.load(pickle_in))




    dic = {}
    for i in positions_2017:
        try:
            tech = Tech(i,time = "daily")
            dic[i] = {'signal':tech.signals(),
                      "RSI":tech.rsi(),
                      "Stochastic":tech.slow_stoch()}
            print ("%s successful"%i)
        except Exception as e:
            print (e)
            print ("%s unsuccessful"%i)
    try:
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA_HISTORY.db')
    except:
        con = lite.connect('ALERT_DATA_HISTORY.db')

    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS HISTORY_2017(DAY DATE,NAME TEXT,SIGNAL INT,RSI INT,SLOWK INT,SLOWD INT)")
    for i in dic:
        cur.execute("INSERT INTO HISTORY_2017(DAY,NAME,SIGNAL,RSI,SLOWK,SLOWD) VALUES (?,?,?,?,?,?)",(date,i,dic[i]['signal'],dic[i]['RSI'],dic[i]['Stochastic'][0],dic[i]['Stochastic'][0]))
    con.commit()
    con.close()


if market_day():
    make_spy_weekly()
    make_watchlist_weekly()
    make_watchlist()
    make_spy()
    make_watchlist_2017()
else:
    print("weekend")


'''

con = lite.connect('ALERT_DATA_HISTORY.db')
cur = con.cursor()
import datetime
cur.execute("select NAME,DAY,SIGNAL from HISTORY")
for i in cur.fetchall():
#     if parser.parse((i[1])) >
      if (parser.parse(str(i[1]))) > parser.parse('2016-12-10'):
        print (i)'''