import multiprocessing
import requests
import timeit
from fake_useragent import UserAgent
headers = {"User-Agent":UserAgent().chrome}
import re
import requests
import bs4
import time


def si(symbol):
    page = requests.get("http://www.streetinsider.com/stock_lookup.php?LookUp=Get+Quote&q=%s"%symbol,headers = headers)
    soup = bs4.BeautifulSoup(page.text,"lxml")
    links = soup.find_all("a",{"class":"story_title"})
    si_links_names = []
    for i in links[0:3]:
        si_links_names.append([i.get('href'),i.text])
    print si_links_names
	
def fool(symbol):
    url = "http://www.fool.com/quote/%s"%symbol
    page = requests.get(url)
    soup = (bs4.BeautifulSoup(page.text,'lxml'))
    links = soup.find_all("a",{"class":"article-link"})
    fool_links_names = []
    for i in links[0:3]:
        fool_links_names.append([i.get('href'),i.text])
    print fool_links_names
	
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

    print  mw_links_names

	
def links():
	si('aapl')
	fool('aapl')
	seeking_alpha("aapl")
	market_watch("aapl")
	
	

start = timeit.default_timer()

links()

stop = timeit.default_timer()
time.sleep(15)
print "Iter-time : %s"%(stop - start)

start2 = timeit.default_timer()
if __name__ == '__main__':
	
	jobs = []
	
	p = multiprocessing.Process(target=links)
	jobs.append(p)
	p.start()
stop2 = timeit.default_timer()
print "multi-time : %s"%(stop2-start2)