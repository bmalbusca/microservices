from  socket import *
from calculator import *

calc = rpnCalculator()

s = socket()
host = '127.0.0.1'
port = 12345

s.bind((host,port))
s.listen(1)


while True:
    c, addr = s.accept()
    
    while True:
        byte = c.recv(1024)
    
        data = byte.decode()
        number = float(data)
        calc.pushValue(number)
    
        print(calc.memory)
    
    c.close()
