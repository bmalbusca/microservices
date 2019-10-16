import Pyro4
import os
import pickle

import UIDB as db 
#from bookDB import *


Pyro4.config.SERIALIZER = 'pickle'

uri = input("What is your uri?: ")

print("Testing connection",uri)


book  = Pyro4.Proxy(uri)

print(" Client: ",book.test(),"\n", "Client: *status* ->",book)



