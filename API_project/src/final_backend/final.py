#### api.py
from flask import Flask , redirect, url_for, request, render_template, make_response, jsonify
import requests as req
import json
from json2html import *
from datetime import  *
#### admin.py
from flask import session
import os
#### mobile.py
import secrets

app = Flask(__name__)

##########################
host = "0.0.0.0"
public_ip = req.get('https://api.ipify.org').text
http = "http://"
port = "5000"
##########################

class logs(object):
    @staticmethod
    def message(service_url, time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
        return {"service": service_url, "datetime": time}

temporary_log = []


def push_log(info):
    try:
        req.put(proxy["log"]+"insert/", headers = {'Content-type': 'application/json'}, json=info)
    except:
        pass

def pop_log():
     data= json.loads(req.get(proxy["log"]+"request/").text)
     return data["log"]






web_pages = {
        "room":http +  str(public_ip) + ":" + port + "/room" ,
        "canteen":http +  str(public_ip) + ":" + port  + "/menu" ,
        "secretariat":http + str(public_ip) + ":" + port + "/secretariat"
        }


hash_services = {
                '6OAQ29s1fMrKQTVxMg6P' : web_pages["room"],
                'YB8rmIMi1qQ33vJlJ5Ik' : web_pages["canteen"],
                'tlDElAgZYbMlppAHwWki' : web_pages["secretariat"],
        }

proxy = {
        "room": "http://"+str(public_ip)+":5001/room/" ,
        "canteen": "http://"+str(public_ip)+":5003/menu/" ,
        "secretariat": "http://"+str(public_ip)+":5002/secretariat/",
        "log": "http://"+str(public_ip)+":5011/"
        }

      

@app.errorhandler(404)
def page_not_found(e):
    return  "Sorry, source not available.", 404


######################################
redirect_uri = "http://127.0.0.1:5000/userAuth" # this is the address of the page on this app
client_id= "570015174623394"
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
######################################



##############################
#   API
##############################
@app.route('/api/room/<path:subpath>', methods= ['GET', 'POST'])
def api_room(subpath):
    push_log(logs.message('/api/room/'+(str(subpath))))
    return req.get(proxy["room"]+str(subpath)).text
   
@app.route('/api/secretariat/<path:subpath>', methods= ['GET', 'POST'])
def api_secretariat(subpath):
    push_log(logs.message('/api/secretariat/'+(str(subpath))))
    return req.get(proxy["secretariat"]+str(subpath)).text
   
@app.route('/api/menu/<path:subpath>', methods= ['GET', 'POST'])
def api_menu(subpath):
    push_log(logs.message('/api/menu/'+(str(subpath))))
    return req.get(proxy["canteen"]+str(subpath)).text 

##############################
#   QR code
##############################
@app.route('/api/token/<path:subpath>', methods= ['GET', 'POST'])
def api_hashtable(subpath):
    push_log(logs.message('/api/token/'+(str(subpath))))
    if str(subpath) in hash_services:
        return make_response(jsonify({"token": hash_services[subpath]}), 201)
    else:
        abort(404)

##############################
# Admin - GET/POST
##############################
@app.route('/', methods= ['GET', 'POST'])
def index():#proxies={}):
	if session.get('inAdmin'): #if user is logged in as Admin then send them to the web page to create/change Secretariat and see logs
    		
		data = pop_log()
		return render_template("adminPage.html", log = data)
	else:
		push_log(logs.message('/loginAdmin/'))
		return render_template("loginadmin.html") # webpage with loginform, after submit send to route bellow

    #global web_pages   
    #proxies = web_pages 
    #return render_template("index.html", proxies=proxies)


@app.route('/loginAdmin', methods = ["POST"])
def loginAdmin():
#	if request.method == "POST":
	if request.form['user'] == 'admin' and request.form['pass'] == 'admin':
		session['inAdmin'] = True
	else:
		session['inAdmin'] = False
	return index()


@app.route('/logoutAdmin', methods = ["POST"])
def logoutAdmin():
	session['inAdmin'] = False
	return index()



@app.route('/show', methods= ['GET', 'POST'])
def show(proxies={}):
    global web_pages
       
    proxies = web_pages 
    push_log(logs.message('/show/'))
    return render_template("index.html", proxies=proxies)



##############################
# WEB - GET/POST
##############################
@app.route('/menu/', methods= ['GET', 'POST'])
def menu():
    push_log(logs.message('/menu/'))
    print(web_pages["canteen"])
    return render_template("menu.html", ref = web_pages["canteen"]+"/search" )
     

@app.route('/room/', methods = ['GET','POST'])
def room():
    push_log(logs.message('/room/'))
    return render_template("room.html", ref=web_pages["room"]+"/search")


@app.route('/secretariat/', methods = ['GET','POST'])
def set():
    push_log(logs.message('/secretariat/'))
    return render_template("set.html", ref=web_pages["secretariat"]+"/search")

##############################
# WEB - POST
##############################
@app.route('/addSecretariat', methods= ['POST'])
def insert_set(): 
    print("proxy", proxy["canteen"])
    print("menu - POST ")
    
    if request.method == 'POST':
       
        name = request.form['Name']
        local = request.form['Location']
        desc = request.form['Description']
        h = request.form['OpeningHours']

        add = "http://"+str(public_ip)+":5002/insert/" +str(name)+"/"+str(local)
       
       
        data = req.put(add, headers = {'Content-type': 'application/json'}, json={"location": str(local), "name": str(name) , "description": str(desc) , "time":h } ).text
        push_log(logs.message(add))
        return json2html.convert(json = data)
    
    else:

        return redirect(url_for('menu'))

@app.route('/changeSecretariat', methods= ['POST'])
def change_set():
    if request.method == 'POST':

        name = request.form['name']
        local = request.form['local']
        desc = request.form['des']
        h = request.form['hours']

        add = "http://"+str(public_ip)+":5002/insert/" +str(name)+"/"+str(local)


        data = req.put(add, headers = {'Content-type': 'application/json'}, json={"location": str(local), "name": str(name) , "description": str(desc) , "time":h } ).text
        push_log(logs.message(add))
        return json2html.convert(json = data)
    else:
        return redirect(url_for('menu'))





@app.route('/menu/search', methods= ['POST'])
def menu_search():
    print("proxy", proxy["canteen"])
    print("menu - POST ")
    if  request.method == 'POST':
        day = request.form['day']
        m = request.form['m']
        y = request.form['y']
        add = proxy["canteen"] + day + "/" + m + "/" + y
        data= req.get(add).text
        print(add)
        push_log(logs.message(add))
        return json2html.convert(json = data)
    
    else:

        return redirect(url_for('menu'))


@app.route('/room/search', methods= ['POST'])
def room_search():
    
    if  request.method == 'POST':
        num = request.form['id']
        add = proxy["room"] + str(num)
        print(add)
        data= req.get(add).text
        push_log(logs.message(add))
        return json2html.convert(json = data)
    
    else:

        return redirect(url_for('menu'))


@app.route('/secretariat/search', methods= ['POST'])
def set_search():
    print("entrou") 
    if  request.method == 'POST':
        name = request.form['name']
        local = request.form['local']
        add = proxy["secretariat"] + str(name) + "/" + str(local) 
        data= req.get(add).text
        print(add)
        push_log(logs.message(add))
        return json2html.convert(json = data)
    
    else:

        return redirect(url_for('menu'))

##############################
# MOBILE APP
##############################
@app.route('/mobile')
def mobile_auth():
    if loginName == False:
        #if the user is not authenticated
        redPage = fenixLoginpage % (client_id, redirect_uri)
        # the app redirecte the user to the FENIX login page
        push_log(logs.message('/mobile'))
        return redirect(redPage)
    else:
        return render_template("mobileIn.html", username=loginName)

################################################
@app.route('/readQR', methods = ['GET','POST'] )
def readQR_auth():
    push_log(logs.message('/readQR'))
    #this page can only be accessed by a authenticated username
    if loginName == False:
        #if the user is not authenticated
        redPage = fenixLoginpage % (client_id, redirect_uri)
        # the app redirecte the user to the FENIX login page
        return redirect(redPage)
    else:
        #if the user ir authenticated
        #we can use the userToken to access the fenix
        params = {'access_token': userToken}
        resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)

        if (resp.status_code == 200):
            r_info = resp.json()
            # if sucessfully loggedin then check if it's POST and if not just return regular page 
            if (request.method == 'POST'):
                if (request.is_json):
                    QRdata = request.json#['QRinfo']
                    url = QRdata.split(http +  host + ":" + port,1)[1]


                    return jsonify(QRdata) #vai me devolver para a consola em formato json
                return jsonify(4) #vai me devolver para a consola em formato json   
            else:
                return redirect("static/testwebcam.html")
                #return render_template("privPage.html", username=loginName, name=r_info['name'])           
        else:
            return "can't access QRpage"

