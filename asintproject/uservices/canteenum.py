from flask import Flask , redirect, url_for, request, render_template, jsonify
import requests as req
import json
import datetime

API_canteen = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"

class MenuDB(object):
    def __init__(self, url, date=None, data_json=None, menu= {}):
        self.data = data_json #nao faz sentido guardar isto
        self.data_time = date #nao faz  sentido 
        self.url_api = url
        self.menu = menu     
        self.tomorrow  = None 
        self.today = None 
    
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

@app.errorhandler(404)
def page_not_found(e):
    return  'Page not found', 404

@app.route('/api', methods = ['GET', 'POST'] )
def api(): 
    resp = req.get(API_canteen)
    menu.request_new()
    return jsonify(resp.json())

@app.route('/menu', methods = ['GET','POST'] )
def menu_api():
    return json.dumps(menu.data)




@app.route('/<date>', methods = ['GET', 'POST'])
def show(date="none"):
    return json.dumps(list(menu.data[date]))

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


#here we are assign the template to the POST form located at localhost/
@app.route('/login',methods = ['POST'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        num = request.form['id']
        form = request.form
        if user == "john" or str(num) is "1":
            return redirect(url_for('fail',name = user))
        else: 
            #return redirect(url_for('datab', request=form))
            return render_template('database.html',result=form)

    #index()
    #return render_template('login.html') # If you use GET, you also need to do the render first - can use the index() or do directly the call for render_template()


if __name__ == '__main__':
   app.run(debug = True)