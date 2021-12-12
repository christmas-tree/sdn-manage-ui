from server.config import *

def auto_str(cls):

    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    cls.__repr__ = __str__
    return cls

# Chứa các thông tin về switch
@auto_str
class Switch():
    def __init__(self, node_id, node_name, node_link, node_flow):
        self.node_id = node_id  # E.g openflow:1
        self.node_name = node_name  # E.g s1
        self.node_link = node_link  # json {src-name : s1, src-port : 1, dest-name : s3, dest-port : 2}
        self.node_flow = node_flow

@auto_str
class Host():
    def __init__(self, node_id, node_name, node_mac, node_ip, node_link):
        self.node_id = node_id  # E.g host:00:00:00:00:00:01
        self.node_name = node_name  # E.g h1
        self.node_mac = node_mac  # E.g 00:00:00:00:00:01
        self.node_ip = node_ip  # E.g 10.0.0.1
        self.node_link = node_link  # json {src-name : h1, src-port : None, dest-name : s3, dest-port : 2} = Link

@auto_str
class Link():
    def __init__(self, src_name, src_port, dst_name, dst_port):
        self.src_name = src_name
        self.src_port = src_port
        self.dst_name = dst_name
        self.dst_port = dst_port

@auto_str
class Flow():
    def __init__(self, flow_id, table_id, switch_id, inport, outport, src_mac, dst_mac):
        self.flow_id = flow_id
        self.table_id = table_id
        self.switch_id = switch_id
        self.inport = inport
        self.outport = outport
        self.src_mac = src_mac
        self.dst_mac = dst_mac

    def json_format(self, is_private):
        if is_private == False:
            json_flow = '''
            {
                "flow-node-inventory:flow": [
                {
                    "id": "%s",
                    "priority": 2,
                    "table_id": %s,
                    "match": {
                        "in-port": "%s"
                    },
                    "instructions": {
                        "instruction": [
                            {
                                "order": 0,
                                "apply-actions": {
                                    "action": [
                                        {
                                            "order": 0,
                                            "output-action": {
                                                "max-length": 65535,
                                                "output-node-connector": "%s"
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    },
                    "idle-timeout": 0
                }
                ]
            }
            '''
            json_flow = json_flow % (str(self.flow_id), str(self.table_id), str(self.inport), str(self.outport))
        else:
            json_flow = '''
            {
                "flow-node-inventory:flow": [
                {
                    "id": "%s",
                    "priority": 2,
                    "table_id": %s,
                    "match": {
                        "in-port": "%s",
                        "ethernet-match": {
                            "ethernet-source": {
                                "address": "%s"
                            },
                            "ethernet-destination": {
                                "address": "%s"
                            }
                        }
                    },
                    "instructions": {
                        "instruction": [
                            {
                                "order": 0,
                                "apply-actions": {
                                    "action": [
                                        {
                                            "order": 0,
                                            "output-action": {
                                                "max-length": 65535,
                                                "output-node-connector": "%s"
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    },
                    "idle-timeout": 0
                }
                ]
            }
            '''
            json_flow = json_flow % (str(self.flow_id), str(self.table_id), str(self.inport), self.src_mac, self.dst_mac, str(self.outport))
        return json_flow