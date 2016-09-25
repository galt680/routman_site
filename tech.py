import talib as ta
import Quandl as q
import numpy as np
from passwords import auth
from live_tech import Tech
import requests
import re


class Tech(object):

	def __init__(self,name):
		self.name = name
		try:
			self.data = q.get('YAHOO/%s'%name.upper(),authtoken =  auth)
			
		except:
			try:
				self.data = q.get('GOOG/%s'%name.upper(),authtoken =  auth)
			except:
				pass
				
		url = "https://www.google.com/finance/getprices?i=60&p=1d&f=c,o,h,l&df=cpct&q=%s"%(name.upper())
		page = requests.get(url).text
		prices = re.findall(r'''\n(\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+)''',page)
		most_recent_close = float(prices[-1].split(',')[0])
		
		url = "https://www.google.com/finance/getprices?i=86400&p=250d&f=c,o,h,l&df=cpct&q=%s"%(name.upper())
		page = requests.get(url).text
		prices = re.findall(r'''\n(\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+)''',page)
		most_recent_high = float(prices[-1].split(',')[1])
		most_recent_low = float(prices[-1].split(',')[2])
		most_recent_open = float(prices[-1].split(',')[3])
		
		# print most_recent_close
		
		# self.high = np.array(list(self.data['High'])+ [most_recent_high]
		# self.low = np.array(list(self.data['Low']).append(most_recent_low))
		# self.close = np.array(list(self.data['Close']).append(most_recent_close))
		a = list(self.data['Close'])+ [most_recent_close]
		
		print a
		# print most_recent_close
		# print round(a[-1],2)
		# self.opens = np.array(list(self.data['Open']).append(most_recent_open))
		# print self.close

	# def prints(self):
		# print "close"
		# print (self.close)
		# print "open"
		# print (self.opens)[-10:]
		# print "high"
		# print (self.high)[-10:]
		# print "low"
		# print (self.low)[-10:]

	def rsi(self):
		real = ta.RSI(((self.close)), timeperiod=14)
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

