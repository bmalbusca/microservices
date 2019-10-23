#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 11:50:49 2019

@author: carina
"""
import Pyro4
import bookDB

#s.connect((host, port))


#falta à classe as cenas para fazer a comunicacao server client, logo faço:
remoteLibrary = Pyro4.expose(bookDB.bookDB)

db = bookDB.bookDB("mylib")
#remoteBook vai ter tudo o que vem do bookDB mas as cenas do Pyro
#vai entao ter o modulo de comunicacao e o dispatch
#o = remoteBookDB() #crio o obj como se         fosse local

#create a Pyro server with defined host 
daemon = Pyro4.Daemon(host="194.210.157.245") #194.210.157.245 #hostname -I

# create remote obj uri and make it available to be accessible remotely
uri = daemon.register(db, "bookDB")
print(uri)

#locauriuri
ns = Pyro4.locateNS(host = "146.193.41.139", port = 9090)
#register the uri of this server in the name server, naming it "elnome"
ns.register("elnome", uri)

#start request loop
daemon.requestLoop()    


#pyro4-nsc -n 146.193.41.139 list #list all servers

