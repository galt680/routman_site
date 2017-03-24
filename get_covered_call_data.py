import re
import bs4
import requests
import datetime
from time import sleep
from random import uniform
from dateutil import parser
from fake_useragent import UserAgent

headers = {"User-Agent":UserAgent().random}


def get_pages_to_visit(symbol):
    '''This function gets and parses the list of strikes from a NASDAQ options
       page, this page is calls only and only has monthly options'''
    url = 'http://www.nasdaq.com/symbol/%s/option-chain?dateindex=0&callput=call&expir=stan'%symbol
    r =requests.get(url,headers = headers).text
    soup = bs4.BeautifulSoup(r,'lxml')
    pages_to_visit  = {}
    try:
        list_of_strikes = [date_block.split() for date_block  in [elem.text for elem in 
                        (soup.find_all('div',{'id':'OptionsChain-dates'}))][0].split('|')[:-2]]
        today = datetime.datetime.now()
        strikes = []
        for raw_date in [unparsed_date[:1]+['18']+unparsed_date[1:]for unparsed_date in list_of_strikes]:
            strikes.append(parser.parse(' '.join(raw_date)))
        for exp_date in strikes:
            if today.month + 1< exp_date.month:
                if (exp_date -today).days < 180:
                    pages_to_visit[strikes.index(exp_date)] = list_of_strikes[strikes.index(exp_date)][0]
    except Exception as e:
        print e
    return pages_to_visit
    
    #73.213.147.83
    
def get_data_to_deliver(list_of_symbols):
    price = {}
    master = {}
    for symbol in list_of_symbols:
        master[symbol] = {}
        for date_index in get_pages_to_visit(symbol).iteritems():
            try:
                sleep(uniform(.05,2))
                strikes_and_premium ={}
                url = 'http://www.nasdaq.com/symbol/%s/option-chain?dateindex=%s&callput=call&expir=stan'%(symbol,date_index[0])
                r =requests.get(url,headers = headers).text
                soup = bs4.BeautifulSoup(r,'lxml')
                price[symbol] =  float(soup.find_all('div',{'class':"qwidget-dollar"})[0].text.replace('$',''))
                rows_of_data = ([piece.text.split() for piece in soup.find('div',{'class':'OptionsChain-chart borderAll thin'}).find_all('tr') ])[1:]
            except IndexError:
                print symbol
            try:
                for row_in_chain in rows_of_data:

                    string = ' '.join(row_in_chain)
                    strike = (float((re.findall(r'''%s (\d+\.?\d?) (\d+?\.\d+)'''%symbol.upper(),string)[0])[0]))
                    premium = (re.findall(r'''%s (\d+\.?\d?) (\d+?\.\d+)'''%symbol.upper(),string)[0])[1]
                    strikes_and_premium[strike] = premium
                strike = min(strikes_and_premium.keys(),key  = lambda y :abs(y-price[symbol]/.95))
                premium = float(strikes_and_premium[min(strikes_and_premium.keys(),key  = lambda y :abs(y-price[symbol]/.95))])
                master[symbol][date_index[1]] = {5:[strike,premium]}
                strike = min(strikes_and_premium.keys(),key  = lambda y :abs(y-price[symbol]/.90))
                premium = float(strikes_and_premium[min(strikes_and_premium.keys(),key  = lambda y :abs(y-price[symbol]/.90))])        
                master[symbol][date_index[1]][10] = [strike,premium]
            except Exception as e:
                print symbol,e
    return master
    
if __name__ == "__main__":
    syms = (raw_input("ENTER SYMBOLS SEPERATED BY COMMAS: ")).split(',') 
    master = get_data_to_deliver(syms)
    for symbol in master:
        print '\n'
        for month, values in master[symbol].iteritems():
            for diff,stuff in values.iteritems():
                print symbol,month,diff,stuff