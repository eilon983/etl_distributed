import socket
import threading
import json
from ehe.agents.base_agent import BaseAgent
ENCODING = 'utf-8'


class MainAgent(BaseAgent):
    def __init__(self, my_host, my_port, frequency):
        super(BaseAgent, my_host, my_port, frequency)
        self.waiting_list = {}  # dictionary of lists. key = data type, value: list of agents who wait for data types
        self.agents_book = {}   # dictionary of 'contact book' with the details of all the available agents

    # ---in case agents make FIRST connection
    def pinged(self, data):      # data = json file
        sender = data['sender']  # sender = ip,port
        self.agents_book[sender['name']] = sender
        self.check_waiting_list(sender['data_type'], sender)
        pass

    # --in case agent wants other agent connection
    def bridge(self, request_file):
        requested_data_types = request_file.request.array
        contacts = {}
        for dt in requested_data_types:
            agent  = self.get_agent(dt, request_file)
            if agent != "Not Available":
                contacts[dt] = agent

        if contacts.__len__() > 0:  #
            self.send(request_file.sender.address, contacts)

    # ---runs over all the waiting list and notify them if the current agent has information for them
    def check_waiting_list(self, data_types, agent_file):  # data_types = list of cols
        agents_to_update = {}
        for dt in data_types:
            if dt in self.waiting_list:                       # in case cur agent data in waiting list:
                for agent_name in self.waiting_list[dt]:      # for each agent update cur agent detail
                    agents_to_update[agent_name].append(dt)
                self.waiting_list.pop(dt)                         # remove data type from waiting list

        for agent_name in agents_to_update:
            agent_data = self.agents_book[agent_name]
            update_file = self.make_update_file(self, agent_file, agents_to_update[agent_name])
            self.send(agent_data.address, update_file)

    # -- make json file to update agent in waiting list for new data
    def make_update_file(self, agent_file, data_types):
        data_array = "["        # data array to string
        counter = 0             # count data amount to close string list
        for dt in data_types:
            if counter == len(data_types):
                data_array += "{}, ".format(dt)
                counter += 1
            else:
                data_array += "{}]".format(dt)

        # -- make json data filr:
        update_data = {'sender': [], 'request': [], 'response': []}
        update_data['sender'].append({
            'agent_name': "main agent",
            'address': {
                'ip':  "1234.1234.1234.1234",
                'port': '1111'
            },
            'data_type': "null"
        })
        update_data['request'].append({
            'type': '"new_agent_for_waiting_data"',
            'get_data': {
                'timestamp': '05-06-2019',
                'key': 'null',                    # array = [ [agent_name, agent_ip, agent_port], [data1, data2, ..] ]
                'array': "[ [{}, {}, {}], {}]".format(agent_file.agent_name, agent_file.address.ip, agent_file.address.port, data_array)
            }})
        update_data['response'].append({
            'answer': 'null',
            'data': 'null',
            'agent': {
                'agent_data_type': 'null',
                'agent_ip': 'null',
                'agent_port': 'null'
            }})

        with open('update_data.txt', 'w') as update_file:
            json.dump(update_data, update_file)
        return update_file

    # ---get the requested data type, and the agents who asked for dt
    # ---if data type not exists add the agent to the waiting list
    def get_agent(self, data_type, agent_requ):
        for agent in self.agents_book:
            if data_type in agent['data_type']:
                return agent
    # ---in case there is no agent who can send the data type
        self.waiting_list[data_type].append(agent_requ['name'])
        return "Not Available"

    def receive(self, message):
        request_type = message.request.type
        if request_type == "ping":
            self.pinged(message)
        elif request_type == "request_for_agent_details":
            self.bridge(message)
        pass


# -- starts the system, call base class
if __name__ == '__main__':
    agent = MainAgent(

    )
    agent.start_system(my_host= '', my_port='',frequency='')





