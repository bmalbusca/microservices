from flask import Flask , redirect, url_for, request, render_template, jsonify, abort 
import requests as req
import json
from datetime import *





API_rooms = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces"
    
app = Flask(__name__)

class Rooms(object):
    def __init__(self, url):
        self.url = url 
    
    def json_to_py(self, json_file):
        return json.loads(json_file)

    def request_url(self, id):
        today = date.today()
        uri = self.url+ "/" + str(id)+ "/" + today.strftime("%d/%m/%Y")
        return self.json_to_py(req.get(self.url+ "/" + str(id)+ "?day=" + today.strftime("%d/%m/%Y")).text)

    def json_dump(self, data ):
        return json.dumps(data)

        

room = Rooms(API_rooms)


@app.errorhandler(404)
def page_not_found(e):
    return  "Sorry, source not available.", 404


@app.route('/', methods = ['GET','POST'] )
def link():
    return "Rooms API v1.1"


@app.route('/<path:subpath>')
def find(subpath):    
    resp = room.request_url(subpath)
    print(resp, type(resp))
    
    if 'error' in resp:
        abort(404)
    else:
        return room.json_dump(resp)

if __name__ == '__main__':
    app.run(debug = True)
    pass



