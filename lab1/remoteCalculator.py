from  socket import *
from calculator import *

calc = rpnCalculator()

s = socket(AF_INET, SOCK_STREAM)
host = '127.0.0.1'
port = 12345

s.bind((host,port))
s.listen(1)



c, addr = s.accept()
#print("Server connected to"+ str(addr))

while True:
    byte = c.recv(1024)
    
    data = byte.decode()
    number = float(data)
    calc.pushValue(number)
    
    print(calc.memory)
    

c.close()
