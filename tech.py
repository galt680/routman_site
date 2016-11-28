import talib as ta
try:
    import Quandl as q
except:
    import quandl as q
import numpy as np
from passwords import auth
import requests
import re

#create class that obtains data for object and calculates technical indicators for them.
class Tech(object):
    #initializes the function with the name being the symbol
    #time can be daily or hourly, default is daily 
    def __init__(self,name,time = "daily"):
        self.name = name
        if time == "daily":
    #attempts to obtain data from quandls YAHOO db, 
    #if that fails trys from GOOG 
    # if that fails it passes and will fail later in the process
            try:
                self.data = q.get('YAHOO/%s'%name.upper(),authtoken =  auth)
                self.data = self.data.round(decimals = 3)
                

            except:
                try:
                    self.data = q.get('GOOG/%s'%name.upper(),authtoken =  auth)
                    self.data = self.data.round(decimals = 3)
                except:
                    pass
    #gets minute data from goog finance api
            url = "https://www.google.com/finance/getprices?i=60&p=1d&f=c,o,h,l&df=cpct&q=%s"%(name.upper())
            page = requests.get(url).text
    #uses regex to get all the data points
            prices = re.findall(r'''\n(\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+)''',page)
    #gets the most recent close (here we use minute data as most recent close is most accurate by minute)
            most_recent_close = float(prices[-1].split(',')[0])
    #gets most recent H/L/C (here use daily as it's unlikely these points are well represented on the minute chart)
            url = "https://www.google.com/finance/getprices?i=86400&p=250d&f=c,o,h,l&df=cpct&q=%s"%(name.upper())
            page = requests.get(url).text
            prices = re.findall(r'''\n(\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+)''',page)
            most_recent_high = float(prices[-1].split(',')[1])
            most_recent_low = float(prices[-1].split(',')[2])
            most_recent_open = float(prices[-1].split(',')[3])
    #checks to see if recent data points is same as the last point on df
    #if the dame it converts to np.array and ignores most_recent
            if round(self.data['Close'][-1],2) == round(most_recent_close,2):
                self.high = np.array(list(self.data['High']))
                self.low = np.array(list(self.data['Low']))
                self.close = np.array(list(self.data['Close']))
    #if they are different it adds most_recent to the end of list and converts to np.array
            else:
                self.high = np.array(list(self.data['High'])+ [most_recent_high])
                self.low = np.array(list(self.data['Low']) + [most_recent_low])
                self.close = np.array(list(self.data['Close'])+ [most_recent_close])
    #if time is initialized to hourly 
        elif time == "hourly":

    #first get the minute data to add to the end of the most recent hourly data to make sure it's up to date
            url = "https://www.google.com/finance/getprices?i=60&p=1d&f=c,o,h,l&df=cpct&q=%s"%(name.upper())
            page = requests.get(url).text
            prices = re.findall(r'''\n(\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+)''',page)
            most_recent_close = float(prices[-1].split(',')[0])
            most_recent_high = float(prices[-1].split(',')[1])
            most_recent_low = float(prices[-1].split(',')[2])
            most_recent_open = float(prices[-1].split(',')[3])

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

    #check if the most recent minute data piece equals the most recent houry if does pass if not add most recent to hourly
            if most_recent_close == self.close[-1]:
                pass
            else:
                self.close.append(most_recent_close)
                self.open.append(most_recent_open)
                self.high.append(most_recent_high)
                self.low.append(most_recent_low)

    #convert all lists to numpy arrays to comply with talib library
            self.open = np.array(self.open)
            self.high = np.array(self.high)
            self.low = np.array(self.low)
            self.close = np.array(self.close)

        elif time == "weekly":
            print 2
            try:
                self.data = q.get('YAHOO/%s'%name.upper(), authtoken =  auth, collapse = "weekly")
                self.data = self.data.round(decimals = 3)

            except:
                try:
                    self.data = q.get('GOOG/%s'%name.upper(), authtoken =  auth, collapse = "weekly")
                    self.data = self.data.round(decimals = 3)
                except:
                    pass
            #gets minute data from goog finance api
            url = "https://www.google.com/finance/getprices?i=60&p=1d&f=c,o,h,l&df=cpct&q=%s"%(name.upper())
            page = requests.get(url).text
            #uses regex to get all the data points
            prices = re.findall(r'''\n(\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+)''',page)
            #gets the most recent close (here we use minute data as most recent close is most accurate by minute)
            most_recent_close = float(prices[-1].split(',')[0])
            #gets most recent H/L/C (here use daily as it's unlikely these points are well represented on the minute chart)
            url = "https://www.google.com/finance/getprices?i=86400&p=250d&f=c,o,h,l&df=cpct&q=%s"%(name.upper())
            page = requests.get(url).text
            prices = re.findall(r'''\n(\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+)''',page)
            most_recent_high = float(prices[-1].split(',')[1])
            most_recent_low = float(prices[-1].split(',')[2])
            most_recent_open = float(prices[-1].split(',')[3])
            #checks to see if recent data points is same as the last point on df
            #if the dame it converts to np.array and ignores most_recent
            if round(self.data['Close'][-1],2) == round(most_recent_close,2):
                self.high = np.array(list(self.data['High']))
                self.low = np.array(list(self.data['Low']))
                self.close = np.array(list(self.data['Close']))
            #if they are different it adds most_recent to the end of list and converts to np.array
            else:
                self.high = np.array(list(self.data['High'])+ [most_recent_high])
                self.low = np.array(list(self.data['Low']) + [most_recent_low])
                self.close = np.array(list(self.data['Close'])+ [most_recent_close])
    #uses talib library to get the 14 day RSI
    def rsi(self):
        real = ta.RSI(((self.close)), timeperiod=14)
        return round(real[-1],2)
    #uses talib library to get the stochastics
    def slow_stoch(self):
        slowk, slowd = ta.STOCH(self.high, self.low, self.close, fastk_period=10, slowk_period=10, slowk_matype=0, slowd_period=3, slowd_matype=0)
        slowk,slowd = slowk[-1],slowd[-1]
        return round(slowk,2),round(slowd,2)
        
    #defines overbought and uses rsi and slow_stoch methods to measure
    #returns True if overbought else False
    def overbought(self):
        slowk,slowd = self.slow_stoch()
        if ((slowk > 70) and (slowd  > 70)) and (self.rsi() > 60):
            return True #"%s is overbought with RSI at %s and the stochastics at %s,%s"%(self.name.upper(),round(self.rsi(),2),round(slowk,2),round(slowd,2))
        else:
            return False
            
    #defines oversold and uses rsi and slow_stoch methods to measure
    #returns True if oversold else False
    def oversold(self):
        slowk,slowd = self.slow_stoch()
        if ((slowk < 30) and (slowd  < 30)) and (self.rsi() < 35):
            return True
        else:
            return False
    #checks if stock is overbought or oversold
    #returns 1 for oversold and -1 for overbought
    #else it returns 0
    def signals(self):
        if self.oversold() == True:
            return 1
        elif self.overbought() == True:
            return -1
        else:
            return 0

	