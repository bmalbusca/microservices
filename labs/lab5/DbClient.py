#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 11:51:01 2019

@author: carina
"""

import Pyro4
import dbUI

        
#uri = input() #id da bd remota =???
#em vez de ler o URI to teclado leio do Name Server

ns = Pyro4.locateNS(host = "146.193.41.139", port = 9090)
uri = ns.lookup("elnome") #para obter o endereco do server correcto

# get proxy for the remote obj
db = Pyro4.Proxy(uri)
    
ui = dbUI.dbUI(db)
ui.menu()

