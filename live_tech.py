import Quandl as q
import numpy as np
from passwords import auth
import talib as ta
import re	
import requests

class Tech(object):
	def __init__(self,name,time = "hourly"):
		#get the minute data from google finance API, get the most recent prices in the chain 
		self.name = name
		url = "https://www.google.com/finance/getprices?i=60&p=1d&f=c,o,h,l&df=cpct&q=%s"%(name.upper())
		page = requests.get(url).text
		prices = re.findall(r'''\n(\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+)''',page)
		most_recent_close = float(prices[-1].split(',')[0])
		most_recent_high = float(prices[-1].split(',')[1])
		most_recent_low = float(prices[-1].split(',')[2])
		most_recent_open = float(prices[-1].split(',')[3])
		# self.data =	
		
		if time == "hourly":
			# self.name = name
			#get the minute data from google finacne API, get the most recent prices in the chain 
			# url = "https://www.google.com/finance/getprices?i=60&p=1d&f=c,o,h,l&df=cpct&q=%s"%(name.upper())
			# page = requests.get(url).text
			# prices = re.findall(r'''\n(\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+)''',page)
			# most_recent_close = float(prices[-1].split(',')[0])
			# most_recent_high = float(prices[-1].split(',')[1])
			# most_recent_low = float(prices[-1].split(',')[2])
			# most_recent_open = float(prices[-1].split(',')[3])
			# self.data =	
			
		#get the hourly data
			url = "https://www.google.com/finance/getprices?i=3600&p=10d&f=c,o,h,l&df=cpct&q=%s"%(name.upper())
			page = requests.get(url).text

			prices = re.findall(r'''\n(\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+)''',page)
			self.open = []
			self.high = []
			self.low = []
			self.close = []
			for i in prices:
				self.close.append(float(i.split(",")[0]))
				self.high.append(float(i.split(',')[1]))
				self.low.append(float(i.split(',')[2]))
				self.open.append(float(i.split(',')[3]))
			if most_recent_close == self.close[-1]:
				pass
			else:
				self.close.append(most_recent_close)
			if most_recent_open == self.open[-1]:
				pass
			else:
				self.open.append(most_recent_open)
			if most_recent_high == self.high[-1]:
				pass
			else:
				self.high.append(most_recent_high)
			if most_recent_low == self.low[-1]:
				pass
			else:
				self.low.append(most_recent_low)	
		elif time == "daily":
	
			#get the daily data 
			url = "https://www.google.com/finance/getprices?i=86400&p=1Y&f=c,o,h,l&df=cpct&q=%s"%(name.upper())
			# url = "https://www.google.com/finance/getprices?i=86400&p=250d&f=c,o,h,l&df=cpct&q=%s"%(name.upper())
			page = requests.get(url).text

			prices = re.findall(r'''\n(\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+)''',page)
			self.open = []
			self.high = []
			self.low = []
			self.close = []
			for i in prices:
				self.close.append(float(i.split(",")[0]))
				self.high.append(float(i.split(',')[1]))
				self.low.append(float(i.split(',')[2]))
				self.open.append(float(i.split(',')[3]))
			if most_recent_close == self.close[-1]:
				pass
			else:
				self.close.append(most_recent_close)
			if most_recent_open == self.open[-1]:
				pass
			else:
				self.open.append(most_recent_open)
			if most_recent_high == self.high[-1]:
				pass
			else:
				self.high.append(most_recent_high)
			if most_recent_low == self.low[-1]:
				pass
			else:
				self.low.append(most_recent_low)	
		else:
			print "what went wrong"
		self.high = np.array(self.high)[-225:]
		self.low = np.array(self.low)[-225:]
		self.close = np.array(self.close)[-225:]
		# self.open = np.array(self.open)

	def prints(self):
		print "close"
		print len(self.close)
		print "open"
		print len(self.open)
		print "high"
		print len(self.high)
		print "low"
		print len(self.low)
	def rsi(self):
		real = ta.RSI((self.close), timeperiod=14)
		return round(real[-1],2)

	def slow_stoch(self):
		slowk, slowd = ta.STOCH(self.high, self.low, self.close, fastk_period=10, slowk_period=10, slowk_matype=0, slowd_period=3, slowd_matype=0)
		slowk,slowd = slowk[-1],slowd[-1]
		return round(slowk,2),round(slowd,2)
	def overbought(self):
		slowk,slowd = self.slow_stoch()
		if ((slowk > 70) and (slowd	 > 70)) and (self.rsi() > 60):
			return True #"%s is overbought with RSI at %s and the stochastics at %s,%s"%(self.name.upper(),round(self.rsi(),2),round(slowk,2),round(slowd,2))
		else:
			return False
	def oversold(self):
		slowk,slowd = self.slow_stoch()
		if ((slowk < 30) and (slowd	 < 30)) and (self.rsi() < 35):
			return True
		else:
			return False

	def signals(self):
		if self.oversold() == True:
			return 1
		elif self.overbought() == True:
			return -1
		else:
			return 0
# a = Tech('goog',time = 'daily')
# a.prints()
