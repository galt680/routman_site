import talib as ta 
import Quandl as q
import numpy as np


def rsi_maker(symbol_array,symbol, timeperiod = 14):
	rsi = ta.RSI(symbol, timeperiod)
	return rsi 
def bollinger_bands_maker(symbol_array,symbol , stdv  = 2):
    upperband, middleband, lowerband = ta.BBANDS(symbol_array,timeperiod=5, nbdevup=stdv, nbdevdn= stdv, matype=0)
    if symbol_array[-1] > upperband[-1]:
        return "%s is above its upper Bollinger Band, this is an overbought signal."%symbol.upper()
    elif symbol_array 	[-1] < lowerband[-1]:
        return "%s is below its lower Bollinger Band, this is an oversold signal."%symbol.upper()
    else:
        return "%s is neutral"%symbol.upper()