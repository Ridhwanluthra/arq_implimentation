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

data = ["" for _ in range(50)]
msg = ""

acks = []

end = False

def check(name):
    global msg, data, acks, end
    ack_counter = 0
    while 1:
        msg = s.recv(1024).decode('ascii')
        # print(msg)
        tem = msg.split(";")
        print(tem)
        for t in tem:
            # print(t)
            if t:
                if t[1:] == "end":
                    end = True
                    break

                acks.append(str((int(t[0]) + 1)))

                if int(t[0]) == ack_counter:
                    # print(t[1:])
                    data[int(t[0])] = t[1:]
                    # print(data[:10])
                    ack_counter += 1

        if end and not acks:
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
                hmm = True
                if hmm:
                    s.send(temp.encode('ascii'))
                    # print("ack sent for ", temp, "acks: ", acks)
            
            # print(len(acks))
            if end and len(acks) == 0:
                s.send("-1".encode('ascii'))
                import time
                time.sleep(1)
                break
    finally:
        print("".join(data))
        s.close()