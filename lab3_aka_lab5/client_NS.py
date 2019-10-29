import Pyro4
import os
import pickle

import UIDB as db 
#from bookDB import *


#Pyro4.config.SERIALIZER = 'pickle'

ns = Pyro4.locateNS(host= '127.0.0.1', port=9090)


#uri = input("What is your uri?: ")
uri = ns.lookup("book")
print("Testing connection Naming Server",uri)


book  = Pyro4.Proxy(uri)

#new_book = book  #not callable, you need to use a function class's 
#new_book.test()

print(" Client: ",book.test(),"\n", "Client: *status* ->",book)





