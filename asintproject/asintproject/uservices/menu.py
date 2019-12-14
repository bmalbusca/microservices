from flask import Flask , request, jsonify
import requests as req
import json


class MenuDB(object):
    def __init__(self, url,  menu= {}):
        self.url_api = url
        self.menu = menu

    def request_new_url(self, url):
        return self.json_to_py(req.get(url).text)

    def request_new(self):
        return self.json_to_py(req.get(self.url_api).text)

    def json_to_py(self, json_file):
        return json.loads(json_file)

    def add_menu(self,menu)
        self.menu = menu 
