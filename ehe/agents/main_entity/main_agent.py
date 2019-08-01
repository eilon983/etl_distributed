import socket
import threading
import json
from ehe.agents.base_agent import BaseAgent
ENCODING = 'utf-8'


class MainAgent(BaseAgent):

    def __init__(self, my_host, my_port, frequency):
        super(BaseAgent, my_host, my_port, frequency)
        self.json.agent_name = 'Main agent'
        self.json.address.ip = self.host
        self.json.address.port = self.port
        self.waiting_list = {}  # dictionary of lists. key = data type, value: list of agents who wait for data types

    # in case agents make FIRST connection
    def pinged(self, connection, message):
        sender = message['sender']
        self.agents_book[sender['name']] = sender
        # message.body.type['ping'] is list of the demanded data types with the ping
        self.data_request(self, connection, message)
        pass

    # in case agents ask for data: ping / data request , sends data and close connection
    def data_request(self, connection, message):
        sender = message['sender']
        response = self.bridge(message.body.data, sender)
        if message.body.type == "ping":
            response.body.type = 'ping_response'
        elif message.body.type == "data request":
            response.body.type = 'data_response'
        connection.sendall(response)
        connection.close()  # sent response close connection

        # update the waiting list
        self.update_waiting_list(sender['data_types'], sender)

    # in case agent wants other agent connection
    def bridge(self, data_types, sender):
        contacts = {}
        for dt in data_types:
            contacts[dt] = self.get_agent(dt, sender)  # returns agent
        response = self.json
        response.body.data = contacts

        return response

    # runs over all the waiting list and notify them if the current agent has information for them
    def update_waiting_list(self, data_types, sender):  # data_types = list of cols
        agents_to_update = {}
        for dt in data_types:
            if dt in self.waiting_list:                       # in case cur agent data in waiting list:
                for agent in self.waiting_list[dt]:      # for each agent update cur agent detail
                    agents_to_update[agent.agent_name].append(dt)
                self.waiting_list.pop(dt)                         # remove data type from waiting list
        self.update_agents(agents_to_update, sender)

    def update_agents(self, agents_to_update, data_agent):
        send_list = {}
        for agent_name, dts in agents_to_update:   # key = agent name, value = the list of data types to update him
            package = json
            package.sender = {'agent_name': 'main agent','address': {'ip': self.ip, 'port': self.port}}
            package.target = self.agents_book[agent_name]
            package.body.type = {'new agent update' : data_agent}
            package.body.data = dts
            send_list.append(package)
        self.send(send_list)

    # get the requested data type, and the agents who asked for dt
    # if data type not exists add the agent to the waiting list
    def get_agent(self, data_type, sender):
        for agent in self.agents_book:
            if data_type in agent['data_type']:
                return agent
        self.waiting_list[data_type].append(sender)
        return "Not Available"

    def receive(self, connection, message):
        if "ping" in message.body.type:
            self.pinged(connection, message)
        if "update received" in message.body.type:
            connection.close()
        if "data request" in message.body.type:
            self.data_request(self, connection, message)
        pass


# starts the system, call base class
if __name__ == '__main__':
    agent = MainAgent(

    )
    agent.start_system(my_host= '', my_port='',frequency='')





