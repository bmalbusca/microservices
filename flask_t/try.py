from flask import Flask , redirect, url_for, request, render_template
app = Flask(__name__)


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
