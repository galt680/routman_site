from flask import Flask,request,render_template
	
	
	
	
def vix_spikes_page():
	thresh = request.form['threshold']
	days = request.form['days']
	return render_template('imp_spikes.html',days = days,thresh = thresh)
	# print thresh
	# return thresh
	