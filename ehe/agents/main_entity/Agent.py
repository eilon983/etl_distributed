import socket
import sys
import threading
from abc import abstractmethod


class Agent:

    list_of_data_types=['telephone numbers', 'credit cards numbers', 'birth dates']

    HOST = ''  # all availabe interfaces
    PORT = 9999  # arbitrary non privileged port

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Could not create socket. Error Code: ", str(msg[0]), "Error: ", msg[1])
        sys.exit(0)

    print("[-] Socket Created")

    # bind socket
    try:
        s.bind((HOST, PORT))
        print("[-] Socket Bound to port " + str(PORT))
    except socket.error as msg:
        print("Bind Failed. Error Code: {} Error: {}".format(str(msg[0]), msg[1]))
        sys.exit()

    s.listen(10)
    print("Listening...")


    def client_thread_receive(conn):
        conn.send("Welcome to the Server. Type messages and press enter to send.\n")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            reply = "OK . . " + data
            conn.sendall(reply)
        conn.close()

    @abstractmethod
    def client_thread_send(self):
        pass

    while True:
        #waits to accept a connection
        conn, addr = s.accept()
        print("[-] Connected to " + addr[0] + ":" + str(addr[1]))

        #creating another thread after recognize a connection
        #this thread will be closed after receving data
        t1 = threading.Thread(client_thread_receive(conn))
        t1.start()

    s.close()
