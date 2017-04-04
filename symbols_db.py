import sqlite3 as lite
from tech import Tech






def get_data(symbols,table_name):
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
    cur.execute("DROP TABLE IF EXISTS %s"%table_name)
    cur.execute("CREATE TABLE %s(NAME TEXT,SIGNAL INT,RSI INT,SLOWK INT,SLOWD INT)"%table_name)
    for i in dic:
        cur.execute("INSERT INTO %s(NAME,SIGNAL,RSI,SLOWK,SLOWD) VALUES (?,?,?,?,?)"%table_name,(i,dic[i]['signal'],dic[i]['RSI'],dic[i]['Stochastic'][0],dic[i]['Stochastic'][0]))
    con.commit()







con = lite.connect("/home/yaschaffel/mysite/watchlists.db")
cur = con.cursor()
for i in [i[0] for i in cur.execute("SELECT * FROM _emails_to_send")]:
    get_data([x[0] for x in cur.execute("SELECT * FROM %s"%i)],i)
	# get_data()




