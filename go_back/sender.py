#!/usr/bin/python3           # This is server.py file
import socket
import random
import _thread

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()

random.seed(input())

port = random.choice(list(range(1111, 9997)))

# bind to the port
try:
    serversocket.bind((host, port))
except OSError:
    serversocket.bind((host, random.choice(list(range(1111, 9997)))))

# queue up to 5 requests
serversocket.listen(5)

msg = "abcdefgh"

packets = [str(msg[i:i+1]) + ";" for i in range(0, len(msg), 1)]
# print(len(packets[0]))
# for pack in packets:
#   print(pack[0], len(msg)/1023)

clientsocket, addr = serversocket.accept()
print("Got a connection from {}".format(addr))

j = 3

i = 0
sequence_list = []

ack_list = []

clientsocket.settimeout(1.0)

def check_ack(name):
    global i, j
    ack_counter = 0
    while 1:
        try:
            ack = clientsocket.recv(1024).decode('ascii')
            tem = ack.split(";")
            for t in tem:
                if t:
                    print("got ack", t)
                    ack_list.append(t)

                    if int(t) == ack_counter + 1:
                        ack_counter += 1
                    else:
                        i = ack_counter
                        # while 1:
                        #     pass
            # print(ack_counter)
        except socket.timeout:
            print("timeout")
            i = ack_counter
            # sequence_list = []


        for a in ack_list:
            if int(a) in sequence_list:
                j += 1
                del sequence_list[sequence_list.index(int(a))]
            
            if int(a) == -1:
                break


# window = [True for _ in range(4)]
# timers = [threading.Timer(1.0, check_ack, ack, i) for _ in range(4)]

def decision(probability):
    return random.random() < probability 


if __name__ == "__main__":
    try:
        _thread.start_new_thread(check_ack, ("ack_checkerack_checker",))
        while i <= len(packets):
            if i >= j:
                continue

            if i == len(packets):
                msg = str(i) + "end;"
            else:
                msg = str(i) + packets[i]
            # print(msg)
            if decision(0.7):
                clientsocket.send(msg.encode('ascii'))

            i += 1
            sequence_list.append(i)
            # print("sent: {}".format(msg))

            while i == len(packets) and sequence_list:
                # print(i)
                continue

            
    finally:
        clientsocket.close()
        serversocket.close()