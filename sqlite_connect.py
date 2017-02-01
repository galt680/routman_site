import sqlite3 as lite

def connect_to_db(db_name):
    try:
        return lite.connect('/home/yaschaffel/mysite/%s.db'%db_name)
    except:
        return lite.connect('%s.db'%db_name)