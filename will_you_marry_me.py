from flask import Flask,request,render_template,url_for
def yes():
	if request.form['decision'] == 'yes':
		return render_template('yes.html')
	else:
		return render_template('no.html')