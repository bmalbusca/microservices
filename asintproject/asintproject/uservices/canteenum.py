from flask import Flask , redirect, url_for, request, render_template, jsonify
import requests as req
import json
import datetime
from menu import Menu 

API_canteen = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"
    
def ifexist_menu(self, date):
    if date in self.menu.keys():
        return self.menu[date]
    else:
        request_new()
        parse_json()
        return self.menu[date]


app = Flask(__name__)
menu= Menu(API_canteen)
menu.add_menu()


data = json.loads(req.get(API_canteen).text)



@app.errorhandler(404)
def page_not_found(e):
    print("request >> ","{}/{}".format(request.script_root, request.path))
    return  "Page not found", 404

@app.route('/api', methods = ['GET', 'POST'] )
def api(): 
    resp = req.get(API_canteen)
    return jsonify(resp.json())

@app.route('/menu', methods = ['GET','POST'] )
def menu_api():
    return menu.dump()

@app.route('/', methods = ['GET','POST'] )
def link():
    return "canteen API v1.1"


@app.route('/menu/<path:subpath>')
def find(subpath):
    print(subpath)
    return str(subpath)
# aka my first flask code
@app.route('/login/<name>')
def fail(name="none"):
   return 'welcome %s - Sign in failed' % name

if __name__ == '__main__':
    app.run(debug = True)
    pass
