from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import timeit
import os
import sqlite3 as lite
from passwords import ivol

import finsymbols
sp500 = finsymbols.get_sp500_symbols()
import random


start = timeit.default_timer()


if os.path.exists('C:\\Users\\Yasch'):
	print "home"
	caps = DesiredCapabilities.FIREFOX
	caps["marionette"] = True
	caps["binary"] = "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
	driver = webdriver.Firefox(capabilities=caps)
	con = lite.connect('IMP_VOL_TABLE.db')
else:
    print "remote"
    con = lite.connect('/home/yaschaffel/mysite/IMP_VOL_TABLE.db')
    from pyvirtualdisplay import Display
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Firefox()


# def check_change():

driver.get('https://www.ivolatility.com/login.j')
username = driver.find_element_by_name('username')
username.send_keys('yaschaffel')
password = driver.find_element_by_name('password')
password.send_keys(ivol)
driver.find_element_by_css_selector('.btn.btn-custom.btn-login').click()
time.sleep(3)



	# driver.get('http://www.ivolatility.com/options.j?ticker=afl&R=0&top_lookup__is__sent=1')
	# aapl_current = float(driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/table[1]/tbody/tr[3]/td[1]/table[2]/tbody/tr[9]/td[2]/font").text.strip('%'))
	# driver.get('http://www.ivolatility.com/options.j?ticker=afl&R=0&top_lookup__is__sent=1')
	# afl_current = float(driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/table[1]/tbody/tr[3]/td[1]/table[2]/tbody/tr[9]/td[2]/font").text.strip('%'))
	# if (aapl_current != 26.76) and (afl_current != 15.39):
		# print datetime.datetime.now()
	# else:
		# print "Nothing Changed"
	# print "logging out"
	# driver.get('http://www.ivolatility.com/home.j?logoff=1')
	# driver.close()



cur = con.cursor()

cur.execute('update IMP_VOL_TABLE set YESTERDAY_VALUE = TODAY_VALUE')
for i in sp500:
	try:
		url = "http://www.ivolatility.com/options.j?ticker=%s&R=0&top_lookup__is__sent=1"%i['symbol']
		driver.get(url)
		try:
			current = float(driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/table[1]/tbody/tr[3]/td[1]/table[2]/tbody/tr[9]/td[2]/font").text.strip('%'))
		except:
			print i['symbol']
			pass
		cur.execute("""update IMP_VOL_TABLE set TODAY_VALUE = %s where name = '%s'"""%(current,i['symbol']))
		print "%s success The value is %s"%(i['symbol'],current)
		time.sleep(random.uniform(0,1.25))
	except:
		pass
con.commit()
con.close()
# driver.find_element_by_xpath('/html/body/nav/div/div[1]/span/span[1]/a/span').click()
# time.sleep(3)
# driver.find_element_by_xpath('/html/body/nav/div/div[1]/span/span[1]/div/ul/li[6]/a/i').click()

stop = timeit.default_timer()
driver.get('http://www.ivolatility.com/home.j?logoff=1')
driver.close()
driver.quit()
display.stop()
stop = timeit.default_timer()
try:
	print "Task took %s minutes"%(int(stop - start)/60)
except:
	pass
# driver.quit()
# try:
	# display.stop()
# except:
	# pass