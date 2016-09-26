import requests
import bs4
import re
import talib as ta
import numpy as np
from live_tech import Tech


# we can now start Firefox and it will run inside the virtual display
from selenium import webdriver
import re
import time
driver = webdriver.Firefox()
driver.get('https://www.ivolatility.com/login.j')
username = driver.find_element_by_name('username')
username.send_keys('galt680')
print "Entered Username"
password = driver.find_element_by_name('password')
password.send_keys('85057047')
print "Entered Password"
driver.find_element_by_css_selector('.btn.btn-custom.btn-login').click()
print "logged in"
time.sleep(3)
symbol = str(raw_input("Enter a symbol:"))
url = "http://www.ivolatility.com/options.j?ticker=%s&R=0&top_lookup__is__sent=1"%symbol
driver.get(url)
current = float(driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/table[1]/tbody/tr[3]/td[1]/table[2]/tbody/tr[9]/td[2]/font").text.strip('%'))
week = float(driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/table/tbody/tr[3]/td/table[2]/tbody/tr[9]/td[3]/font").text.strip('%'))
month = float(driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/table/tbody/tr[3]/td/table[2]/tbody/tr[9]/td[4]/font").text.strip('%'))
hi = (driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/table/tbody/tr[3]/td/table[2]/tbody/tr[9]/td[5]/font").text.strip('%'))
hi = float(re.findall(r"""\d+\.\d+""",hi)[0])
low = (driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/table/tbody/tr[3]/td/table[2]/tbody/tr[9]/td[6]/font").text.strip('%'))
low = float(re.findall(r"""\d+\.\d+""",low)[0])
print current
print current/((week + month + (hi) + low))

print "logging out"
driver.find_element_by_xpath('/html/body/nav/div/div[1]/span/span[1]/a/span').click()
time.sleep(3)
driver.find_element_by_xpath('/html/body/nav/div/div[1]/span/span[1]/div/ul/li[6]/a/i').click()
print "logged out"



# def hourly_data():
	# symbol = str(raw_input("Enter a symbol:")).upper()

	# url = "https://www.google.com/finance/getprices?i=60&p=1d&f=c,o,h,l&df=cpct&q=%s"%(symbol)

	# page = requests.get(url).text

	# prices = re.findall(r'''\n(\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+)''',page)

	# most_recent_close = float(prices[-1].split(',')[0])
	# most_recent_high = float(prices[-1].split(',')[1])
	# most_recent_low = float(prices[-1].split(',')[2])
	# most_recent_open = float(prices[-1].split(',')[3])
	
	
	# url = "https://www.google.com/finance/getprices?i=3600&p=10d&f=c,o,h,l&df=cpct&q=%s"%(symbol)
	# page = requests.get(url).text

	# prices = re.findall(r'''\n(\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+)''',page)
	# o = []
	# h = []
	# l = []
	# c = []
	# for i in prices:
		# c.append(float(i.split(",")[0]))
		# h.append(float(i.split(',')[1]))
		# l.append(float(i.split(',')[2]))
		# o.append(float(i.split(',')[3]))
	# if most_recent_close == c[-1]:
		# pass
	# else:
		# c.append(most_recent_close)
	# if most_recent_open == o[-1]:
		# pass
	# else:
		# o.append(most_recent_open)
	# if most_recent_high == h[-1]:
		# pass
	# else:
		# h.append(most_recent_high)
	# if most_recent_low == l[-1]:
		# pass
	# else:
		# l.append(most_recent_low)		
	# print "close"
	# print c[-5:]
	# print "high"
	# print h[-5:]
	# print "low"
	# print l[-5:]
	# print "open"
	# print o[-5:]
# hourly_data()
# real = ta.RSI(np.array(c),timeperiod = 14)

# print real[-1]

# slowk, slowd = ta.STOCH(np.array(h)	,np.array(l),np.array(c), fastk_period=10, slowk_period=10, slowk_matype=0, slowd_period=3, slowd_matype=0)
# print slowk[-1],slowd[-1]



# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.firefox.webdriver import FirefoxProfile
# import re
# import numpy as np
# import random
# from scipy import stats

# caps = DesiredCapabilities.FIREFOX


# caps["marionette"] = True
# profile = FirefoxProfile("C:\\Users\\Yasch\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\10vq47dc.default")

# caps["binary"] = "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
# driver = webdriver.Firefox(profile)
# symbol = str(raw_input("Enter a symbol:"))
# url = 'http://www.ivolatility.com/options.j?ticker=%s&R=0&top_lookup__is__sent=1'%symbol
# driver.get(url)
# current = float(driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/table[1]/tbody/tr[3]/td[1]/table[2]/tbody/tr[9]/td[2]/font").text.strip('%'))
# week = float(driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/table/tbody/tr[3]/td/table[2]/tbody/tr[9]/td[3]/font").text.strip('%'))
# month = float(driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/table/tbody/tr[3]/td/table[2]/tbody/tr[9]/td[4]/font").text.strip('%'))
# hi = (driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/table/tbody/tr[3]/td/table[2]/tbody/tr[9]/td[5]/font").text.strip('%'))
# hi = float(re.findall(r"""\d+\.\d+""",hi)[0])
# low = (driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/table/tbody/tr[3]/td/table[2]/tbody/tr[9]/td[6]/font").text.strip('%'))
# low = float(re.findall(r"""\d+\.\d+""",low)[0])


# nums = [week,month,hi,low,current]
# std = np.std(nums)
# mean = np.mean(nums)
# def attempt():
    # count = 0
    # losers = 0
    # fake_datapoints = [hi,low,current,week,month]
    # while len(fake_datapoints) < 25000:
        # mult = random.uniform(-2,2)*std
        # fake_point = mult + mean
        # if (fake_point > hi) or (fake_point < low):
            # pass
        # else:
            # fake_datapoints.append(round(fake_point,2))
    # return fake_datapoints

# fake = attempt()
# print (stats.percentileofscore(fake,current))
# driver.quit()














# options = webdriver.ChromeOptions() 
# options.add_argument("user-data-dir=C:\\Users\\Yasch\\AppData\\Local\\Google\\Chrome\\User Data") #Path to your chrome profile
# browser = webdriver.Chrome(executable_path="C:\\Users\\Yasch\\Anaconda2\\Scripts\\chromedriver.exe",chrome_options=options)
# url = "http://www.ivolatility.com/options.j?ticker=%s&R=0&top_lookup__is__sent=1"%symbol
# url = "https://mail.google.com"
# browser.get(url)
# print float(browser.find_element_by_xpath("/html/body/div/div[3]/div[2]/table[1]/tbody/tr[3]/td[1]/table[2]/tbody/tr/td/table/tbody/tr[9]/td[2]/font").text.strip('%'))
# browser.quit()



















