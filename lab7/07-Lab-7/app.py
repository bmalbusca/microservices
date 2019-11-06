from flask import Flask
from flask import render_template
from flask import request
import bookDB

app = Flask(__name__)
db = bookDB.bookDB("mylib")

@app.route('/')
def hello_world():
    count = len(db.listAllBooks())
    return render_template("mainPage.html", count_books=count)



@app.route('/addBooksForm')
def add_Book_Form():
    return render_template("addBookTemplate.html")

@app.route('/listAllBooks',methods=['POST'])
def list_all_form():
    book = showBook(1);
    return render_template("showAll.html")

@app.route('/addBook', methods=['POST', 'GET'])
def add_Book():
    if request.method == "GET":
        return str(request.args)
    else:
        return str(request.form)
    return render_template("addBookTemplate.html")

@app.route('/crash')
def main():
    raise Exception()

if __name__ == '__main__':
    app.run(debug=True)
