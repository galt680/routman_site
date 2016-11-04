from flask import Flask,request,render_template,url_for
from cStringIO import StringIO
from sentiment_ import whale_wisdom,sentiment_index,short_interest
from mv import VIX
from lxml import html
from fake_useragent import UserAgent
import matplotlib.pyplot as plt
import talib as ta
import numpy as np
try:
    import quandl as q
except:
    import Quandl as q
import re,requests,bs4,urllib,time,random
from tech import Tech
from ilvu import love
from passwords import auth

#renders the html form
def form():
    return render_template("myform.html")
#after the form is rendered and a symbol is input it calls the reading fucntion to gather all relevant data for that symbol
def readings():
    #! changed input name from "test" to "symbol"
    symbol = request.form['symbol']
    if (symbol.lower() == 'yds'):
        return render_template('say_yes.html')
    elif (symbol == "#ilvu"):
        return love()
    else:

    #request.form accesses the input from the myform.html page and the name is the access point from the html file

        length = request.form["length"]

    #to access some sites html to be scraped there needs to be a user-agent this creates a dict that makes a chrome specific user agent
        headers = {"User-Agent":UserAgent().chrome}

    #use a try/except to make sure that a valid symbol is present. if invalid symbol is entered it returns to original form
    #and using jinja modifies it to look for another symbol
        try:
            whale_change,guru_info = whale_wisdom(symbol)
        except Exception as e:

            return render_template("myform.html", a = "nother",b = ", the previous symbol appears to be invalid")
        index = sentiment_index(symbol)
        short = short_interest(symbol)

    #uses quandl to get the past data to render a chart with bollinger bands for the stock.
    #authtoken to prevent ratge limiting by quandl
    #creates a pandas series of past 'length values'
        symbol_prices = q.get("YAHOO/%s"%symbol.upper(),authtoken = auth, collapse = length)['Close'][-25:]
    #creates a numpy array of the symbol prices the talib library needs arrays as inputs
        symbol_array = np.array(list(symbol_prices))
    #unsure why dtype='f8'
        ta_symbol = np.array(symbol_array,dtype = "f8")
    #creates the 3 bollinger band lines using talib library
        upperband, middleband, lowerband = ta.BBANDS(ta_symbol, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    #create figure using fig from matplotlib ; size is golden ratio multiplier
        size = 1.618
    #unclear! why need fig and ax
        fig,ax = plt.subplots(figsize = ((size*4),4))
    #makes the title of the graph the symbol name
        plt.title(symbol.upper())
    #plots the price,upper and lower bands. uses label to create legent
        ax.plot(symbol_array,label = "Price")
        ax.plot(upperband,label = "Upper Band")
        ax.plot(lowerband, label = "Lower Band")
    #moves the lengend box out of the way
        plt.legend(bbox_to_anchor=(.45,.9),bbox_transform=plt.gcf().transFigure)
    #unclear! what io does
        io = StringIO()
    #saves the fig in png format
        fig.savefig(io, format = 'png')
    #unclear! how the encode and decode work but it's required to make it run
        data = io.getvalue().encode('base64').decode('utf8')
    #creates function that gets links from soup_str
        def links():
            #attempt to build funtion that can pull news from all sites using dict
            def meta_scrape(symbol):
                site_specific = {}
            def si(symbol):
            #!
                url = "http://www.streetinsider.com/stock_lookup.php?LookUp=Get+Quote&q=%s"%symbol
                page = requests.get(url,headers = headers)
                soup = bs4.BeautifulSoup(page.text,"lxml")
                links = soup.find_all("a",{"class":"story_title"})
                si_links_names = []
                for i in links[0:3]:
                    si_links_names.append([i.get('href'),i.text])
                print si_links_names
                return si_links_names


            def fool(symbol):
                url = "http://www.fool.com/quote/%s"%symbol
                page = requests.get(url)
                soup = (bs4.BeautifulSoup(page.text,'lxml'))
                links = soup.find_all("a",{"class":"article-link"})
                fool_links_names = []
                for i in links[0:3]:
                    fool_links_names.append([i.get('href'),i.text])
                return fool_links_names

            def seeking_alpha(symbol):
                seekingalpha = "http://seekingalpha.com/symbol/%s/news"%symbol.upper()
                page = requests.get(seekingalpha,headers = headers)
                soup= (bs4.BeautifulSoup(page.text,"lxml"))
                links = soup.find_all("a", {"class":"market_current_title"})
                sa_links_names = []
                for i in links[0:3]:
                    sa_links_names.append([i.get('href'),i.text])
                return  sa_links_names

            def market_watch(symbol):
                page = requests.get('http://www.marketwatch.com/investing/stock/%s/news'%symbol)
                soup = (bs4.BeautifulSoup(page.text,'lxml'))
                a = soup.find_all("li", {"class":"fnewsitem"})
                mw_links_names = []
                for i in a[0:3]:
                    x = i.find_all('a')
                    for y in x:
                        mw_links_names.append([y.get('href'),y.text])
                    print mw_links_names
                return mw_links_names

            return si(symbol = symbol),fool(symbol = symbol),seeking_alpha(symbol = symbol),market_watch(symbol = symbol)
        si,fool,seeking_alpha,market_watch = links()

        print len(si),len(fool),len(seeking_alpha),len(market_watch)
        statements = [index,short]
        print 4
        alert = Tech(symbol)
        alert_data = []
        if alert.signals() == True:
            alert_data.append(alert.rsi())
            alert_data.append(alert.slow_stoch())
        else:
            print "ERROR"
            alert_data = None


        # gets the ip address needs to be used in live version to track usage  #ip = request.remote_addr
        return render_template('index.html',alert = alert_data,picture = data ,statements = statements  ,market_watch = market_watch,seeking_alpha = seeking_alpha,     fool = fool,si = si,guru_info = guru_info,whale_change = whale_change)


def error_page_incorrect_symbol():
    return render_template('error.html')