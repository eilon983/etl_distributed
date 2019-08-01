import socket
import threading
from abc import abstractmethod
import time
import ehe.mysql
import ehe.oracle
import json

ENCODING = 'utf-8'


class BaseAgent(threading.Thread):

    def __init__(self, my_host, my_port, agents_map, frequency):
        threading.Thread.__init__(self, name="messenger_receiver")
        self.agents_map = agents_map
        self.host = my_host
        self.port = my_port
        self.mysql = ehe.mysql.MySql()
        self.oracle = ehe.oracle.Oracle()
        self.frequency = frequency
        self.agents_book = {}   # dictionary of 'contact book' with the details of all the available agents
        self.json = {
            'sender': {'agent_name': '', 'address': {'ip': '', 'port': ''}},
            'target': {'agent_name': '', 'ip': '', 'port': ''},
            'body': {'type': '', 'data': ''},
        }

    # getters
    def get_agents_map(self, key):
        my_list = self.agents_map[key]
        return my_list

    def get_agents_book(self, key):
        my_list = self.agents_book[key]
        return my_list

    # setters
    def set_agents_map(self, list, key):
        self.agents_map[key] = list

    def set_agents_book(self, agent_name, agent_address):
        self.agents_book[agent_name] = agent_address


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

    # --send new messages and waits the receiver to answer and close connections
    def send(self, send_list):
        for package in send_list:
            json_obj = json.loads(package)
            t = threading.Thread(target=self.send_package, args=(json_obj,))
            t.start()

    # --send a single package
    def send_package(self, package):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((package.target.ip, package.target.port))
        sock.sendall(package)

    # ---checks every x millisconds(frequency) if there was an update in db
    def db_listner(self):
        while True:
            time.sleep(5)
            t1 = threading.Thread(target=self.start_listner, args=(connection, data))
            t1.start()

    @abstractmethod   # implement in derived class
    def start_listner(self):
        pass

    @abstractmethod
    def receive(self, connection, data):
        pass

    #  receive:
    def pinged(self, connection, messege):
        self.set_agents(self, messege.body.data)
        connection.close()

    def get_agents_update(self, connection, messege):
        self.set_agents(self, messege.body.data)
        package = self.json
        package.body.type = 'data received'
        connection.sendall(package)
        connection.close()  # sent response close connection

    def set_agents(self, agents_list):
        for data, agents in agents_list:
            self.set_agents_map(self, agents, data)
            for agent in agents:
                self.agents_book[agent.agent_name] = agent.address

    # send:
    def send_data_request(self, data_types, agent):          # request data to other agent (main agent or agent X)
        package = self.json
        package.target = agent
        package.body.type = 'data request'
        package.body.data = data_types
        send_list = {package}
        self.send(send_list)

    def ping(self, data_types):
        package = self.json
        package.target = self.agents_book['Main agent']
        package.body.type = 'ping'
        package.body.data = data_types
        send_list = {package}
        self.send(send_list)

    def run(self):
        self.listen()

