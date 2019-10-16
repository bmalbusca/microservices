import Pyro4
from  bookDB import *
from  classBook import book

Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')

'''
remoteDB=Pyro4.expose(bookDB)
daemon = pyro4.Deamon(..)
bd =remoteBD()
uri=daemon.register(bd, "mom")
print uri
daemon.requestloop()
'''

ExposedClass = Pyro4.expose(book)
#ExposedClass = Pyro4.expose(BookDB)
db = ExposedClass()

daemon = Pyro4.Daemon()
uri= daemon.register(db, "book")

print(uri)
print("Running")

daemon.requestLoop()




