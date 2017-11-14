#!/usr/bin/python3           # This is server.py file
import socket
import random

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()

port = 9999

# bind to the port
serversocket.bind((host, port)) 

# queue up to 5 requests
serversocket.listen(5)

msg = "abcdefg"

packets = [str(msg[i:i+1]) for i in range(0, len(msg), 1)]
# print(len(packets[0]))
# for pack in packets:
#   print(pack[0], len(msg)/1023)

clientsocket, addr = serversocket.accept()
print("Got a connection from {}".format(addr))

i = 0

sequence = 0

clientsocket.settimeout(1.0)

def decision(probability):
    return random.random() < probability 

try:
    while i <= len(packets):
        if i == len(packets):
            msg = str(sequence) + "end"
        else:
            msg = str(sequence) + packets[i]
        
        if decision(0.7):
            clientsocket.send(msg.encode('ascii'))
            print("sent: {}".format(msg))
        else:
            print("sent: {}".format(msg))
        
        try:
            ack = clientsocket.recv(1024)
        except socket.timeout:
            print("timeout")
            continue

        if int(ack) == (sequence + 1) % 2:
            i += 1
            sequence = (sequence + 1) % 2
        else:
            continue
finally:
    clientsocket.close()
    serversocket.close()