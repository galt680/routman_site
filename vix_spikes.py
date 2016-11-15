from flask import Flask,request,render_template
import sqlite3 as lite

try:
	con = lite.connect('/home/yaschaffel/mysite/IMP_VOL_TABLE.db')
except:
	con = lite.connect('IMP_VOL_TABLE.db')
	
	
	
	
def vix_spikes_page():
	thresh = request.form['threshold']
	days = request.form['days']
	
	
	return render_template('imp_spikes.html',days = days,thresh = thresh)
	# print thresh
	# return thresh
	
	
	
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