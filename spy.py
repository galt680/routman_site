import requests,bs4
import re
import quandl as q
import pandas as pd
import numpy as np
import talib as ta
from flask import render_template
from bittles import bittles_levels
from vix_eval import evaluate
from passwords import auth

def spy_evalu():
	spy = np.array(list(q.get("GOOG/NYSE_SPY",authtoken = auth)["Close"]))
	spy_volume =  np.array(list(q.get("GOOG/NYSE_SPY",authtoken = auth)["Volume"]))
	def get_McOscillator():
		McOscillator = 'http://www.mcoscillator.com/market_breadth_data'
		page = requests.get(McOscillator)
		mcosc = 'http://www.mcoscillator.com'
		soup = str(bs4.BeautifulSoup(page.text,"lxml"))
		a  = re.findall(r'''src\=\"(\/data.+\.gif)''',soup)
		a = a[0]
		img = mcosc + a
		return img
	def rsi(spy):
		rsi = ta.RSI(spy,timeperiod = 14)
		rsi = round(rsi[-1],2)
		if rsi >=  70:
			statement = "RSI is in extreme overbought territory at %s"%rsi
		elif rsi > 60:
			statement = "RSI is at %s and it's	getting overbought"%rsi
		elif rsi < 40:
			statement = "RSI is at %s and it's getting oversold"%rsi
		elif rsi < 30:
			statement = "RSI is in extreme oversold territory at %s"%rsi
		else:
			statement = "RSI is at %s and is neutral"%rsi
		return rsi,statement
	def bbands(spy):
		upperband, middleband, lowerband = ta.BBANDS(spy, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
		if spy[-1] > upperband[-1]:
			bband_statement = "SPY is overbought as its above its upper Bollinger Band."
		elif spy[-1] > (.8*upperband[-1]):
			bband_statement = "SPY is getting overbought as it approaches its upper Bollinger Band."
		elif spy[-1] < lowerband[-1]:
			bband_statement = "SPY is oversold as it's below its lower Bollinger Band."
		elif spy[-1] < (1.2*lowerband[-1]):
			bband_statement = "SPY is getting oversold as it approaches its lower Bollinger Band."
		else:
			bband_statement = "SPY is between its Bollinger Bands and is neutral"
		return bband_statement
	def volume_average(spy_volume):
		recent = spy_volume[-1]
		ma5 =  list(pd.Series(spy_volume).rolling(window = 5, center = False).mean())
		ma20 = list(pd.Series(spy_volume).rolling(window = 20, center = False).mean())
		if ma5[-1] > ma20[-1]:
			return "Volume has been above average."
		elif ma5[-1] < ma20[-1]:
			return "Volume has been below average. "
		avg = np.median(spy_volume)
		return avg
	def market_breadth():
		def new_extremes():
			new_lows = q.get("URC/NYSE_52W_LO",authtoken = auth)["Numbers of Stocks"]
			new_highs = q.get("URC/NYSE_52W_HI",authtoken = auth)["Numbers of Stocks"]
			avg_lows = list(pd.Series(new_lows).rolling(window = 252, center = False).mean())[-1]
			avg_highs = list(pd.Series(new_highs).rolling(window = 252, center = False).mean())[-1]
			rec_highs = new_highs[-1]
			rec_lows = new_lows[-1]

			if rec_highs > rec_lows:
				if rec_highs > avg_highs:
					extreme_statements = "New highs are expanding rapidly with new highs outnumbering new lows %s to %s."%(int(rec_highs),int(rec_lows))
				else:
					extreme_statements = "New highs are expanding with new highs outnumbering new lows %s to %s."%(int(rec_highs),int(rec_lows))
			elif rec_highs < rec_lows:
				if rec_lows > avg_lows:
					extreme_statements = "New lows are expanding rapidly with new lows outnumbering new highs %s to %s"%(int(rec_lows),int(rec_highs))
				else:
					extreme_statements = "New lows are expanding with new lows outnumbering new highs %s to %s"%(int(rec_lows),int(rec_highs))
			return extreme_statements
		return new_extremes()

	picture = get_McOscillator()
	vol_avg = volume_average(spy_volume)
	bband_statement = bbands(spy)
	rsi,rsi_statement = rsi(spy)
	market_statement = market_breadth()
	a = bittles_levels()
	vix_statement = evaluate()
	lista = [rsi_statement,bband_statement,vol_avg,market_statement,vix_statement]
	return render_template("spy_eval.html",picture = picture, levels = a, lista = lista)

	# return render_template("spy_eval.html",picture = picture,levels = a,rsi = rsi,rsi_statement = rsi_statement,bband_statement = bband_statement,avg = vol_avg,market_statement = market_statement)

if __name__ == "__main__":
	spy_evalu()