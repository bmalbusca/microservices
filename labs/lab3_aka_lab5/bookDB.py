
"""
bookDB
The bookDB class contains an array of books and should implement the following methods:
• Insert book
• Show book (using the book identifier)
• List all authors
• List books from a certain author
• List book publish in a certain year
Every time a book is inserted, the database should be serialized into a backup file using the pickle functions.

"""
import pickle
import os
import Pyro4

from classBook import *

@Pyro4.expose 
class BookDB:
    def __init__(self):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

        self.books = []
        self.books_from_author = {}
        self.books_from_year = {}
        self.backup_directory = os.path.join(THIS_FOLDER, 'backup.txt')

    def unique(self,new_book):
        if(self.books):
            for book in self.books:
                if new_book.identifier == book.identifier:
                    return False
        return True

    def insert(self,new_book):
       
        if (self.unique(new_book)):
            self.books.append(new_book)

            try:
                dump_out = open(self.backup_directory,'wb')
                pickle.dump(new_book ,dump_out)
                dump_out.close();
            except:
                pass
        
            try:
                self.books_from_author[new_book.author].append(new_book)
            except:
                self.books_from_author[new_book.author]=[]
                self.books_from_author[new_book.author].append(new_book)
        
            try:
                self.books_from_year[new_book.year].append(new_book)  
            except:
                self.books_from_year[new_book.year]=[]
                self.books_from_year[new_book.year].append(new_book) 
        else:
            print("Already exists")

    def authors(self):
        for name in self.books_from_author.keys():
            print(name, " ")
        print("\n")
    
    def print_book(self,data):
        print(" Book ID: ",data.identifier,"\n" ,"Title: ",data.author," ",data.year)
        
    def book_list(self):
        if(self.books):
            for book in self.books:
                self.print_book(book)
        return self.books  

    def find_book_author(self, author):
        try:
            keybook = self.books_from_author[author]
            if(keybook):
                for data in keybook:
                    self.print_book(data)
        except:
            print("Does not exist")


    def find_book_year(self, year):
        try:
            keybook = self.books_from_year[year]
            if(keybook):
                for data in keybook:
                    self.print_book(data)
        except:
             print("Does not exist")

    def find_book_id(self,id):
        if(self.books):
            for data in self.books:
                if data.identifier == id:
                    self.print_book(data)
                    return book 
            print("Does not exist")

    def insert_book(self, author,title,year,ID):
        new_book = book(author,title,year,ID)
        self.insert(new_book)

