from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import timeit
import os
import sqlite3 as lite
from passwords import ivol
import random
import finsymbols
import datetime
sp500 = finsymbols.get_sp500_symbols()
random.shuffle(sp500)




def market_day():
    today = ((datetime.datetime.today()- datetime.timedelta(hours = 6)))
    not_holiday = today not in holidays.UnitedStates()
    isntweekend = today.isoweekday()
    if not_holiday and (isntweekend != 7) and (isntweekend != 6):
        return True
    else:
        return False

start = timeit.default_timer()

if market_day():
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




    driver.get('https://www.ivolatility.com/login.j')
    username = driver.find_element_by_name('username')
    username.send_keys('yaschaffel')
    password = driver.find_element_by_name('password')
    password.send_keys(ivol)
    driver.find_element_by_css_selector('.btn.btn-custom.btn-login').click()
    time.sleep(3)






    cur = con.cursor()

    cur.execute('update IMP_VOL_TABLE set YESTERDAY_VALUE = TODAY_VALUE')
    cur.execute("CREATE TABLE IF NOT EXISTS HISTORICAL_VOL(DAY DATE,NAME TEXT,VOL INT)")
    date = (datetime.datetime.today()- datetime.timedelta(days = 1)).strftime('%Y-%m-%d')
    for i in sp500:
        try:
            url = "http://www.ivolatility.com/options.j?ticker=%s&R=0&top_lookup__is__sent=1"%i['symbol']
            driver.get(url)
            try:
                current = float(driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/table[1]/tbody/tr[3]/td[1]/table[2]/tbody/tr[9]/td[2]/font").text.strip('%'))
            except:
                print i['symbol']
                pass
            if market_day():
                cur.execute("""update IMP_VOL_TABLE set TODAY_VALUE = %s where name = '%s'"""%(current,i['symbol']))
                cur.execute("INSERT INTO HISTORICAL_VOL(DAY,NAME,VOL) VALUES (?,?,?)",(date,i['symbol'],current))
            else:
                pass
            print "%s success The value is %s"%(i['symbol'],current)
            time.sleep(random.uniform(0,1.25))
        except:
            pass
    con.commit()
    con.close()


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
else:
    pass