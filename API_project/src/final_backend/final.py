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
http = "https://"
port = "5000"
##########################
#http+host+":"+port

print("SERVER IP:", public_ip)

class logs(object):
    @staticmethod
    def message(service_url, time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
        return {"service": service_url, "datetime": time}

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


###################################### MOBILE APP
redirect_uri = http+host+":"+port+"/mobile/userAuth" # this is the address of the page on this app
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

# will later be populated with the following info per user:
userlist = []
######################################



##############################
#   API
##############################
@app.route('/api/room/<path:subpath>', methods= ['GET', 'POST'])
def api_room(subpath):
    print("here")
    push_log(logs.message('/api/room/'+(str(subpath))))
    return req.get(proxy["room"]+str(subpath)).text
   
@app.route('/api/secretariat/<path:subpath>', methods= ['GET', 'POST'])
def api_secretariat(subpath):
    push_log(logs.message('/api/secretariat/'+(str(subpath))))
    print(proxy["secretariat"]+str(subpath))
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


@app.route('/newService/', methods = ['POST'])
def new_service():
    push_log(logs.message('/newService/'))
    
    if request.method == 'POST':
       
        name = request.form['name']
        url = request.form['url']
        proxy[name]= url 
        web_pages[name] =  http + str(public_ip) + ":" + port + "/usrService/" + str(name)

    else:
        return redirect(url_for('menu'))

@app.route('/usrService/<path:subpath>', methods = ['GET'])
def show_usr_service(subpath):
    push_log(logs.message('/usrService/'+str(subpath)))
    fields = subpath.split("/")
    data= req.get(proxy[fields[0]]).text
    return json2html.convert(json = data)





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
        params = {'access_token': userToken}
        resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
        if (resp.status_code == 200):
            r_info = resp.json()
            #check if user list exists
            if "user_info" in userlist:
                #if so, check if user is there
                currUser = next((item for item in userlist if item['user_info'] == r_info), None)
                #if not there then add the user
                if currUser is None:
                    aux = {
                    "user_info": r_info
                    }
                    userlist.append(aux) 
            #no user list exists
            else:
                aux = {
                    "user_info": r_info
                    }
                userlist.append(aux)    
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
                    QRdata = request.json
                    #localip /qr/ micro/data

                    #print(QRdata)
                    #print("https://" +  public_ip + ":"+ port)
                    url = QRdata.split("https://" +  public_ip + ":" + port,1)[1]
                    #print(url)
                    #print("dividi o url em")
                    #print(url.split("/",3))
                    #print(url) #/microserice/data
                    #url = url[2:]
                    #print("url plit plos /")
                    #print(url.split("/",1))
                    microservice = url.split("/",3)[2]
                    #print("micros")
                    #print(microservice)
                    data = url.split("/",3)[3]
                    #print("subpath data")
                    #print(data)
                    #tp = url.split("/",3)[3]
                    #print("aqui vai a tentativa:") 
                    #print("microservice: "+microservice)
                    print("vou pedir o url para")
                    print(url_for("api_"+microservice,subpath = data))
                    return redirect(url_for("api_"+ microservice, subpath = data))
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
                currUser = next((item for item in userlist if item['user_info'] == r_info), None)
                currUser['secret'] = userSecret
                info = {
                    "name": r_info["name"],
                    "istID": r_info["username"],
                    "photo": r_info["photo"],
                    "secret": userSecret
                }
                return info
        return redirect('static/askSecret.html')

@app.route('/valBy', methods = ['GET','POST'])
def valBy_auth():
    push_log(logs.message('/valBy'))
    if loginName == False:
        #if the user is not authenticated
        redPage = fenixLoginpage % (client_id, redirect_uri)
        # the app redirecte the user to the FENIX login page
        return redirect(redPage)
    else:
        params = {'access_token': userToken}
        resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
        
        if (resp.status_code == 200):
            r_info = resp.json()
            if (request.method == 'GET'):
                currUser = next((item for item in userlist if item['user_info'] == r_info), None)
                # if the user has been validated by someone  
                if "lastvalBy" in currUser:
                    # get info of the user that asked for the validation
                    lastvalBy = currUser['lastvalBy']
                    info = {
                        "name": lastvalBy["name"],
                        "istID": lastvalBy["istID"],
                        "photo": lastvalBy["photo"]
                    }
                # no user has asked for validation of the currUser
                else:
                    info = {
                        "name": "none"}
                return info
        return redirect('static/askSecret.html')

##################################################
@app.route('/validateSecret', methods = ['GET','POST'])
def validateSecret_auth():
    push_log(logs.message('/validateSecret'))

    #this page can only be accessed by a authenticated username
    if loginName == False:
        #if the user is not authenticated
        # redPage = fenixLoginpage % (client_id, redirect_uri)
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
                        aux = {"secret": "invalid"}
                        return aux
                    #check if secret is in userlist
                    #if it is then return data
                    my_item = next((item for item in userlist if item['secret'] == secretIn), None)
                    if my_item is None:
                        aux = {"secret": "invalid"}
                        return aux
                    else:
                        #check if user asking for validation already generated their own secret
                        lastvalByuser = next((item for item in userlist if item['user_info'] == r_info), None)
                        if lastvalByuser is None:
                            #if the user hasn't asked for their own secret:
                            my_item['lastvalBy'] = {
                                "name": r_info["name"],
                                "istID": r_info["username"],
                                "photo": r_info["photo"]
                                #"secret": lastvalBysecret  
                            }
                        else:
                            #if the user already has a secret:
                            my_item['lastvalBy'] = {
                                "name": r_info["name"],
                                "istID": r_info["username"],
                                "photo": r_info["photo"],
                                # add to the data of the user whose secret was input, the data of the user that asked for validation
                                "secret": lastvalByuser["secret"]  
                            }
                        #info to be displayed of requested user given a valid secret:
                        info = {
                            "name": my_item['user_info']["name"],
                            "istID": my_item['user_info']["username"],
                            "photo": my_item['user_info']["photo"],
                            "secret": userSecret
                        }
                        return info
        return redirect('static/validateSecret.html')


################################################
@app.route('/mobile/userAuth')
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
        return redirect('/mobile') #comment the return jsonify....
    else:
        return 'oops'





##############################
# MAIN
##############################	
if __name__ == '__main__':
	app.secret_key = os.urandom(12) 
	app.run(host = host, ssl_context='adhoc')
	pass
