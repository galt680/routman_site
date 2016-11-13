try:
    import quandl as q
except:
    import Quandl as q
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests,bs4
from lxml import html
from mv import VIX
import re
from passwords import auth
###
#get the Total Call and Put ratios and equity Put/Call ratio
Total_Call = q.get('CBOE/TOTAL_PC',authtoken = auth)['Total Call Volume']
Total_Put  = q.get('CBOE/TOTAL_PC',authtoken = auth)['Total Put Volume']
Equity_PC = q.get('CBOE/EQUITY_PC',authtoken = auth)['P/C Ratio']
#create dataframe to make make the total Put/Call ratio from its individual components.
d = {
    'EC':Total_Call,
    'EP':Total_Put
}
d = pd.DataFrame(d)
#make the Total put/call ratio
Total_Ratio = d['EP']/d['EC']

def convert_string(string):
    potential_negative= re.findall(r'[\+\-]',string)#[0]
    number = re.findall(r'\d+\.?\d+',string)[0]
    number = float(number)

    if '-' in potential_negative:
        return number*-1
    else:
        return number

#get the page of AAII survey information
page = requests.get('http://www.aaii.com/sentimentsurvey')
#parse it to make sure its in format
soup = bs4.BeautifulSoup(page.text,'lxml')
#put in html
tree = html.fromstring(page.content)
#get the xpaths and pull down the info strip out the percentage signs convert the raw number to floats the change is a string

bullish = float(tree.xpath('''//*[@id="page_content"]/div/div/div[1]/div/div[8]/div[2]/text()''')[0].strip('%'))
bullish_change = convert_string(str(tree.xpath('//*[@id="page_content"]/div/div/div[1]/div/div[10]/text()')[0]))
bullish_average = float((tree.xpath('//*[@id="page_content"]/div/div/div[1]/div/div[5]/strong/text()')[0]).strip('%'))

bearish = float(tree.xpath('''//*[@id="page_content"]/div/div/div[1]/div/div[26]/div[2]/text()''')[0].strip('%'))
bearish_change = convert_string(str(tree.xpath('''//*[@id="page_content"]/div/div/div[1]/div/div[28]/text()''')[0].strip('%')))
bearish_average = float((tree.xpath('''//*[@id="page_content"]/div/div/div[1]/div/div[23]/strong/text()''')[0]).strip('%'))

neutral = float(tree.xpath('''//*[@id="page_content"]/div/div/div[1]/div/div[17]/div[2]/text()''')[0].strip('%'))
neutral_change = convert_string(str(tree.xpath('''//*[@id="page_content"]/div/div/div[1]/div/div[19]/text()''')[0].strip('%')))
neutral_average = float(tree.xpath('''//*[@id="page_content"]/div/div/div[1]/div/div[14]/strong/text()''')[0].strip('%'))
# create a list of all the values
AAII = [bullish,bullish_change,bullish_average,bearish,bearish_change,bearish_average,neutral,neutral_change,neutral_average]

# repeat what was done with AAII with NAAIM exposure
page = requests.get('http://www.naaim.org/programs/naaim-exposure-index/')
soup = bs4.BeautifulSoup(page.text,'lxml')
tree = html.fromstring(page.content)
naaim = tree.xpath('/html/body/div[2]/div/div/div[3]/p[5]/text()')
naaim = float(naaim[0])

#make function that takes series and length and returns moving average of length length
def moving_average_ratio(index,length):
    moving_average = index.rolling(window = length, center = False).mean()
    return float(moving_average.tail(1))
total_ratio = moving_average_ratio(Total_Ratio,10)
Equity = moving_average_ratio(Equity_PC,3)
tot, eq = total_ratio, Equity

#create function that determines if Bittlles various measurments are in bullish, bearish or neutral territory.
def bittles_levels(tot = tot, eq = eq,VIX = VIX):
    #create a dict for bittles inidciators and their respecitve levels.
    levels = {
    'tot':[tot,(.95>tot),(.8<tot),'The 10 Day MA of the Total Put/Call ratio is %s%% this is '%str(round(tot,2))],
    'eq':[eq,(.7>eq),(.6<eq),'The 3 Day MA of the Equity Put/Call ratio is %s%% this is '%str(round(eq,2))],
    'VIX':[VIX[-1],(VIX[-1]>23),(VIX[-1]<16),'The VIX is at %s this is '%str(VIX[-1])],
    'AAII':[AAII,(AAII[3]>AAII[0]),(AAII[0]>= 2*(AAII[3])),("The AAII bulls are at %s, the bears are at %s, the neutral are at %s. Overall this is "    %(AAII[0],AAII[3],AAII[6]))],
    "NAAIM":[naaim,(naaim<30),(naaim>70),'The exposure of NAAIM members is %s this is'%(str(naaim))]
    }
    # create function that iterates over dict and prints statement depnding on level
    def thresh(levels):
        statements = []
        for key in levels:
            if levels[key][1]:
                statements.append(levels[key][3]+'bullish.')
            elif levels[key][2]:
                statements.append(levels[key][3] + ' bearish.')
            else:
                statements.append(levels[key][3] + ' neutral.')
        return statements
    # print statements[0]
    # print statements[1]
    # print statements[2]
    # print statements[3]
    # print statements[4]
    a = thresh(levels)
    return a
if __name__ == "__main__":
    bittles_levels()