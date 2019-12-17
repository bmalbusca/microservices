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
		return render_template("mainPage.html") # webpage with loginform, after submit send to route bellow

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

# @app.route('/api/userSearch', methods = ["GET"])
# def searchService(uri):
# 	if uri.split('/',-1)[0]: #user introduces microservice/
# 		micro = uri.split('/',-1)[0] 
# 	else: #user introduces /microservice/
# 		micro = uri.split('/',-1)[1] 

# @app.route('/api/<path:subpath>')
# def show_subpath(subpath):
#     # show the subpath after /path/
#     return 'Subpath %s' % subpath

# #@app.route('/api/<path:rooms/<int:room_id>>', methods=["GET"])
# @app.route('/api/<path:rooms/<int:room_id>>', methods=["GET"])
# def get_room(room_id):
# 	return 'jsonify(<usar funcao do microservico para get info according to id:%d' % room_id


@app.route('/api/<path:subpath>', methods=['POST', 'GET'])
def dealing(subpath):
	#if request.method == "GET":
	uris = subpath.split('/',-1) 
	return 'o subpath e: %s' % uris


@app.route('/readQR', methods = ['GET','POST'])
def getQRinfo():		
	if (request.method == 'POST'):
		if (request.is_json):
			jsdata = request.json
			#print(jsdata) #vai me imprimir no terminal a mensagem
			#read URL from QR Code 

			#redirect to route: transformar url que retorna html para um que de para a api

			#>>>>>>>> DESCODIFICAR A STRING <<<<<<<<<<<<<<


			#>>>>>>>> redirect para a API <<<<<<<<<<<<<<

			# get URL from a route by doing:
			# @app.route('/')
			# def index():
			# 	.
			# 	.
			# 	.
			# url_for('index') (can use it on flask or in html page)
			return jsonify("did it receive") 
		return jsonify(4) #vai me devolver para a consola em formato json
	return redirect("static/testwebcam.html", code = 302)


# Python assigns the name "__main__" to the script when the script is executed.
# 	If the script is imported from another script, the script keeps it given name
# By checking if name is main we  
if __name__ == '__main__':
	app.secret_key = os.urandom(12) #generate a random key to keep the session safe
	app.run()
