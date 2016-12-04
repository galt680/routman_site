import pickle
from flask import render_template,request	


def watchlist_landing_page():
	try:
		pickle_in = (open("symbols_list.pickle","rb"))
		symbol_list = sorted(pickle.load(pickle_in))
		print symbol_list
		return render_template('input.html',symbol_list = (symbol_list))

	except Exception as e:
		print e
		return render_template('input.html')


def add_symbol_2017():
	try:
		pickle_in = open("symbols_list.pickle","rb")
		symbol_list = (pickle.load(pickle_in))
		
		symbol = request.form['symbol']
		for i in symbol.split(','):
			print type(str(i))
			symbol_list.append(i.upper().strip().strip("'"))
	except Exception as e:
		print e
		symbol = request.form['symbol']
		symbol_list = symbol.split(',')
	pickle_out = open("symbols_list.pickle","wb")
	pickle.dump(symbol_list,pickle_out)
	pickle_out.close()	
	return watchlist_landing_page()
	

def delete_symbol_2017():
	try:
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
	
		pickle_out = open("symbols_list.pickle","wb")
		pickle.dump(symbol_list,pickle_out)
		pickle_out.close()
		return watchlist_landing_page()
	except Exception as e:
		print e
		return watchlist_landing_page()