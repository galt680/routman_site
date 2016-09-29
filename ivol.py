from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import time
import timeit
import os


start = timeit.default_timer()


if os.path.exists('C:\\Users\\Yasch'):
	caps = DesiredCapabilities.FIREFOX
	caps["marionette"] = True
	caps["binary"] = "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
	browser = webdriver.Firefox(capabilities=caps)
else:
	from pyvirtualdisplay import Display
	display = Display(visible=0, size=(800, 600))
	display.start()



browser.get('https://www.ivolatility.com/login.j')
username = browser.find_element_by_name('username')
username.send_keys('galt680')
password = browser.find_element_by_name('password')
password.send_keys('85057047')
browser.find_element_by_css_selector('.btn.btn-custom.btn-login').click()
time.sleep(3)


con = lite.connect('IMP_VOL_TABLE.db')
cur = con.cursor()

cur.execute('update IMP_VOL set YESTERDAY_VALUE = TODAY_VALUE')
for i in sp500:
    try:
        url = "http://www.ivolatility.com/options.j?ticker=%s&R=0&top_lookup__is__sent=1"%i['symbol']
        browser.get(url)
            try:
        current = float(browser.find_element_by_xpath("/html/body/div/div[3]/div[2]/table[1]/tbody/tr[3]/td[1]/table[2]/tbody/tr[9]/td[2]/font").text.strip('%'))
            except:
                print i['symbol']
                pass
        cur.execute("""update IMP_VOL set TODAY_VALUE = %s where name = '%s'"""%(current,i['symbol']))
        time.sleep(random.uniform(0,1.5))
    except:
        pass
con.commit()
con.close()
browser.find_element_by_xpath('/html/body/nav/div/div[1]/span/span[1]/a/span').click()
time.sleep(3)
browser.find_element_by_xpath('/html/body/nav/div/div[1]/span/span[1]/div/ul/li[6]/a/i').click()

stop = timeit.default_timer()
try:
    print "Task took %s minutes"%(int(stop - start)/60)
except:
    pass
driver.quit()
try:
	display.stop()
except:
	pass