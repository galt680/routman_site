import talib as ta
import Quandl as q
import numpy as np
from passwords import auth
from live_tech import Tech


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
		self.high = np.array(self.data['High'])
		self.low = np.array(self.data['Low'])
		self.close = np.array(self.data['Close'])
		self.opens = np.array(self.data['Open'])

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

