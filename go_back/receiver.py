#!/usr/bin/python3           # This is client.py file

import socket
import random
import _thread

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()

random.seed(input())

port = random.choice(list(range(1111, 9997)))

# connection to hostname on the port.
try:
    s.connect((host, port))
except OSError:
    s.connect((host, random.choice(list(range(1111, 9997)))))

data = ""
msg = ""

acks = []

end = False

def check(name):
    global msg, data, acks, end
    ack_counter = 0
    while 1:
        msg = s.recv(1024).decode('ascii')
        tem = msg.split(";")
        for t in tem:
            if t:
                if t[1:] == "end":
                    end = True
                    break

                acks.append(str((int(t[0]) + 1)))

                if int(t[0]) == ack_counter:
                    data += t[1:]
                    ack_counter += 1

        if end:
            break

                


def decision(probability):
    return random.random() < probability

if __name__ == "__main__":
    try:
        _thread.start_new_thread(check, ("ack_checker",))
        while 1:
            if acks:
                hmm = decision(0.7)
                temp = acks.pop(0) + ";"
                if hmm:
                    s.send(temp.encode('ascii'))
                    print("ack sent for ", temp, "acks: ", acks)
            
            # print(len(acks), end)
            if end and len(acks) == 0:
                break
    finally:
        print(data)
        s.close()