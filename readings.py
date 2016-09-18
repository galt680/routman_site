from flask import Flask,request,render_template,url_for
from cStringIO import StringIO
from sentiment_ import whale_wisdom,sentiment_index,short_interest
from mv import VIX
from lxml import html
from fake_useragent import UserAgent
import matplotlib.pyplot as plt
import talib as ta
import numpy as np
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
	symbol = request.form['test']
	if (symbol == 'yds') or (symbol == 'Yds'):
		return render_template('say_yes.html')
	elif (symbol == "#ilvu"):
		return love()
	else:
		try:
		#request.form accesses the input from the myform.html page and the name is the access point from the html file

			length = request.form["length"]

		#to access some sites html to be scraped there needs to be a user-agent this creates a dict that makes a chrome specific user agent
			headers = {"User-Agent":UserAgent().chrome}

		#use a try/except to make sure that a valid symbol is present. if invalid symbol is entered it returns to original form
		#and using jinja modifies it to look for another symbol
			try:
				whale_change,guru_info = whale_wisdom(symbol)
			except:
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
				def seeking_alpha():
					seekingalpha = "http://seekingalpha.com/symbol/" + symbol.capitalize()
					page = requests.get(seekingalpha,headers = headers)
					soup_str = str(bs4.BeautifulSoup(page.text,"lxml"))
					def get_sa(soup_str = soup_str):
					#uses regex to slim down html
					#unclear! why this takes to regexes
						re1 = re.findall(r'''class="symbol_article"><a href="(.+)" ''',soup_str)
					# makes empty list to collect links as the for-loop iterates over re1 to get the pure link.
					#
						link_list = []
						for i in range(3):
					#2nd regex to finish parsing then add beggining of seekingalpha link to make functioning link
							re2 = "//www.seekingalpha.com" + re.findall(r"(.+) sasource",re1[i])[0]
							link_list.append(re2)
						return link_list
				#function to get titles of links
					def sa_names(soup_str = soup_str):
						re1 = re.findall(r'''class="symbol_article"><a href="(.+)" ''',soup_str)
						titles_list = []
						for i in range(3):
							titles = (re.findall(r'''sasource="qp_latest">(.+)</a>''',re1[i])[0].decode('utf-8'))
							titles_list.append(titles)
						return titles_list
					return zip(get_sa(),sa_names())

				def market_watch():
					page = requests.get('http://www.marketwatch.com/investing/fund/%s/news'%symbol)
					soup = str(bs4.BeautifulSoup(page.text,'lxml'))
					def get_mw():
						re1 = re.findall(r'''<p> <a href="(/story/.+)"''',soup)
						links = []
						for i in range(3):
							links.append('//marketwatch.com' + re1[i])
						return links
					def mw_names():
						re1 = re.findall(r'''<p> <a href="/story/.+">(.+)</a>''',soup)
						titles_list = []
						for i in range(3):
							titles_list.append(re1[i])
						for i in range(len(titles_list)):
							titles_list[i] = titles_list[i].decode('utf-8')
						return titles_list
					return zip(get_mw(),mw_names())

				def fool():
					print symbol
					page = requests.get("http://www.fool.com/quote/%s"%symbol)
					soup = str(bs4.BeautifulSoup(page.text,'lxml'))
					def get_fool():
						link_list = []
						for i in range(3):
							link_list.append('/'+(re.findall(r'''<a class="article-link" href="(.+).aspx''',soup)[i]))
						return link_list
					def fool_names():
						names_list = []
						for i in range(3):
							names_list.append(re.findall(r'''<a class="article-link" href=.+\.aspx">(.+)<''',soup)[i])
						for i in range(len(names_list)):
							names_list[i] = names_list[i].decode('utf-8')
						return names_list
					return zip(get_fool(),fool_names())

				def si():
					page = requests.get("http://www.streetinsider.com/stock_lookup.php?LookUp=Get+Quote&q=%s"%symbol,headers = headers)
					soup_str = str(bs4.BeautifulSoup(page.text,"lxml"))
					soup = (bs4.BeautifulSoup(page.text,"lxml"))
					major = str(soup.find(id = "content_all"))
					def si_links():
						links = re.findall(r'''href="(.+)"''',major)
						print len(links)
						print links[0]
						for i in range(3):
							links[i] = '//streetinsider.com/' + links[i]
						links_list = []
						for i in range(3):
							links_list.append(links[i])
						return links_list
					def si_names():
							names = list(re.findall(r'''.html">(.+)</a''',major)[:3])
							for i in range(len(names)):
								names[i] = names[i].decode('utf-8')
							return names
					return zip(si_links(),si_names())
				return seeking_alpha(),market_watch(),fool(),si()
			seeking_alpha,market_watch,fool,si = links()
			print len(market_watch)
			statements = [index,short]
			alert = Tech(symbol)
			alert_data = []
			if alert.signals() == True:
				alert_data.append(alert.rsi())
				alert_data.append(alert.slow_stoch())
			else:
				alert_data = None


			# gets the ip address needs to be used in live version to track usage  #ip = request.remote_addr
			return render_template('index.html',alert = alert_data,picture = data ,statements = statements	,seeking_alpha = seeking_alpha,market_watch = market_watch,fool = fool,si = si,guru_info = guru_info,whale_change = whale_change)

		except:
			return render_template('error.html')