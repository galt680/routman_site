from flask import Flask,request,render_template,url_for
from get_covered_call_data import get_data_to_deliver






app = Flask(__name__)

    
    
@app.route('/',methods = ['GET','POST'])
def symbol_input_readings():
    return render_template('covered_call_input.html')

@app.route('/get_data',methods = ['GET','POST'])
def get_call_data():
    
    symbol = request.form['symbol']
    data = get_data_to_deliver([symbol])
    # data = ({'aapl': {u'May': {10: [155.0, 0.52], 5: [150.0, 1.14]}, u'Jun': {10: [155.0, 0.91], 5: [150.0, 1.7]}, u'Aug': {10: [155.0, 2.19], 5: [150.0, 3.61]}, u'Jul': {10: [155.0, 1.42], 5: [150.0, 2.46]}}})
    return render_template('covered_call_table.html',data = data,symbol = symbol)
    
    
if __name__ == "__main__":
    app.run(debug = True)