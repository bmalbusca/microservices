from flask import Flask
from flask import session
from flask import request
from flask import render_template
from flask import redirect
from flask import jsonify

import os

app = Flask(__name__) # create an instance of the Flask class for the web app

@app.route('/') 
def home():
	if session.get('inAdmin'): #if user is logged in as Admin then send them to the web page to create/change Secretariat and see logs
		return render_template("adminPage.html")
	else:
		return render_template("loginadmin.html") # webpage with loginform, after submit send to route bellow

@app.route('/loginAdmin', methods = ["POST"])
def loginAdmin():
#	if request.method == "POST":
	if request.form['user'] == 'admin' and request.form['pass'] == 'admin':
		session['inAdmin'] = True
	else:
		session['inAdmin'] = False
	return home()

@app.route('/logoutAdmin', methods = ["POST"])
def logoutAdmin():
	session['inAdmin'] = False
	return home()

##### add secretariat

##### list logs

#####

 
# Python assigns the name "__main__" to the script when the script is executed.
if __name__ == '__main__':
	app.secret_key = os.urandom(12) #generate a random key to keep the session safe
	app.run()
