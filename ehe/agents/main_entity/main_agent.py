import socket
import threading
#import repo
import ehe
ENCODING = 'utf-8'


class MainAgent(threading.Thread, ehe.agen):
    def __init__(self, my_host, my_port):
        threading.Thread.__init__(self, name="Main_Agent")
        self.host = my_host
        self.port = my_port
        self.agentsList = []
        self.data_waiting_list = []

    def check_data_request(self, data):
        agents = []
        for i in range(self.agentsList.__len__()):
            cur_data = self.agentsList[i][3]
            if cur_data.__contains__(data):
                agents.append(self.agentsList[i][0])
        return agents

    def add_data_request(self, data, user_name):
        exists = False
        for i in range( self.data_waiting_list.__len__()):
            if self.data_waiting_list[i][0] == data:
                self.data_waiting_list[i][1].append(user_name)
                exists = True
                break
        if not exists:
            self.data_waiting_list.__add__([data, [user_name]])

    def send_data(self, agents_data, user_name):
        found_user = False
        for i in range(self.agentsList.__len__()):
            if self.agentsList[i][0] == user_name:
                sender = Sender(self.agentsList[i][2], self.agentsList[i][3])
                found_user = True
        if found_user:
            message = "data_reply {}".format(agents_data)
            sender.send(message)
        else:
            print("no connection to {} user".format(user_name))

    def resolve_message(self, message):
        if "connect_request" in message:
            print("connect request received")
            arr = message.split("|")
            if len(arr) == 5:
                user_name = arr[1]
                user_host = arr[2]
                user_port = arr[3]
                user_data = arr[4]  #data list
                print("adding user: {}, {}, {}, {}".format(user_name, user_host, user_port, user_data))
                agent = [user_name, user_host, user_port, user_data]
                self.agentsList.append(agent)
            else:
                print("invalid connect request...")
        elif "data_request:" in message:
            print("data request received")
            arr = message.split("|")
            if len(arr) == 3:
                user_name = arr[1]
                user_data_request = arr[2]
                agents_data = self.check_data_request(user_data_request)
                if agents_data.__len__() == 0:
                    self.add_data_request(self, user_data_request, user_name)
                else:
                    self.send_data(agents_data, user_name)
            else:
                print("invalid data request...")
        elif "from:" in message:
            print("received message... starting queueing process")
            arr = message.split("|")
            if len(arr) == 2:
                sender_name = arr[0].replace("from:", "")
                print("adding message from {} to queue".format(sender_name))
                message_text = arr[1]
                self.queue.add_message(sender_name, message_text)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(10)
        while True:
            connection, client_address = sock.accept()
            print("connection received from {}".format(str(client_address)))
            try:
                full_message = ""
                while True:
                    data = connection.recv(16)
                    full_message = full_message + data.decode(ENCODING)
                    if not data:
                        print("received message: [{}]".format(full_message))
                        self.resolve_message(full_message.strip())
                        break
            finally:
                print("exchange finished. closing connection")
                connection.shutdown(2)
                connection.close()


class Sender(threading.Thread):

    def __init__(self, host, port):
        threading.Thread.__init__(self, name="main_agent_sender")
        self.host = host
        self.port = port

    def send(self, message):
        print("sending message {} to {}".format(message, str((self.host, self.port))))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.host, self.port))
            s.sendall(message.encode(ENCODING))
        finally:
            print("message has been sent. closing connection")
            s.shutdown(2)
            s.close()

#    def run(self):
#       while True:
#          if self.queue.messages_waiting():
            #                print("there are messages on queue. popping one")
            #   message = self.queue.pop_message()
            #   users = self.users.all_users()
            #   for user in users:
            #       if user.get("name") != message.get("sender"):
            #           self.send("{}: {}".format(message.get("sender"), message.get("message")), user.get("host"),
#                     user.get("port"))


def main():
#    users = repo.Users()
    my_host = input("my host: ")
    my_port = int(input("my port: "))
    receiver = MainAgent(my_host, my_port)
    send_host = input("server host: ")
    send_port = int(input("server port: "))
    sender = Sender(send_host, send_port)
    threads = [receiver.start(), sender.start()]

if __name__ == '__main__':
    main()