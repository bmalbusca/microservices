from flask import Flask , request, jsonify
import requests as req
import json
from datetime import * 

"""
    @Class Menu 
    Canteen microservice 
    note: date example 12/2/2015 
"""

class Menu(object):
    def __init__(self, url,  menu= {}):
        self.url_api = url
        self.menu = menu

    def request_url(self, url):
        return self.json_to_py(req.get(url).text)

    def request(self):
        return self.json_to_py(req.get(self.url_api).text)

    def json_to_py(self, json_file):
        return json.loads(json_file)

    def add_menu(self, data={}): 
        if not data:
            data = self.request()

        if (data): 
            for day in data:
                if day["day"] not in self.menu.keys():
                    self.menu[day["day"]] = day["meal"] 
    
    def data_dump(self, dic):
        return json.dumps(dic)

    def order(self):
        self.menu = sorted(self.menu.items(), key = lambda x:datetime.strptime(x[0], '%d/%m/%Y'), reverse=True)

    def find(self, key):
        if key in  self.menu.keys():
            return self.data_dump(self.menu[key])
        else:
            resp = self.request_url(self.url_api + "/?day=" + key)
            
            if 'error' in resp:
                return 404
            else:
                self.add_menu(resp)
                try:
                    return self.data_dump(self.menu[key])
                except: 
                    return 404
    def dump(self):
        return json.dumps(self.menu)


