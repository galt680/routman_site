import sqlite3 as lite
from werkzeug.exceptions import HTTPException, NotFound
from flask import Flask,request,render_template,url_for,session
from watchlist_2017 import watchlist_landing_page,add_symbol_2017,delete_symbol_2017
from blank_watchlist import blank_watchlist_landing_page,add_symbol_blank,delete_symbol_blank



app = Flask(__name__)
app.secret_key = "super secret key"


def show_symbols_from_selected_watchlist():

    try:
        name = request.form['watchlist_name']
        print name
        session['picked_watchlist'] = name
    except HTTPException as e:
        pass
        
    con = lite.connect("watchlists.db")
    cur = con.cursor()
    email_watchlist = [i[0] for i in cur.execute("SELECT * FROM _emails_to_send").fetchall()]
    if session['picked_watchlist'] in email_watchlist:
        checked = "checked"
    else:
        checked = "none"
    symbol_list = sorted([i[0] for i in cur.execute("SELECT Name FROM %s  "%session['picked_watchlist'])])
    
    return render_template('symbols_from_watchlist.html',
        symbol_list = symbol_list,watchlist_name = session['picked_watchlist'],
        checked = checked)

    
@app.route("/watchlist_landing_page", methods = ["GET","POST"])
def landing():
    con = lite.connect("watchlists.db")
    cur = con.cursor()
    return render_template( "watchlist_landing_page.html",database = (
                            [watchlist[0] for watchlist in cur.execute(
                            "SELECT name FROM sqlite_master WHERE type='table'").fetchall() 
                            if not watchlist[0].startswith('_')]))

@app.route("/create_watchlist",methods = ["GET","POST"])
def create_watchlist():
	print 1
	session['picked_watchlist'] = request.form['watchlist_to_create']
	print 2
	con = lite.connect("watchlists.db")
	cur = con.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS %s (NAME TEXT, USER TEXT)"%session['picked_watchlist'])
	print 3
	con.commit()
	print 4
	return show_symbols_from_selected_watchlist()


							
@app.route("/selected_watchlist", methods  = ["GET","POST"])
def selected_watchlist():
    
    return show_symbols_from_selected_watchlist()

@app.route("/to_send_or_not", methods = ["GET","POST"])
def to_send_or_not():
    con = lite.connect('watchlists.db')
    cur = con.cursor()
    email_watchlist = [i[0] for i in cur.execute("SELECT * FROM _emails_to_send").fetchall()]
    try:
        box = request.form['abc']
        if session['picked_watchlist'] not in email_watchlist:
            cur.execute("INSERT INTO _emails_to_send (WATCHLIST) VALUES (?)",(session['picked_watchlist'],)).fetchall()
            con.commit()
        return show_symbols_from_selected_watchlist()
    except HTTPException:
        cur.execute("DELETE FROM _emails_to_send WHERE WATCHLIST = '%s'"%session['picked_watchlist'])
        con.commit()
        return show_symbols_from_selected_watchlist()
    

@app.route("/delete_symbol", methods  = ["GET","POST"])
def delete_symbol():
    name = request.form['symbol']
    picked_watchlist = session['picked_watchlist']
    con = lite.connect("watchlists.db")
    cur = con.cursor()
    for individual_symbol in name.split(','):
        cur.execute("DELETE FROM %s WHERE NAME = '%s'"%(picked_watchlist,individual_symbol.upper())	)
    con.commit()
    return show_symbols_from_selected_watchlist()
    
@app.route("/add_symbol", methods  = ["GET","POST"])
def add_symbol():
    name = request.form['symbol']
    picked_watchlist = session['picked_watchlist']
    con = lite.connect("watchlists.db")
    cur = con.cursor()
    for individual_symbol in name.split(','):
        cur.execute("INSERT INTO %s (NAME, USER ) VALUES (?,?)"%picked_watchlist, (individual_symbol.upper(),'routman'))
    con.commit() 
    return show_symbols_from_selected_watchlist()

if __name__ == "__main__":
    app.run(debug = True)
