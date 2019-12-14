from flask import Flask , redirect, url_for, request, render_template, jsonify
import requests as req
import json
import datetime

API_canteen = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"

class MenuDB(object):
    def __init__(self, url, data_json=None, menu= {}):
        self.data = data_json #nao faz sentido guardar isto
        self.url_api = url
        self.menu = menu     
    
    def request_new_url(self, url):        
        self.data = self.json_to_py(req.get(url).text)

    def request_new(self):        
        self.data = self.json_to_py(req.get(self.url_api).text)
        
    def json_to_py(self, json_file):
        return json.loads(json_file)
    
    def print_json(self):
        print(type(self.data))
        print(self.data[0]["day"]) 
    
    def parse_json(self):
        for day in self.data:
            if day not in self.data.key():
                self.menu[day["day"]]  = day["meal"]

    
    def ifexist_menu(self, date):
        if date in self.menu.keys():
            return self.menu[date]
        else:
            request_new()
            parse_json()
            return self.menu[date]


app = Flask(__name__)
menu= MenuDB(API_canteen)

data = json.loads(req.get(API_canteen).text)
#print(data)


menu = {}

for day in data:
    print(day["meal"], "\n")
    if day["day"] not in menu.keys():
        menu[day["day"]] = day["meal"]
print(data[0]["meal"])
#print(menu)




@app.errorhandler(404)
def page_not_found(e):
    print("request >> ","{}/{}".format(request.script_root, request.path))
    return  "Page not found", 404

@app.route('/api', methods = ['GET', 'POST'] )
def api(): 
    resp = req.get(API_canteen)
    menu.request_new()
    return jsonify(resp.json())

@app.route('/menu', methods = ['GET','POST'] )
def menu_api():
    return json.dumps(menu.data)


# aka my first flask code
@app.route('/fail/<name>')
def fail(name="none"):
   return 'welcome %s - Sign in failed' % name

#To render a heml file, you need to use the render_template  and the file need to be inside the "template" folder

@app.route('/database')
def datab(result):    
    return render_template('database.html',result=result)


@app.route('/')
def index():
    return render_template('login.html')
   
#The GET method is used to retrieve information from the given server using a given URI. 
# IF you want to render the page using GET (given a direct link), add "GET" to the method argument


if __name__ == '__main__':
 # app.run(debug = True)
  pass
