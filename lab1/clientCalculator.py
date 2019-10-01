from socket import *


s = socket()

host = '127.0.0.1'
port= 12345
s.connect((host,port))

while True:
    data = input("Insert numbers:")
    byte = str(data)
    try:
        s.send(byte.encode())
    except:
        print("Broken pipe")

