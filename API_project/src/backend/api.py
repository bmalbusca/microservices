from flask import Flask , redirect, url_for, request, render_template, make_response, jsonify
import requests as req
import json
from json2html import *
from datetime import  *

app = Flask(__name__)

host = "0.0.0.0"
public_ip = req.get('https://api.ipify.org').text
http = "http://"
port = "5000"

class logs(object):
    @staticmethod
    def message(service_url, time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
        return {"service": service_url, "datetime": time}

temporary_log = [] 


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
        "secretariat": "http://"+str(public_ip)+":5002/secretariat/"
        }

      

@app.errorhandler(404)
def page_not_found(e):
    return  "Sorry, source not available.", 404



###############
#   API
###############
@app.route('/api/room/<path:subpath>', methods= ['GET', 'POST'])
def api_room(subpath):
    temporary_log.append(logs.message('/api/room/'+(str(subpath))))
    return req.get(proxy["room"]+str(subpath)).text
   
@app.route('/api/secretariat/<path:subpath>', methods= ['GET', 'POST'])
def api_secretariat(subpath):
    temporary_log.append(logs.message('/api/secretariat/'+(str(subpath))))
    return req.get(proxy["secretariat"]+str(subpath)).text
   
@app.route('/api/menu/<path:subpath>', methods= ['GET', 'POST'])
def api_menu(subpath):
    temporary_log.append(logs.message('/api/menu/'+(str(subpath))))
    return req.get(proxy["canteen"]+str(subpath)).text 

################
#   QR code
################
@app.route('/api/token/<path:subpath>', methods= ['GET', 'POST'])
def api_hashtable(subpath):
    temporary_log.append(logs.message('/api/token/'+(str(subpath))))
    if str(subpath) in hash_services:
        return make_response(jsonify({"token": hash_services[subpath]}), 201)
    else:
        abort(404)



#############
# WEB
#############

@app.route('/', methods= ['GET', 'POST'])
def index(proxies={}):
    global web_pages
       
    proxies = web_pages 
    temporary_log.append(logs.message('/index/'))
    print("LOG:", len(temporary_log), temporary_log)
    return render_template("index.html", proxies=proxies)

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
        data= req.get(add).text
        print(add)
        req.post(add, json={"location": local, "name": name , "description": desc , "time":h } )
        temporary_log.append(logs.message(add))
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
        temporary_log.append(logs.message(add))
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
        temporary_log.append(logs.message(add))
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
        temporary_log.append(logs.message(add))
        return json2html.convert(json = data)
    
    else:

        return redirect(url_for('menu'))



@app.route('/menu/', methods= ['GET', 'POST'])
def menu():
    temporary_log.append(logs.message('/menu/'))
    print(web_pages["canteen"])
    return render_template("menu.html", ref = web_pages["canteen"]+"/search" )
     

@app.route('/room/', methods = ['GET','POST'])
def room():
    temporary_log.append(logs.message('/room/'))
    return render_template("room.html", ref=web_pages["room"]+"/search")




@app.route('/secretariat/', methods = ['GET','POST'])
def set():
    temporary_log.append(logs.message('/secretariat/'))
    return render_template("set.html", ref=web_pages["secretariat"]+"/search")

@app.route('/admin/', methods = ['GET','POST'])
def admin_page():
    data = temporary_log
    print(len(data), data)
    return render_template("adminPage.html", log=data)



if __name__ == '__main__':
    app.run(host = host, debug = True)
    pass
