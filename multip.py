'''Attempt to start a new process before the current process
            has finished its bootstrapping phase.

            This probably means that you are on Windows and you have
            forgotten to use the proper idiom in the main module:

                if __name__ == '__main__':
                    freeze_support()
                    ...

            The "freeze_support()" line can be omitted if the program
            is not going to be frozen to produce a Windows executable.

            Attempt to start a new process before the current process
            has finished its bootstrapping phase.

            This probably means that you are on Windows and you have
            forgotten to use the proper idiom in the main module:

                if __name__ == '__main__':
                    freeze_support()
                    ...

            The "freeze_support()" line can be omitted if the program
            is not going to be frozen to produce a Windows executable.

            Attempt to start a new process before the current process
            has finished its bootstrapping phase.

            This probably means that you are on Windows and you have
            forgotten to use the proper idiom in the main module:

                if __name__ == '__main__':
                    freeze_support()
                    ...

            The "freeze_support()" line can be omitted if the program
            is not going to be frozen to produce a Windows executable.

            Attempt to start a new process before the current process
            has finished its bootstrapping phase.

            This probably means that you are on Windows and you have
            forgotten to use the proper idiom in the main module:

                if __name__ == '__main__':
                    freeze_support()
                    ...

            The "freeze_support()" line can be omitted if the program
            is not going to be frozen to produce a Windows executable.'''
from concurrent.futures import ProcessPoolExecutor
import time
import timeit
def mult():
	time.sleep(5)
#	  return q.put((1,2))
	return 20

def div():
	time.sleep(5)
	return 30
def take_time():
	time.sleep(5)
	



try:
	
	if __name__ == '__main__':
		start1 = timeit.default_timer()
		div()
		mult()
		take_time()
		stop1 = timeit.default_timer()
		print "Linear-Time : %s"%(stop1 - start1)
		start = timeit.default_timer()
		executor = ProcessPoolExecutor(max_workers=1000)
		funcs = [mult,div,take_time]
		futures = [executor.submit(f) for f in funcs]
		results = [future.result() for future in futures]
		print results
		stop = timeit.default_timer()
		print "Mult-Time : %s seconds"%(stop - start)
except Exception as e:
	print e
	
# from concurrent.futures import ProcessPoolExecutor

# executor = ProcessPoolExecutor(max_workers=4)
# funcs = [mult,div]
# futures = [executor.submit(f) for f in funcs]
# a = [future.result() for future in futures]
# print a

'''import multiprocessing
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
	return	sa_links_names

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
	for i in range(5):
		p = multiprocessing.Process(target=worker, args=('aapl',))
		jobs.append(p)
		p.start()
stop2 = timeit.default_timer()
print "multi-time : %s"%(stop2-start2)'''