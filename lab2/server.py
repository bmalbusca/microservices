import Pyro4
from  bookDB import *
from  classBook import book

Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')

#@expose as wrapper function:
book_data = book("Bruno", "1",2,3)

ExposedClass = Pyro4.expose(book)
db = ExposedClass()

daemon = Pyro4.Daemon()
uri2 = daemon.register(book_data,"book") #Send a object (data)
uri= daemon.register(db, "book_class") #Send bookDB class 

print(uri2) #Try also uri 
print("Running...")

daemon.requestLoop()




