#!/usr/bin/python3           # This is client.py file

import socket
import random

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()

port = 9999

# connection to hostname on the port.
s.connect((host, port))

data = ""
msg = ""

def decision(probability):
    return random.random() < probability

try:
    while 1:
        msg = s.recv(1024).decode('ascii')
        data += msg

        if decision(0.7):
            s.send(str((int(msg[0]) + 1) % 2).encode('ascii'))
            print(msg)
        else:
            print(msg)
        
        
        if msg[-3:] == "end":
            break
finally:
    s.close()