import sqlite3 as lite
con = lite.connect('IMP_VOL_TABLE.db')
cur = con.cursor()
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
print (dict['AAPL'][0]-dict['AAPL'][2])/dict['AAPL'][2]
print (dict['AMZN'][0]-dict['AMZN'][2])/dict['AMZN'][2]

def get_percent(symbol):
    return dict[symbol][0]-dict[symbol][2])/dict[symbol][2]