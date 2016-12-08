import sqlite3 as lite
from flask import Flask,request,render_template,url_for

app = Flask(__name__)



@app.route('/',methods = ['GET','POST'])
def homepage():
	con = lite.connect("watchlist.db")
	cur = con.cursor()
	try:
		cur.execute("SELECT name FROM sqlite_master where type='table'")
		table_list = []
		for table in cur.fetchall():
			table_list.append(str(table[0]))
	except:
		pass
	# active_watchlist = request.form['active_watchlist']
	# print active_watchlist
	print table_list
	return render_template("sql_input.html",table_list = table_list)
	

@app.route("/create_watchlist",methods = ['GET','POST'])
def create_watchlist():
	con = lite.connect("watchlist.db")
	cur = con.cursor()
	watchlist = request.form['symbol']
	cur.execute("CREATE TABLE IF NOT EXISTS %s(NAME TEXT)"%(watchlist))
	con.commit()
	con.close()
	return homepage()
	
@app.route("/add_symbol",methods = ['GET','POST'])
def add_sql():
	return homepage()
	
	

@app.route("/delete_symbol",methods = ['GET','POST'])
def delete_sql():
	pass

if __name__ == "__main__":
	app.run(debug = True)
