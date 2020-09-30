from flask import Flask
from flask import request
from flask import render_template
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__) # create an instance of the Flask class for the web app
auth = HTTPBasicAuth()

# callback function that the extension will use to obtain the password for a given user
@auth.verify_password
def authenticate(user, password):
	if user and password:
		if user == "admin" and password =="admin":
			return True
		# else:
			return False
	return False

# callback will be used by the extension when it needs to send the unauthorized error code back to the client
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


#To be able to invoke this function we have to send our credentials:
#$ curl -u admin:admin -i http://127.0.0.1:5000/ 
@app.route('/')
@auth.login_required
def home():
	return render_template("adminPage.html")

# Using Postman
# https://techtutorialsx.com/2018/01/02/flask-basic-authentication/
# https://www.roytuts.com/python-flask-http-basic-authentication/
# OAuth: https://serverfault.com/questions/371907/can-you-pass-user-pass-for-http-basic-authentication-in-url-parameters

# Python assigns the name "__main__" to the script when the script is executed.
# 	If the script is imported from another script, the script keeps it given name
# By checking if name is main we  
if __name__ == '__main__':
	app.run()
