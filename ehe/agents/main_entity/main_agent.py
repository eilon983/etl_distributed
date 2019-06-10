import socket
import threading
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
    # todo it smart - done
    def check_waiting_list(self, data_types, agent_file):  # data_types = list of cols
        for dt in data_types:
            if dt in self.waiting_list:                       # in case cur agent data in waiting list:
                for agent_name in self.waiting_list[dt]:      # for each agent update cur agent detail
                    agent_data = self.agents_book[agent_name]
                    self.send(agent_data.address, agent_file)
                self.waiting_list.pop(dt)                     # remove data type from waiting list

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





