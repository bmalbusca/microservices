import Pyro4
from  bookDB import *
from  classBook import book
import os
import threading
import time 

def thread_function(name):
    print("thread start",name)
    os.system('python3 -m Pyro4.naming')

    
server = threading.Thread(target=thread_function, args=(1,))
server.start()

time.sleep( 1 )

#Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')

#@expose as wrapper function:
book_data = book("Bruno", "1",2,3)

ExposedClass = Pyro4.expose(book)
db = ExposedClass()

daemon = Pyro4.Daemon(host= '194.210.176.234') #my local IP wget -qO- http://ipecho.net/plain | xargs echo

#uri2 = daemon.register(book_data,"book") #Send a object (data)
uri= daemon.register(db, "book_class") #Send bookDB class 

ns = Pyro4.locateNS(host= '127.0.0.1', port=9090) # python3 -m Pyro4.naming

ns.register("book", uri) 

#print(uri) #Try also uri 
print("Running...")

daemon.requestLoop()




