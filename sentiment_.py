try:
	import Quandl as q
except:
	import quandl as q
import pandas as pd
import requests
import re
import urllib
from passwords import auth

def whale_wisdom(x):
	site = 'http://whalewisdom.com/stock/' + x
	r = requests.get(site)
	data = r.content
	if 'increasing' in data:
		search = '<td class=" increasing ">'
	else:
		search = '<td class="decreasing">'
	data = data[data.index(search)+ len(search):]
	data = data[:data.index('<')]
	data = data.strip()
	data = str(data)
	guru_links =  '''//gurufocus.com/gurutrades/%s'''%x
	# print 'Large institutions have changed their holdings by '+ data
	return [('Large institutions have changed their holdings by '+ data),guru_links]

def sentiment_index(x):
	def checker():
		r = requests.get('http://stocktwits.com/symbol/aapl')
		data = r.content
		search = "<span class='bullish'>"
		data = data[data.index(search)+ len(search):]
		data = data[:data.index('Bearish')]
		return True
	site = 'http://stocktwits.com/symbol/' + x
	r = requests.get(site)
	data = r.content
	search = "<span class='bullish'>"
	try:
		data = data[data.index(search)+ len(search):]
	except Exception as e:
		if checker() == True:
			print "This doesn't have it"
		else:
			print 'The code may be broken'
	data = data[:data.index('Bearish')]
	data = re.findall(r'\d+?%',data)
	print data
	for i in range(len(data)):
		data[i] = float(data[i].strip('%'))
	if data[0] > data[1]:
		data = data[0]
		return "The Sentiment Index is at %s%% bullish"%int(data)
	elif data[1] > data[0]:
		data = -1*data[1]
		return "The Sentiment Index is at %s%% bearish"%int(data)
	else:
		return 'This code may be broken'

def short_interest(x):
	x = x.capitalize()
	symbol = 'SI/'+ x + '_SI'
	sym = q.get(symbol, authtoken = auth)
	if "Days To Cover" in sym.columns:
		dtc = "Days To Cover"
		sint = sym[dtc]
	else:
		dtc = "Days to Cover"
		sint = sym[dtc]
	sint = sint[-24:]
	median = sint.median()
	recent = sint[-1]
	avg = 100*(recent-median)/median
	avg = round(avg,2)
	if avg > 0:
		avg = str(avg)
		return 'The short interest in '+ x.upper() + " rose " + avg +'%'
	else:
		avg = str(avg)
		return 'The short interest in '+ x.upper() + " fell " + avg + '%'
	std = sint.std()
	cstd = (recent - median)/std
	cstd = abs(cstd)
	cstd = round(cstd,2)
	cstd = str(cstd)
	print "This is a " +cstd + " standard deviation move"