##################################################
@app.route('/askSecret', methods = ['GET','POST'])
def askSecret_auth():
    push_log(logs.message('/askSecret'))

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
        resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
            
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
                return info#json2html.convert(json = r_info["photo"])
        return redirect('static/askSecret.html')

##################################################
@app.route('/validateSecret', methods = ['GET','POST'])
def validateSecret_auth():
    push_log(logs.message('/validateSecret'))

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
        resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)

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
@app.route('/userAuth')
def userAuthenticated():
    #This page is accessed when the user is authenticated by the fenix login pagesetup

    #first we get the secret code retuner by the FENIX login
    code = request.args['code']
    #print ("code "+request.args['code'])

    push_log(logs.message('/userAuth'))

    # we now retrieve a fenix access token
    payload = {'client_id': client_id, 'client_secret': clientSecret, 'redirect_uri' : redirect_uri, 'code' : code, 'grant_type': 'authorization_code'}
    response = req.post(fenixacesstokenpage, params = payload)
    #print (response.url)
    #print (response.status_code)
    if(response.status_code == 200):
        #if we receive the token
        #print ('getting user info')
        r_token = response.json()
        #print(r_token)

        params = {'access_token': r_token['access_token']}
        resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
        r_info = resp.json()
        #print( r_info)

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





##############################
# MAIN
##############################	
if __name__ == '__main__':
	app.secret_key = os.urandom(12) 
	app.run(host = host, debug = True)
	pass
