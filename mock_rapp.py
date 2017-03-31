from flask import Flask,request,render_template,url_for,session
from watchlist_2017 import watchlist_landing_page,add_symbol_2017,delete_symbol_2017
import sqlite3 as lite
from blank_watchlist import blank_watchlist_landing_page,add_symbol_blank,delete_symbol_blank



app = Flask(__name__)
app.secret_key = "super secret key"


def show_symbols_from_selected_watchlist():

    try:
        name = request.form['watchlist_name']
        print name
        session['picked_watchlist'] = name
    except Exception as e:
        print e

    print "secrert",session['picked_watchlist']
    con = lite.connect("watchlists.db")
    cur = con.cursor()
    symbol_list = [i[0] for i in cur.execute("SELECT Name FROM %s  "%session['picked_watchlist'])]
    return render_template('symbols_from_watchlist.html',symbol_list = symbol_list)

    
@app.route("/watchlist_landing_page", methods = ["GET","POST"])
def landing():
    con = lite.connect("watchlists.db")
    cur = con.cursor()
    return render_template( "watchlist_landing_page.html",database = (
							[watchlist[0] for watchlist in cur.execute(
							"SELECT name FROM sqlite_master WHERE type='table'").fetchall() 
							if not watchlist[0].startswith('_')]))

	
@app.route("/selected_watchlist", methods  = ["GET","POST"])
def selected_watchlist():
    
    return show_symbols_from_selected_watchlist()

@app.route("/delete_symbol", methods  = ["GET","POST"])
def delete_symbol():
    name = request.form['symbol']
    picked_watchlist = session['picked_watchlist']
    con = lite.connect("watchlists.db")
    cur = con.cursor()
    cur.execute("DELETE FROM %s WHERE NAME = '%s'"%(picked_watchlist,name))
    con.commit()
    symbol_list = [i[0] for i in cur.execute("SELECT Name FROM %s  "%picked_watchlist)]
    print name
    return show_symbols_from_selected_watchlist()
    
@app.route("/add_symbol", methods  = ["GET","POST"])
def add_symbol():
    name = request.form['symbol']
    picked_watchlist = session['picked_watchlist']
    con = lite.connect("watchlists.db")
    cur = con.cursor()
    for individual_symbol in name.split(','):
        cur.execute("INSERT INTO %s (NAME, USER ) VALUES (?,?)"%picked_watchlist, (individual_symbol,'routman'))
    con.commit()
    symbol_list = [i[0] for i in cur.execute("SELECT Name FROM %s  "%picked_watchlist)]   
    print name
    return show_symbols_from_selected_watchlist()

if __name__ == "__main__":
    app.run(debug = True)
