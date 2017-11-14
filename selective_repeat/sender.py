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
end = False
i = 0
sequence_list = []

ack_list = []

clientsocket.settimeout(1.0)

def check_ack(name):
    global i, j, ack_list, end
    ack_counter = 0
    while 1:
        try:
            ack = clientsocket.recv(1024).decode('ascii')
            tem = ack.split(";")
            for t in tem:
                if t:
                    # print("got ack", t)
                    ack_list.append(t)

                    if int(t) in sequence_list:
                        del sequence_list[sequence_list.index(int(t))]

                    if int(t) == -1:
                        end = True
                        break
                if end and not sequence_list:
                    break
                    # else:
                        # if int(t) in ack_list:
                        #     ack_counter += 1
                        # send_msg(ack_counter)
                        # while 1:
                        #     pass
            # print(ack_counter)
        except socket.timeout:
            print("timeout")
            if sequence_list:
                send_msg(sequence_list.pop(0) - 1)
            elif end:
                break
            # ack_counter += 1

            # while 1:
            #     if str(ack_counter) in ack_list:
            #         ack_counter += 1
            #     else:
            #         break
            # sequence_list = []


        # for a in ack_list:
        #     if int(a) in sequence_list:
        #         del sequence_list[sequence_list.index(int(a))]
            
        #     if int(a) == -1:
        #         end = True
        # if end:
        #     break


# window = [True for _ in range(4)]
# timers = [threading.Timer(1.0, check_ack, ack, i) for _ in range(4)]

def decision(probability):
    return random.random() < probability 

def send_msg(index):
    if index == len(packets):
        msg = str(index) + "end;"
    else:
        msg = str(index) + packets[index]

    sequence_list.append(index + 1)
    print(msg)
    # print(msg)
    if decision(0.5):
        clientsocket.send(msg.encode('ascii'))

if __name__ == "__main__":
    try:
        _thread.start_new_thread(check_ack, ("ack_checkerack_checker",))
        while i <= len(packets):

            send_msg(i)

            # sequence_list.append(i)
            # print("sent: {}".format(msg))

            # while i == len(packets):
            # #     # print(i)
            #     continue
            while i == len(packets):
                if end:
                    break

            i += 1

            
    finally:
        clientsocket.close()
        serversocket.close()