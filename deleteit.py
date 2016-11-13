import sqlite3 as lite
import holidays
import datetime
con = lite.connect('IMP_VOL_TABLE.db')
cur = con.cursor()
cur.execute("SELECT * FROM HISTORICAL_VOL order by DAY DESC")
dict = {}
for i in cur.fetchall():
    if str(i[1]) not in dict:
        dict[str(i[1])] = [i[2]]
    else:
        if len(dict[str(i[1])]) < 3:
            dict[str(i[1])].append(i[2])
        else:
            pass

def get_percent(symbol):
    return (dict[symbol][0]-dict[symbol][2])/dict[symbol][2]
def market_day():
    today = ((datetime.datetime.today()))
    print today.isoweekday()
    not_holiday = today not in holidays.UnitedStates()
    isntweekend = today.isoweekday()
    if not_holiday and (isntweekend != 7) and (isntweekend != 1):
        return True
    else:
        return False
print market_day()
