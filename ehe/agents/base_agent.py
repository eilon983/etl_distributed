import socket
import threading
from abc import abstractmethod
import time
import ehe.mysql
import ehe.oracle
import json

ENCODING = 'utf-8'



class BaseAgent(threading.Thread):

    def __init__(self, my_host, my_port,agents_map,frequency):
        threading.Thread.__init__(self, name="messenger_receiver")
        self.agents_map=agents_map
        self.host = my_host
        self.port = my_port
        self.mysql = ehe.mysql.MySql()
        self.oracle = ehe.oracle.Oracle()
        self.frequency = frequency

    #getters
    def get_agents_map(self,key):
        my_list = self.agents_map['key']
        return my_list

    #setter
    def set_agents_map(self,list,key):
        self.agents_map['key']=list

    def start_system(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(10)

        while True:
            connection, client_address = sock.accept()
            try:
                full_message = ""
                while True:
                    data = connection.recv(16)
                    t1 = threading.Thread(target=self.receive,args=(connection, json.loads(data)))
                    t1.start()
                    #full_message = full_message + data.decode(ENCODING)

                    if not data:
                        print(full_message.strip())
                        break
            finally:
                connection.shutdown(2)
                connection.close()

    def send(self,package):
        # send package to package.target.ip, package.target.port
        #TODO!!!
        jsonObj = json.loads(package)
        for node in send_list:
           pass #multi thread - open socket to node['address'] and send the data node['data']
        pass

    # ---checks every x millisconds(frequency) if there was an update in db
    def db_listner(self):
        while True:
            time.sleep(5)
            t1 = threading.Thread(target=self.start_listner, args=(connection, data))
            t1.start()

    @abstractmethod #implement in derived class
    def start_listner(self):
        pass

    @abstractmethod
    def receive(self, connection, data):
        pass

    def run(self):
        self.listen()

