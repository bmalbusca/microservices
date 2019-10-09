"""dbUI
The dbUI will allow the interaction with the bookDB from the keyboard.
The dbUI should be a class that reads commands from the keyboard and accesses the methods of the database class:
• NEW
• SHOW
• AUTHORS
• SEARCH_AUTH • SEARCH_YEAR
"""
from bookDB import *

class dbUI:
    def __init__(self):
        self.last_command=None
        self.database =None
    def new_db(self):
        self.database = bookDB()
    def read(self):
        comm = input("Insert command: ")
        name = comm.split(" ")
        if comm.strip() ==  "NEW":
            self.new_db()
            print(self.database)
            self.last_command = comm
        elif comm.strip() == "SHOW":
            print(self.database.books)
            self.database.book_list()
            self.last_command = comm
        elif comm.strip() == "AUTHORS":
            self.database.authors()
            self.last_command = comm
        elif name[0] == "SEARCH_AUTH":
            self.database.find_book_author(name[1])
            self.last_command = name[0]
        elif name[0] == "SEARCH_YEAR":
            self.database.find_book_year(name[1])
            self.last_command = name[0]
        elif name[0] == "NEW_BOOK":
            print("Data received: ",len(name))
            if len(name) == 5:
                self.database.insert_book(name[1],name[2],float(name[3]),name[4])
            else:
                print("Book miss information")
        else:
            print("NOPE ",comm)
    
