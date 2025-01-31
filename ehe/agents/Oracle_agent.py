from ehe.agents.base_agent import BaseAgent
ENCODING = 'utf-8'


class OracleAgent(BaseAgent):

    def __init__(self, my_host, my_port, frequency):
        super(BaseAgent, my_host, my_port, frequency)
        self.json.agent_name = 'Oracle agent'
        self.json.address.ip = self.host
        self.json.address.port = self.port

    def receive(self, connection, message):
        if "ping response" in message.body.type:
            self.pinged(connection, message)
        if "new agent update" in message.body.type:  # - main agents alerts new data
            self.get_agents_update(self, connection, message)
        if "data response" in message.body.type:  # - agent X alerts new data
            self.get_data_update(self, connection, message)
        if "data request" in message.body.type:  # - other agent asks for data
            self.data_request_response(self, connection, message)
        if "update received" in message.body.type:
            connection.close()
        pass

    def get_data_update(self, connection, messege):
        self.oracle.execute_to_dataframe(self, messege.body.data)
        connection.close()

    def data_request_response(self, connection, message):
        package = self.json
        package.body.type = 'data response'
        data_response = {}
        for dt in message.body.data:
            data_response[dt] = self.oracle.execute_to_dataframe(self, dt)
        package.body.data = data_response
        connection.sendall(package)
        connection.close()  # sent response close connection
