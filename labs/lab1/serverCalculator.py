#!/usr/local/bin/python3
# which python3

import pickle
import os 
from  socket import *
from calculator import *

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'myfile.txt')

try:
    dump_in = open(my_file, 'rb')
    calc = pickle.load(dump_in)
    dump_in.close()
    print("Server - Loading data...abs")
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
        
        string = data.split(" ")

        if string[0] == "push":
            number = float(string[1])
            calc.pushValue(number)
            response = "ACKN"
            c.send(response.encode())
        elif string[0] == "pop":
            response = str(calc.popValue())
            c.send(response.encode())
        elif string[0] == "add":
            response = str(calc.add())
            c.send(response.encode())
        else:
            response = "NOP"
            c.send(response.encode())

        print("Server - Received, Acknowledge and Reply %i" %counter)
        counter +=1;
   
    except KeyboardInterrupt:
        print("Server - Ctrl-C interrupt received, saving data...")
        dump_out = open(my_file,'wb')
        pickle.dump(calc ,dump_out)
        dump_out.close();
        s.close()
        c.close()
        break
    

c.close()




