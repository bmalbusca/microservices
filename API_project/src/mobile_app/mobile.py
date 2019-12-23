from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
from json2html import *
import requests
import secrets

#to get the following value go to:
# FENIX -> Pessoal - Gerir Aplicações -> criar
#https://fenixedu.org/dev/tutorials/use-fenixedu-api-in-your-application/ (Step1)

redirect_uri = "http://127.0.0.1:5000/userAuth" # this is the address of the page on this app
client_id= "570015174623394"
#"12234455666935" # copy value from the app registration
clientSecret = "BNSpLi3noPqnh6/AX2pBKXSOG2uVy+XZ+9MqcE3aq0QHWa5VOS350ofnhkcsMgqXeSRLX0iDSa5R6CzAfcu8NQ=="


fenixLoginpage= "https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=%s&redirect_uri=%s"
fenixacesstokenpage = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

loginName = False  
userToken = None
code = False
app = Flask(__name__)

# sizeSecret = nbytes of secret 
sizeSecret  = 10 #string will have 8 digits
# return a random string with nbytes rahttps://fandom.randintenix.tecnico.ulisboa.pt/oauthndom bytes with each byte converted to 2 hex digits
userSecret = secrets.token_hex(int(sizeSecret/2))
askedSecret = False

@app.route('/')
def hello_world_auth():
    if loginName == False:
        #if the user is not authenticated
        redPage = fenixLoginpage % (client_id, redirect_uri)
        # the app redirecte the user to the FENIX login page
        return redirect(redPage)
    else:
        return render_template("mobileIn.html", username=loginName)

##################################################
@app.route('/askSecret', methods = ['GET','POST'])
def askSecret_auth():
    #this page can only be accessed by a authenticated username
    if loginName == False:
        #if the user is not authenticated
        redPage = fenixLoginpage % (client_id, redirect_uri)
        # the app redirecte the user to the FENIX login page
        return redirect(redPage)
    else:
        #if the user ir authenticated
        #print(userToken)
        #we can use the userToken to access the fenix
        params = {'access_token': userToken}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)

        if (resp.status_code == 200):
            r_info = resp.json()
            # if sucessfully loggedin then check if it's POST and if not just return regular page 
            if (request.method == 'POST'):
                info = {
                "name": r_info["name"],
                "istID": r_info["username"],
                "photo": r_info["photo"],
                "secret": userSecret
                }
                print(info["istID"])
                return info#json2html.convert(json = r_info["photo"])
        return redirect('static/askSecret.html')

##################################################
@app.route('/validateSecret', methods = ['GET','POST'])
def validateSecret_auth():
    #this page can only be accessed by a authenticated username
    if loginName == False:
        #if the user is not authenticated
        redPage = fenixLoginpage % (client_id, redirect_uri)
        # the app redirecte the user to the FENIX login page
        return redirect(redPage)
    else:
        #if the user ir authenticated
        #print(userToken)
        #we can use the userToken to access the fenix
        params = {'access_token': userToken}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)

        if (resp.status_code == 200):
            r_info = resp.json()
            # if sucessfully loggedin then check if it's POST and if not just return regular page 
            if(request.method == 'POST'):
                if (request.is_json):
                    secretIn = request.json["secret"] # secretIn is a string: print(type(secretIn))
                    if(len(secretIn)!= sizeSecret):
                        return json2html.convert(json = "invalid")
                    return json2html.convert(json = secretIn)
        return redirect('static/validateSecret.html')

################################################
@app.route('/readQR', methods = ['GET','POST'] )
def readQR_auth():
    #this page can only be accessed by a authenticated username
    if loginName == False:
        #if the user is not authenticated
        redPage = fenixLoginpage % (client_id, redirect_uri)
        # the app redirecte the user to the FENIX login page
        return redirect(redPage)
    else:
        #if the user ir authenticated
        print(userToken)

        #we can use the userToken to access the fenix
        params = {'access_token': userToken}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)


        if (resp.status_code == 200):
            r_info = resp.json()
            print( r_info)
            # if sucessfully loggedin then check if it's POST and if not just return regular page 
            if (request.method == 'POST'):
                if (request.is_json):
                    jsdata = request.json#['QRinfo']
                    print(jsdata)
                    return jsonify(jsdata) #vai me devolver para a consola em formato json
                return jsonify(4) #vai me devolver para a consola em formato json   
            else:
                return render_template("testwebcam.html")
                #return render_template("privPage.html", username=loginName, name=r_info['name'])        	
        else:
            return "can't access QRpage"

# FICA a faltar colocar esta autorizaçao nas paginas dos segredos

@app.route('/userAuth')
def userAuthenticated():
    #This page is accessed when the user is authenticated by the fenix login pagesetup

    #first we get the secret code retuner by the FENIX login
    code = request.args['code']
    print ("code "+request.args['code'])


    # we now retrieve a fenix access token
    payload = {'client_id': client_id, 'client_secret': clientSecret, 'redirect_uri' : redirect_uri, 'code' : code, 'grant_type': 'authorization_code'}
    response = requests.post(fenixacesstokenpage, params = payload)
    print (response.url)
    print (response.status_code)
    if(response.status_code == 200):
        #if we receive the token
        print ('getting user info')
        r_token = response.json()
        print(r_token)

        params = {'access_token': r_token['access_token']}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
        r_info = resp.json()
        print( r_info)

        # we store it
        global loginName
        loginName = r_info['username']
        global userToken
        userToken = r_token['access_token']

        #now the user has done the login
        return jsonify(r_info)
        #we show the returned infomration
        #but we could redirect the user to the private page
        return redirect('/private') #comment the return jsonify....
    else:
        return 'oops'

if __name__ == '__main__':
    app.run()
