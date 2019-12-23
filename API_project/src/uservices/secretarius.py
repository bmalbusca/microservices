from flask import Flask ,make_response,  redirect, url_for, request, render_template, jsonify, abort 
import requests as req
import json
from datetime import *


datab = { "secretariats" : [ {"location": "Alameda" , "name": "DA" , "description": "Direcao academica" , "time":"9:30 - 17:00" }  
            ]}


# add this to the  object class - for comparison 
secretariat = {"location": "Alameda" , "name": "DA" , "description": "Direcao academica" , "time":"9:30 - 17:00" }  


class Database(object):

    def __init__(self,data={"secretariats" :[]} ):
        self.database = data

    def insert(self, data):
        try:
            for setdata in self.database["secretariats"]:
                if setdata["name"] == data["name"] and  setdata["location"] == data["location"]:                
                    setdata = data 
                    return 200
            self.database["secretariats"].append(data)
            return 201

        except:
            print("Database not defined")
            return 400 
    
    def find(self, name, local):
        for data in self.database["secretariats"]:
            if name == data["name"] and local == data["location"] :
                return data
            else:
                return 404
            
    def remove(self, name ):
        for data in self.database["secretariats"]:
            if name == data["name"]:
                self.database["secretariats"].remove(data) 
                break


    def reset(self):
        del self.database["secretariats"]
        self.database["secretariats"] = []

    def printDB(self):
        print(self.database)

    def dump(self):
        return json.dumps(self.database)

    
app = Flask(__name__)
db = Database(datab)
#db.printDB()

#db.insert(secretariat)
#db.printDB()
#db.reset()
#db.printDB()






@app.errorhandler(404)
def page_not_found(e):
    return  "Sorry, source not available.", 404


@app.route('/', methods = ['GET','POST'] )
def link():
    return "Secretariats API v1.1"

###############################################################################################
#
#   requests.post("http://127.0.0.1:5000/quarks", json={"name":"top","charge":"+2/3"})
#
#   curl -X GET http://127.0.0.1:5000/insert/DA/Alameda -H 'Content-Type: application/json'   -d '{"location": "Alameda" , "name": "DA" , "description": "Direcao academica" , "time":"9:30 - 17:00" }'
#
################################################################################################

@app.route('/insert/<path:subpath>', methods = ['GET','POST','PUT'])
def insert(subpath):
    
    #We need to check if json data is correctly composed 
    keys = str(subpath).split("/")
    
    
    # name/local  - primary keys 
    res = request.get_json()
    print(res)
    # set(d_1.keys()) == set(d_2.keys()) check if have the same type
    if not res:
        return make_response(jsonify({"error": "Missing data for insert "+str(keys[0])+ "," + str(keys[1]) + "@database" }), 400)

    print("Insert:", res)

    status = db.insert(res)
    
    if status == 200:
        res = make_response(jsonify({"message": "Collection replaced"}), 200)
        return res
    elif  status == 201:
        res = make_response(jsonify({"message": "Collection created"}), 201)
        return res
    else:
        abort(404)


# http://127.0.0.1:5000/DA/Alameda >> name/local
@app.route('/secretariat/<path:subpath>', methods = ['GET','POST'])
def find(subpath):
    
    keys = str(subpath).split("/")
    data  = db.find(keys[0],keys[1])
    if data == 400:
        abort(404)
    else:
        return  make_response(jsonify(data), 200) 
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = '5002',debug = True)
    pass





