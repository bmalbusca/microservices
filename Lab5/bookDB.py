"""
Created on Fri Oct 10 10:02:24 2014

@author: jnos
"""
import book
import pickle


class bookDB:
        def __init__(self, name):
                self.name = name
                try:
                        f = open('bd_dump'+name, 'rb')
                        self.bib = pickle.load(f)
                        f.close()
                except IOError:
                        self.bib = {}
        def addBook(self, author, title, year):
                b_id = len(self.bib)
                self.bib[b_id] = book.book(author, title, year, b_id)
                f = open('bd_dump'+self.name, 'wb')
                pickle.dump(self.bib, f)
                f.close()
        def showBook(self, b_id):
                return self.bib[b_id]

        def listAllBooks(self):
                return list(self.bib.values())

        def listBooksAuthor(self, authorName):
                ret_value = []
                for b in self.bib.values():
                        if b.author == authorName:
                                ret_value.append(b)
                return ret_value
        def listBooksYear(self, year):
                ret_value = []
                for b in self.bib.values():
                        if b.year == year:
                                ret_value.append( b)
                return ret_value


