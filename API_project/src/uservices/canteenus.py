from flask import Flask , redirect, url_for, request, render_template, jsonify, abort 
import requests as req
import json
from datetime import *
from menu import Menu 

"""
See client request : print("request >> ","{}/{}".format(request.script_root, request.path))
API endpoint : API_canteen

Things to be done: 
    1. Order the dict keys by datetime 
    2. Check if is need to search entire dict 
    3. Manage the dict size 
"""
#@app.route('/api', methods = ['GET', 'POST'] )
#def api(): 
#    resp = req.get(API_canteen)
#    return jsonify(resp.json())

API_canteen = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"
    
app = Flask(__name__)

menu= Menu(API_canteen)
menu.add_menu()


@app.errorhandler(404)
def page_not_found(e):
    return  "Sorry, source not available.", 404


@app.route('/', methods = ['GET','POST'] )
def link():
    return "canteen API v1.1"


@app.route('/menu/<path:subpath>')
def find(subpath):
    print("Received", subpath)
    resp = menu.find(str(subpath))
  
    if  resp == 404:
        return abort(resp)
    else:
        return resp 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = '5003', debug = True)
    pass
