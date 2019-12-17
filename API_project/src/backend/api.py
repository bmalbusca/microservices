from flask import Flask , redirect, url_for, request, render_template, make_response, jsonify
import requests as req
import json
from json2html import *

app = Flask(__name__)


proxy = {
        "room": "http://0.0.0.0:5001/room/" ,
        "canteen": "http://0.0.0.0:5003/menu/" ,
        "secretariat": "http://0.0.0.0:5002/secretariat/"
        }



@app.errorhandler(404)
def page_not_found(e):
    return  "Sorry, source not available.", 404


#  This route paths should used to behave like a middleware for API endpoints
#  The json2html will be implemented but using the redirect html and templates
#





@app.route('/api/room/<path:subpath>', methods= ['GET', 'POST'])
def room(subpath):
    return req.get(proxy["room"]+str(subpath)).text
    #return json2html.convert(json = data)
    #return json.dumps(data)

@app.route('/api/secretariat/<path:subpath>', methods= ['GET', 'POST'])
def secretariat(subpath):
    return req.get(proxy["secretariat"]+str(subpath)).text
    #return json2html.convert(json = data)
    #return json.dumps(data)

@app.route('/api/menu/<path:subpath>', methods= ['GET', 'POST'])
def menu(subpath):

    data= req.get(proxy["canteen"]+str(subpath)).text 
    return json2html.convert(json = data)
    #return json.dumps(data)

@app.route('/', methods= ['GET', 'POST'])
def api():
    return "Fenix API V1.0"

if __name__ == '__main__':
    app.run(debug = True)
    pass
