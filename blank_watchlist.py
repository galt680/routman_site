import pickle
from flask import render_template,request


def blank_watchlist_landing_page():
    try:
        try:
            pickle_in = (open("/home/yaschaffel/mysite/blank_watchlist.pickle","rb"))
        except:
            pickle_in = open("blank_watchlist.pickle","rb")
        symbol_list = sorted(pickle.load(pickle_in))
        print symbol_list
        return render_template('input_blank.html',symbol_list = (symbol_list))
    except Exception as e:
        print e
        return render_template('input_blank.html')


def add_symbol_blank():
    try:
        try:
            pickle_in = (open("/home/yaschaffel/mysite/blank_watchlist.pickle","rb"))
        except:
            pickle_in = open("blank_watchlist.pickle","rb")
        symbol_list = (pickle.load(pickle_in))

        symbol = request.form['symbol']
        for i in symbol.split(','):
            print type(str(i))
            symbol_list.append(i.upper().strip().strip("'"))
        try:
            pickle_out = (open("/home/yaschaffel/mysite/blank_watchlist.pickle","wb"))
            print 1
        except Exception as e:
            print e
            pickle_out = open("blank_watchlist.pickle","wb")
    except Exception as e:
        print e
        symbol = request.form['symbol']
        symbol_list = symbol.split(',')
        try:
            pickle_out = (open("/home/yaschaffel/mysite/blank_watchlist.pickle","wb"))
            print 1
        except Exception as e:
            print e
            pickle_out = open("blank_watchlist.pickle","wb")
    pickle.dump(symbol_list,pickle_out)
    pickle_out.close()
    return blank_watchlist_landing_page()


def delete_symbol_blank():
    try:
        try:
            pickle_in = (open("/home/yaschaffel/mysite/blank_watchlist.pickle","rb"))
        except:
            pickle_in = open("blank_watchlist.pickle","rb")
        symbol_list = (pickle.load(pickle_in))
        symbol = str(request.form['symbol'])
        print type(symbol)
        for i in symbol.split(','):
            if i in symbol_list:
                i = i.upper()
                while i in symbol_list:
                    symbol_list.remove((i))
            else:
                pass

        try:
            pickle_out = (open("/home/yaschaffel/mysite/blank_watchlist.pickle","wb"))
        except:
            pickle_out = open("blank_watchlist.pickle","wb")
        pickle.dump(symbol_list,pickle_out)
        pickle_out.close()
        return watchlist_landing_page()
    except Exception as e:
        print e
        return blank_watchlist_landing_page()