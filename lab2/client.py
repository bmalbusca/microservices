import Pyro4
import UIDB as db
from  classBook import *
from bookDB import *
from classBook import *

Pyro4.config.SERIALIZER = 'pickle'

uri = input("What is your uri?: ")

print("Testing connection",uri)

book = Pyro4.Proxy(uri)
book.test()
book.test()

