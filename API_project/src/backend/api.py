from flask import Flask , redirect, url_for, request, render_template, make_response, jsonify
import requests as req
import json
from json2html import *

app = Flask(__name__)

#host = "127.0.0.1"
host = "localhost"
http = "http://"
port = "5000"

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
    return req.get(proxy["room"]+str(subpath)).text
   
@app.route('/api/secretariat/<path:subpath>', methods= ['GET', 'POST'])
def api_secretariat(subpath):
    return req.get(proxy["secretariat"]+str(subpath)).text
   
@app.route('/api/menu/<path:subpath>', methods= ['GET', 'POST'])
def api_menu(subpath):
    return req.get(proxy["canteen"]+str(subpath)).text 

#############
# WEB
#############

@app.route('/', methods= ['GET', 'POST'])
def index(proxies={}):
    global web_pages
    proxies = web_pages 
    return render_template("index.html", proxies=proxies)


@app.route('/menu/search', methods= ['POST'])
def search():
    
    if  request.method == 'POST':
        day = request.form['day']
        m = request.form['m']
        y = request.form['y']
        
        #print("data",day,m,y)
        add = proxy["canteen"] + day + "/" + m + "/" + y
        data= req.get(add).text
        
        return json2html.convert(json = data)
    
    else:

        return redirect(url_for('menu'))



@app.route('/menu/', methods= ['GET', 'POST'])
def menu():
    return render_template("menu.html", ref = web_pages["canteen"]+"/search" )
     


if __name__ == '__main__':
    app.run( debug = True)
    pass
