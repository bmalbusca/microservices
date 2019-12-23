from flask import Flask , redirect, url_for, request, render_template, make_response, jsonify
import requests as req
import json
from json2html import *
from datetime import  *

app = Flask(__name__)

#host = "127.0.0.1"
host = "localhost"
http = "http://"
port = "5000"

class logs(object):
    @staticmethod
    def message(service_url, time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
        return {"service": service_url, "datetime": time}

temporary_log = [] 



web_pages = {
        "room":http +  host + ":" + port + "/room" ,
        "canteen":http +  host + ":" + port  + "/menu" ,
        "secretariat":http +  host + ":" + port + "/secretariat"
        }

proxy = {
        "room": "http://0.0.0.0:5001/room/" ,
        "canteen": "http://0.0.0.0:5003/menu/" ,
        "secretariat": "http://0.0.0.0:5002/secretariat/"
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

@app.route('/menu/search', methods= ['POST'])
def search():
    
    if  request.method == 'POST':
        day = request.form['day']
        m = request.form['m']
        y = request.form['y']
        add = proxy["canteen"] + day + "/" + m + "/" + y
        data= req.get(add).text
        temporary_log.append(logs.message(add))
        return json2html.convert(json = data)
    
    else:

        return redirect(url_for('menu'))



@app.route('/menu/', methods= ['GET', 'POST'])
def menu():
    temporary_log.append(logs.message('/menu/'))
    return render_template("menu.html", ref = web_pages["canteen"]+"/search" )
     


if __name__ == '__main__':
    app.run( debug = True)
    pass
