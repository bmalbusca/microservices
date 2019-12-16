from flask import Flask , redirect, url_for, request, render_template, jsonify, abort 
import requests as req
import json
from datetime import *


datab = { "secretariats" : [ {"location": "Alameda" , "name": "DA" , "description": "Direcao academica" , "time":"9:30 - 17:00" }  
            ]}

secretariat = {"location": "Alameda" , "name": "DA" , "description": "Direcao academica" , "time":"9:30 - 17:00" }  

class Database(object):

    def __init__(self,data={"secretariats" :[]} ):
        self.database = data

    def insert(self, data):
        try:
            for setdata in self.database["secretariats"]:
                if setdata["name"] == data["name"] and  setdata["location"] == data["location"]:
                    return
            self.database["secretariats"].append(data)

        except:
            print("Database not defined")
    
    def find(self, name, local):
        for data in self.database["secretariats"]:
            if name == data["name"] and local == data["location"] :
                return data
            else:
                return None
            
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

    


db = Database(datab)
db.printDB()

db.insert(secretariat)
db.printDB()
db.reset()
db.printDB()






