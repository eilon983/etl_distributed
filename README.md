# etl_distribute

'data' is json structure:

{
  "sender": {
    "agent_name": "Oracledadada",
    "address": {
      "ip": "1234.1234.1234.1234",
      "port": "1111"
    },
    "data_type": "['person info', 'companies location']"
  },
  "request": {
    "type": "request_for_data/request_for_agent_details/ping",
    "get_data": {
      "timestamp": "2019-06-05",
      "key": "'id'",
      "array": "[id1,id2,id3,id4]"
    }
  },
  "response": {
    "answer": "data/agent detail",
    "data": "list of sql rowsֿ",
    "agent": {
      "agent_data_type": "['person info', 'companies location']",
      "agent_ip": "0000.0000.0000.0000",
      "agent_port": "4444"
    }
  }
}
