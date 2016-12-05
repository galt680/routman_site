import sqlite3 as lite
from tech import Tech
import timeit

start = timeit.default_timer()
symbols = [
            'AAL','AAPL','ABT','ABBV','ABX','ACAD','ADBE','ADP','AET','AGO','ALL','AMAT','AMD','AMGN','APA','AXP','BA','BAC','BAX','BCLYF',
            'BHI','BMY','BP','C','CAR','CBI','CELG','CMCSA','CNI','COP', 'CREE','CSCO','CREE','CTL','CLX','CTSH','CVS','CVX','DFS','DIS',
            'DO','DTV','DVN','ESRX','EXAS','F','FB','FCX','FITB','FLR','GE','GILD','GLW','GS','L_GSK','HAL','HP','HPQ','IBM','INTC','INTU',
            'JNJ','JPM','KEY','NYSE_KKR','KR','KRFT','KSU','L','LLY','LNKD','LOW','MCK','MET','MDT','MMM','MON','MRK','MSFT','MUR','MYL','NBL',
            'NE','NFX','NTRS','NVSEF','ORCL','OXY','P','PE','PEP','PFE','PG','PLUG','PM','PNC','PSX','PXD','QCOM','RRC','SCHW','STLD','STT',
            'T','TA_TEVA','TRV','TSO','TWTR','TXN','TYC','UBS','UNGS','UNH','URI','USB','UTX','VRX','VZ','WFC','X','YHOO','XOM','GOOG','JPM',
            'PCLN','SPY'
          ]
    
# positions_2017 = [
            # 'AMZN', 'VRX', 'AGN', 'RH', 'BLUE', 'CMG', 'MNK', 'PRGO', 'GPRO', 'GILD',
            # 'BBBY', 'CF', 'FOSL', 'WDC', 'TWTR', 'ALXN', 'ILMN', 'VIAB', 'TEVA', 'BIIB',
            # 'CL', 'LLL', 'KORS', 'KMI', 'NLNK', 'SKX', 'SWIR', 'CVS', 'WSM', 'WHR',
            # 'MYL', 'BMRN', 'CLVS', 'OPHT', 'ALNY', 'TSLA', 'BMY ', 'NSM', 'STX', 'VOD',
            # 'ICPT', 'MCK', 'MRO', 'SHPG', 'SPG', 'NOV', 'ETE', 'MON', 'TRGP', 'COP',
            # 'IBB', 'SSYS', 'CLDX', 'M', 'WFM', 'DATA', 'TRN', 'BG', 'DVN', 'THC',
            # 'PBYI', 'CSIQ', 'BX', 'AXP', 'APC', 'HES', 'AMBA', 'XON'
            # ]



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

try:
    pickle_in = (open("/home/yaschaffel/mysite/symbols_list.pickle","rb"))
except:
    pickle_in = open("symbols_list.pickle","rb")
positions_2017 = (pickle.load(pickle_in))
daily_data_2017(symbols = positions_2017)

