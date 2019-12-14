from flask import Flask , request, jsonify
import requests as req
import json

"""
    @Class 

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

    def add_menu(self,data={}):
        data = self.request() 
        if (data): 
            for day in data:
                if day["day"] not in self.menu.keys():
                    self.menu[day["day"]] = day["meal"]

    def dump(self):
        return json.dumps(self.menu)


