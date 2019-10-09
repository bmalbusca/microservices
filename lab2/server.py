import pyro4
from bookDB import *
'''
remoteDB=Pyro4.expose(bookDB)
daemon = pyro4.Deamon(..)
bd =remoteBD()
uri=daemon.register(bd, "mom")
print uri
daemon.requestloop()

'''
daemon = Pyro4.Daemon()
obj = exposedClass()
uri= daemon.register(obj,"objName")
daemon.requestLoop()


