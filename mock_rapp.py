from flask import Flask,request,render_template,url_for
from watchlist_2017 import watchlist_landing_page,add_symbol_2017,delete_symbol_2017
import sqlite3 as lite
from blank_watchlist import blank_watchlist_landing_page,add_symbol_blank,delete_symbol_blank



app = Flask(__name__)


def show_symbols_from_selected_watchlist():
    try:
        name = request.form['days']
    except:
        pass
    con = lite.connect("watchlists.db")
    cur = con.cursor()
    symbol_list = [i[0] for i in cur.execute("SELECT Name FROM %s  "%'TRY1')]
    # line = str(' '.join(i[0] for i in symbols))
    # print line
    return render_template('symbols_from_watchlist.html',symbol_list = symbol_list)

@app.route('/symbols_2017', methods = ["GET","POST"])   
def symbols_2017():
    return watchlist_landing_page()
    
@app.route('/symbols_blank', methods = ["GET","POST"])  
def symbols_blank():
    return blank_watchlist_landing_page()
    
@app.route("/add_symbol_blank", methods = ["GET","POST"])
def symbol_blank_add():
    return add_symbol_blank()
    
@app.route("/delete_symbol_blank", methods = ["GET","POST"])
def symbol_blank_delete():
    return delete_symbol_blank()    
    
@app.route("/watchlist_landing_page", methods = ["GET","POST"])
def landing():
    con = lite.connect("watchlists.db")
    cur = con.cursor()
    return render_template("watchlist_landing_page.html",database = [watchlist[0] for watchlist in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()])

@app.route("/selected_watchlist", methods  = ["GET","POST"])
def selected_watchlist():
    return show_symbols_from_selected_watchlist()

@app.route("/delete_symbol", methods  = ["GET","POST"])
def delete_symbol():
    name = request.form['symbol']
    con = lite.connect("watchlists.db")
    cur = con.cursor()
    cur.execute("DELETE FROM TRY1 WHERE NAME = '%s'"%name)
    con.commit()
    symbol_list = [i[0] for i in cur.execute("SELECT Name FROM %s  "%'TRY1')]
    print name
    return show_symbols_from_selected_watchlist()
	
@app.route("/add_symbol", methods  = ["GET","POST"])
def add_symbol():
    name = request.form['symbol']
    con = lite.connect("watchlists.db")
    cur = con.cursor()
	for individual_symbol in name.spit(','):
		cur.execute("INSERT INTO TRY1 (NAME, USER ) VALUES (?,?)", (individual_symbol,'routman'))
    con.commit()
    symbol_list = [i[0] for i in cur.execute("SELECT Name FROM %s  "%'TRY1')]	
    print name
    return show_symbols_from_selected_watchlist()

if __name__ == "__main__":
    app.run(debug = True)
