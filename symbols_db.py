import sqlite3 as lite
from tech import Tech
import timeit
import pickle

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

watchlist_hurry = [ u'AA', u'AAPL', u'ACCO', u'ADNT', u'AEE', u'AET', u'AFL', u'AGN', u'AKS', u'ALL',
                    u'AMAT', u'AMP', u'AMZN', u'ARNC', u'ASIX', u'AVY', u'ACP', u'BAC', u'BAX', u'BBRY',
                    u'BIIB', u'BIVV',u'BP', u'BSX', u'C', u'CBS', u'CC', u'CELG', u'CHTR', u'CL', u'CLX',
                    u'CMCSA', u'COP', u'CSCO', u'CTL', u'CV', u'CVX',u'DDAIF', u'DD', u'DFS', u'DIG', u'DIS',
                    u'DUK', u'DVMT', u'EMR', u'ENB', u'ESRX', u'ESV', u'FAZ', u'FBHS', u'FCX', u'FOXA',
                    u'FRCMQ', u'FTR', u'GE', u'GSK', u'GS', u'GILD', u'GLW', u'HD', u'HON', u'HPE', u'HPQ',
                    u'HYH', u'IBB', u'IBM', u'IMMU', u'INTC',u'JCI', u'JNJ', u'JPM', u'KMB', u'KO', u'LITE',
                    u'LLY', u'M', u'MDT', u'MMM', u'MNKD', u'MPC', u'MON', u'MRK', u'MRO',u'MS', u'MSI',
                    u'MSFT', u'MSTX', u'MYGN', u'MYRX', u'NCR', u'NSRGY', u'NRG', u'NWSA', u'OCN', u'ORCL',
                    u'PACW', u'PBI',u'PEP', u'PDLI', u'PFE', u'PG', u'PJC', u'PHG', u'PNC', u'PNR', u'POR',
                    u'PRGO', u'PRTA', u'PTQME', u'RAD', u'RAI', u'REGN',u'SR', u'SHPG', u'SJM', u'STI', u'SYF',
                    u'T', u'TEL', u'TDC', u'TEVA', u'TIME', u'TROV', u'TWX', u'UEPEO', u'USB', u'UNH',
                    u'UYG', u'VIAB', u'VOD', u'VRX', u'VZ', u'WBA', u'WFC', u'WM', u'WMT', u'WU', u'XOM', u'YUM']

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

def watchlist_speed(symbols):
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
    cur.execute("DROP TABLE IF EXISTS watchlist_hurry")
    cur.execute("CREATE TABLE watchlist_hurry(NAME TEXT,SIGNAL INT,RSI INT,SLOWK INT,SLOWD INT)")
    for i in dic:
        cur.execute("INSERT INTO watchlist_hurry(NAME,SIGNAL,RSI,SLOWK,SLOWD) VALUES (?,?,?,?,?)",(i,dic[i]['signal'],dic[i]['RSI'],dic[i]['Stochastic'][0],dic[i]['Stochastic'][0]))
    con.commit()
    stop = timeit.default_timer()
    try:
        print "Task took %s minutes"%(int(stop - start)/60)
    except:
        pass
if __name__ == '__main__':
    daily_data(symbols = symbols)
    weekly_data(symbols = symbols)
    watchlist_speed(symbols = watchlist_hurry)

    try:
        pickle_in = (open("/home/yaschaffel/mysite/symbols_list.pickle","rb"))
    except:
        pickle_in = open("symbols_list.pickle","rb")
    positions_2017 = (pickle.load(pickle_in))
    daily_data_2017(symbols = positions_2017)

