import sqlite3 as lite
from tech import Tech
import timeit
import pickle

start = timeit.default_timer()





def daily_data(symbols):
    dic = {}
    for i in symbols:
        try:
            tech = Tech(i,time = "daily")
            dic[i] = {'signal':tech.signals(),
                      "RSI":tech.rsi(),
                      "Stochastic":tech.slow_stoch()}
            print "%s successful"%i
        except Exception as e:
            print e
            print "%s unsuccessful"%i
    try:
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
    except:
        con = lite.connect('ALERT_DATA.db')
    print con
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS ALERT_DATA")
    cur.execute("CREATE TABLE ALERT_DATA(NAME TEXT,SIGNAL INT,RSI INT,SLOWK INT,SLOWD INT)")
    for i in dic:
        cur.execute("INSERT INTO ALERT_DATA(NAME,SIGNAL,RSI,SLOWK,SLOWD) VALUES (?,?,?,?,?)",(i,dic[i]['signal'],dic[i]['RSI'],dic[i]['Stochastic'][0],dic[i]['Stochastic'][0]))
    con.commit()
    stop = timeit.default_timer()
    try:
        print "Task took %s minutes"%(int(stop - start)/60)
    except:
        pass


def weekly_data(symbols):
    dic = {}
    for i in symbols:
        try:
            tech = Tech(i,time = "daily")
            dic[i] = {'signal':tech.signals(),
                      "RSI":tech.rsi(),
                      "Stochastic":tech.slow_stoch()}
            print "%s successful"%i
        except Exception as e:
            print e
            print "%s unsuccessful"%i
    try:
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
    except:
        con = lite.connect('ALERT_DATA.db')
    print con
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS ALERT_DATA_WEEKLY")
    cur.execute("CREATE TABLE ALERT_DATA_WEEKLY(NAME TEXT,SIGNAL INT,RSI INT,SLOWK INT,SLOWD INT)")
    for i in dic:
        cur.execute("INSERT INTO ALERT_DATA_WEEKLY(NAME,SIGNAL,RSI,SLOWK,SLOWD) VALUES (?,?,?,?,?)",(i,dic[i]['signal'],dic[i]['RSI'],dic[i]['Stochastic'][0],dic[i]['Stochastic'][0]))
    con.commit()
    stop = timeit.default_timer()
    try:
        print "Task took %s minutes"%(int(stop - start)/60)
    except:
        pass


def daily_data_2017(symbols):
    dic = {}
    for i in symbols:
        try:
            tech = Tech(i,time = "daily")
            dic[i] = {'signal':tech.signals(),
                      "RSI":tech.rsi(),
                      "Stochastic":tech.slow_stoch()}
            print "%s successful"%i
        except Exception as e:
            print e
            print "%s unsuccessful"%i
    try:
        con = lite.connect('/home/yaschaffel/mysite/ALERT_DATA.db')
    except:
        con = lite.connect('ALERT_DATA.db')
    print con
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS ALERT_DATA_2017")
    cur.execute("CREATE TABLE ALERT_DATA_2017(NAME TEXT,SIGNAL INT,RSI INT,SLOWK INT,SLOWD INT)")
    for i in dic:
        cur.execute("INSERT INTO ALERT_DATA_2017(NAME,SIGNAL,RSI,SLOWK,SLOWD) VALUES (?,?,?,?,?)",(i,dic[i]['signal'],dic[i]['RSI'],dic[i]['Stochastic'][0],dic[i]['Stochastic'][0]))
    con.commit()
    stop = timeit.default_timer()
    try:
        print "Task took %s minutes"%(int(stop - start)/60)
    except:
        pass



daily_data(symbols = symbols)
weekly_data(symbols = symbols)


