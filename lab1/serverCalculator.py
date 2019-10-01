#!/usr/local/bin/python3
# which python3

import pickle 
from  socket import *
from calculator import *

try:
    dump_in = open("dump.txt", 'rb')
    calc = pickle.load(dump_in)

except:
    calc = rpnCalculator()

s = socket(AF_INET, SOCK_STREAM)
host = '127.0.0.1'
port = 12345

s.bind((host,port))
s.listen(1)



c, addr = s.accept()
print("Server connected to"+ str(addr))

counter = 0;
while True:
    
    try:
       
        byte = c.recv(1024)
 
        data = byte.decode()
        number = float(data)
        calc.pushValue(number)
    
        response = str(calc.popValue())
        c.send(response.encode())
        print("Server - Received, Acknowledge and Reply %i" %counter)
        counter +=1;
   
    except KeyboardInterrupt:
        print("W: interrupt received, saving data...")
        dump_out = open("dump.txt ","wb")
        pickle.dump(calc ,dump_out)
        dump_out.close();
        break
    

c.close()




