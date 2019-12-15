from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
import requests

#to get the following value go to:
# FENIX -> Pessoal - Gerir Aplicações -> criar
#https://fenixedu.org/dev/tutorials/use-fenixedu-api-in-your-application/ (Step1)

redirect_uri = "http://127.0.0.1:5000/userAuth" # this is the address of the page on this app

client_id= "12234455666935" # copy value from the app registration
clientSecret = "6wrRVKcgjhjiHHKkjkGFD5LaoZioWPfg1SzNhwPoi*&&JhhhhoeXwSrdfqn7P3ed9ue+teTw==" # copy value from the app registration

fenixLoginpage= "https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=%s&redirect_uri=%s"
fenixacesstokenpage = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

loginName = False
userToken = None
code = False
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("appPage.html", username=loginName)

@app.route('/private')
def private_page():
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
            return render_template("privPage.html", username=loginName, name=r_info['name'])
        else:
            return "oops"

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
