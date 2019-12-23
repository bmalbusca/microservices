from flask import Flask ,make_response,  redirect, url_for, request, render_template, jsonify, abort 
import requests as req
import json
from datetime import *


datab = { "log" : [ ]}


class Database(object):

    def __init__(self,data={"log" :[]} ):
        self.database = data

    def insert(self, data):
        try:
            self.database["log"].append(data)
            return 201

        except:
            print("Database not defined")
            return 400 
    

    def reset(self):
        del self.database["log"]
        self.database["log"] = []

    def printDB(self):
        print(self.database)

    def dump(self):
        return json.dumps(self.database)

    
app = Flask(__name__)
db = Database(datab)

@app.errorhandler(404)
def page_not_found(e):
    return  "Sorry, source not available.", 404


@app.route('/', methods = ['GET','POST'] )
def link():
    return "LOG API v1.1"

#######################################################################################

@app.route('/insert/', methods = ['GET','POST','PUT'])
def insert():
        
    
    # name/local  - primary keys 
    res = request.get_json()
    print(res)
  
    status = db.insert(res)
    
    if status == 200:
        res = make_response(jsonify({"message": "Collection replaced"}), 200)
        return res
    elif  status == 201:
        res = make_response(jsonify({"message": "Collection created"}), 201)
        return res
    else:
        abort(404)


@app.route('/request/', methods = ['GET','POST'])
def find():
    return  make_response(jsonify(db.database), 200) 
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = '5011',debug = True)
    pass





