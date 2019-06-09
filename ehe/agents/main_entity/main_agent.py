import socket
import threading
from ehe.agents.base_agent import BaseAgent
ENCODING = 'utf-8'


class MainAgent(BaseAgent):
    def __init__(self, my_host, my_port,frequency):
        super(BaseAgent,my_host,my_port,frequency)
        self.waiting_list = {} # dictionary of lists. key = data type, value: list of agents who wait for data types
        self.agents_book = {}  # dictionary of 'contact book' with the details of all the available agents

    # ---in case agents make FIRST connection
    def pinged(self,data):
        sender = data['sender']
        self.agents_book[sender['name']]=sender
        self.check_waiting_list(sender['data_type'])
        pass

    # --in case agent wants other agent connection
    def bridge(self,data):
        requested_dataTypes = data.request.array
        contacts = {}
        for dt in requested_dataTypes:
            agent = self.get_agent(dt)
            contacts[dt] = self.get_agent(dt)
        self.send(data.sender.address,contacts)

    # ---runs over all the waiting list and notify them if the current agent has information for them
    # todo it smart
    def check_waiting_list(self,data_types):
        ############to build##############
        for dt in data_types:
            if dt in self.waiting_list:
                #todo
                pass


    # ---get the requested data type, and the agents who asked for dt
    # ---if data type not exists add the agent to the waiting list
    def get_agent(self,data_type,agent):
        for agent in self.agents_book:
            if data_type in agent['data_type']:
                return agent
    # ---in case there is no agent who can send the data type
        self.waiting_list[data_type].append(agent['name'])
        return 'Not Available'

    # todo: call the functions from here according to the json in message
    def receive(self, message):
        request_type = message.request.type
        pass

#-- starts the system, call base class
if __name__ == '__main__':
    agent = MainAgent(

    )
    agent.start_system(my_host= '', my_port='',frequency='')





