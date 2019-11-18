from flask import Flask , redirect, url_for
app = Flask(__name__)

@app.route('/hello/<int:ID>')
def hello_world(ID):
    if ID == 1111:
        return redirect(url_for('wellcome'))
    else:
        return 'Hello World ID:' + str(ID)

@app.route('/')
def wellcome():
    return 'Hey mrs. User'

if __name__ == '__main__':
    app.debug = True   
    app.run()
