#importing request allows to pull down a website
import requests
#import Quandl which allows to pull down data from Quandl website
import Quandl as q
#gives acces to pandas
import pandas as pd
#allows access to date features and holiday features
from datetime import timedelta, date, datetime
import datetime
import holidays
import calendar
import time
import bs4
import re


#pull all the data from Quandl
#authtoken allows unlimited pulls, End part specifies which part of the data is needed.
authtoken = "UxWHyskR-2WjjvSsdxu4"
qSPY = q.get("YAHOO/INDEX_SPY", authtoken = authtoken)['Close'] 
qSPY_PC = q.get('CBOE/SPX_PC', authtoken = authtoken)['S&P PUT-CALL RATIO']
qVIX = q.get("CBOE/VIX", authtoken = authtoken)["VIX Close"]
qVXV = (q.get("CBOE/VXV", authtoken = authtoken)["CLOSE"])
qVXST = q.get("CBOE/VXST", authtoken = authtoken)["Close"]
qVX1 = q.get("CHRIS/CBOE_VX1", authtoken = authtoken)["Close"]
qVX2 = q.get("CHRIS/CBOE_VX2", authtoken = authtoken)["Close"]
qVX3 = q.get("CHRIS/CBOE_VX3", authtoken = authtoken)["Close"]
qVVIX = q.get('CBOE/VVIX', authtoken = authtoken)['VVIX']
today = date.today()



#gets the vixcentral website
r = requests.get('http://vixcentral.com/')
# sets what's to be searched for in the html; this is all the stuff before the numbers we need
search = 'var last_data_var=['
data = r.content
# this filters out everything until the data
data = data[data.index(search)+ len(search):]
#this gets everything until the end of the data
data = data[:data.index(']')]
#this splits the data into its parts
data = data.split(',')
#initializes a blank list to convert the data from strings to floats
vxs = []
for i in data:
	i = float(i)
	vxs.append(i)
#get each item out of list
sVX1 = vxs[0]
sVX2 = vxs[1]
sVX3 = vxs[2]



#get vixcentral again to get the indexes
r = requests.get('http://vixcentral.com/')
# the search term required
search = 'var vcurve_data_var=['
data = r.content
#filter
data = data[data.index(search)+ len(search):]
data = data[:data.index(']')]
#split
data = data.split(',')
#convert to strings
indexs = []
for i in data:
	i = float(i)
	indexs.append(i)
#get each item from list
sVXST = indexs[0]
sVIX = indexs[1]
sVXV =indexs[2]
sVXMT = indexs[3]



#get latest spy data from bloomberg
page = requests.get('http://www.bloomberg.com/quote/SPY:US')
soup = bs4.BeautifulSoup(page.text,'lxml')
sSPY = float(re.findall(r'''(\d\d\d\.\d\d+)''',(str(soup.find_all('div',class_ = 'price'))))[0])
print sSPY	



#get VVIX from cnbc
r = requests.get('http://data.cnbc.com/quotes/.VVIX')
data = r.content
#filter
seach = '''"last":"'''
data = data[data.index(seach) + len(seach):]
data = data[:data.index(',')]
#convert from string to float while being able to keep all the digits and period.
sVVIX = float(''.join(d for d in data if d.isdigit() or d == '.'))



try:
	#get xiv from cnbc
	r = requests.get('http://data.cnbc.com/quotes/xiv')
	data = r.content
	#filter
	seach = '''"last":'''
	data = data[data.index(seach) + len(seach):]
	data = data[:data.index(',')]
	XIV = float(''.join(d for d in data if d.isdigit() or d == '.'))
except:
	pass


#make appen	der function which checks if the most recently scraped data is new and if its not appends on the latest data.
def appender(var,new_var):
	new_list = list(var)
	if new_list[-1] != new_var:
		new_list.append(new_var)
	return new_list



SPY = appender(qSPY,sSPY)
VIX = appender(qVIX,sVIX)
VXST = appender(qVXST,sVXST)
VXV = appender(qVXV,sVXV)
VX1 = appender(qVX1,sVX1)
VX2 = appender(qVX2,sVX2)
VX3 = appender(qVX3,sVX3)
VVIX = appender(qVVIX,sVVIX)
#quandl doesnt have vxmt
VXMT = sVXMT

#gets the next 3r friday of the month
def next_third_friday(d):
	""" Given a third friday find next third friday"""
	d += timedelta(weeks=4)
	return d if d.day >= 15 else d + timedelta(weeks=1)

#gets next set of n 3rd Fridays
def third_fridays(d, n):
	"""Given a date, calculates n next third fridays"""

	# Find closest friday to 15th of month
	s = date(d.year, d.month, 15)
	result = [s + timedelta(days=(calendar.FRIDAY - s.weekday()) % 7)]
	

	# This month's third friday passed. Find next.
	if result[0] < d:
		result[0] = next_third_friday(result[0])

	for i in range(n - 1):
		result.append(next_third_friday(result[-1]))

	return result
	#def timestamp(d):
		   # return int(time.mktime(d.timetuple()))
		
#make function that determines when the next X fridays are
def fridays():
	#set variable today is today, rd_fridays equals the third_fridays function above and f contains a Pandas.Series of the next 5 fridays
	# with index starting at 1
	today = date.today()
	rd_fridays = third_fridays((today), 5)
	f = pd.Series(rd_fridays, index = [1,2,3,4,5])
	#function that determines when the next VIX exp is by taking the next SPX expiration
	def vix_exp():
		#us_holidays checks if there is us holiday on usuall SPX exp if so takes of another day 
		#f[x] is a datetime.date object, timedelta(x) subtracts that many days from that time
		us_holidays = holidays.UnitedStates()
		if (f[2] - timedelta(31)) in us_holidays:
			f1 = f[2] - timedelta(32)
			f2 = f[3] - timedelta(31) 
			f3 = f[4] - timedelta(31)
			f4 = f[5] - timedelta(31)
		else:
			f0 = f[1] - timedelta(31) 
			f1 = f[2] - timedelta(31)
			f2 = f[3] - timedelta(31) 
			f3 = f[4] - timedelta(31)
			f4 = f[5] - timedelta(31)

		#reurns the value for the next 4 expirations and the previous 1(f[0])
		return [f0,f1, f2, f3, f4]
	#defines vix_exp and returns it 
	vix_exp = vix_exp()
	return vix_exp
#define function that says how many days until expiration
def expiration():
	#define variables today gets todaym, Fridays represents the function fridays(), nxt represents the next VIX expiration
	today = date.today()
	Fridays = fridays()
	nxt = []
	#get nxt by getting the values of the next 3 expirations using loop
	for x in range(0,4):
		nxt.append(Fridays[x])
	# if the closest VIX exp has past and the fridays() function hasn't reset then use passed to move up all expirations, else use normal expiraions
	passed = nxt[0] - today
	passed = int(passed.days)
	if passed < 0:
		exp = int((nxt[1] - today).days)
		exp2 = int((nxt[2] - today).days)
		# try:
		exp3 = int((nxt[2]-today).days)
		# except Exception as e:
			# print e
			# print nxt[2]
			# print today
		if exp < 0:
			return [exp2,exp3]
		else:
			return[exp,exp2]
	else:
		exp = int((nxt[0] - today).days) 
		exp2 = int((nxt[1] - today).days)
		# try:
		exp3 = int((nxt[2]-today).days)
		# except Exception as e:
			# print e
			# print nxt[2]
			# print today
		if exp < 0:
			return [exp2,exp3]
		else:
			return [exp,exp2]
#Unpack exp1 and exp2 from the expiration function to T1, T2 
T1,T2 = expiration()