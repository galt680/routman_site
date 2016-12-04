import pickle
from flask import render_template,request


def watchlist_landing_page():
    try:
        try:
            pickle_in = (open("/home/yaschaffel/mysite/symbols_list.pickle","rb"))
        except:
            pickle_in = open("symbols_list.pickle","rb")
        symbol_list = sorted(pickle.load(pickle_in))
        print symbol_list
        return render_template('input.html',symbol_list = (symbol_list))
    except Exception as e:
        print e
        return render_template('input.html')


def add_symbol_2017():
    try:
        try:
            pickle_in = (open("/home/yaschaffel/mysite/symbols_list.pickle","rb"))
        except:
            pickle_in = open("symbols_list.pickle","rb")
        symbol_list = (pickle.load(pickle_in))

        symbol = request.form['symbol']
        for i in symbol.split(','):
            print type(str(i))
            symbol_list.append(i.upper().strip().strip("'"))
        try:
            pickle_out = (open("/home/yaschaffel/mysite/symbols_list.pickle","wb"))
            print 1
        except Exception as e:
            print e
            pickle_out = open("symbols_list.pickle","wb")
    except Exception as e:
        print e
        symbol = request.form['symbol']
        symbol_list = symbol.split(',')
        try:
            pickle_out = (open("/home/yaschaffel/mysite/symbols_list.pickle","wb"))
            print 1
        except Exception as e:
            print e
            pickle_out = open("symbols_list.pickle","wb")
    pickle.dump(symbol_list,pickle_out)
    pickle_out.close()
    return watchlist_landing_page()


def delete_symbol_2017():
    try:
        try:
            pickle_in = (open("/home/yaschaffel/mysite/symbols_list.pickle","rb"))
        except:
            pickle_in = open("symbols_list.pickle","rb")
        symbol_list = (pickle.load(pickle_in))
        symbol = str(request.form['symbol'])
        print type(symbol)
        for i in symbol.split(','):
            if i in symbol_list:
                while i in symbol_list:
                    symbol_list.remove((i))
            else:
                pass

        try:
            pickle_out = (open("/home/yaschaffel/mysite/symbols_list.pickle","wb"))
        except:
            pickle_out = open("symbols_list.pickle","wb")
        pickle.dump(symbol_list,pickle_out)
        pickle_out.close()
        return watchlist_landing_page()
    except Exception as e:
        print e
        return watchlist_landing_page()