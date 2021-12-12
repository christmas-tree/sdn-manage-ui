import json
from server.modules.utils import ODLRequest
from server.models import Switch, Host, Link, Flow
from server.config import CONF_URL, OPERATION_URL


def get_topo():
    list_switch = []
    list_host = []
    data = ODLRequest.get(OPERATION_URL + '/network-topology:network-topology')

    with open("sdntopo.json", "w") as outfile:
        json.dump(data, outfile, indent=4)

    topology = data['network-topology']['topology']
    if 'node' not in topology[0] or 'link' not in topology[0]:
        raise Exception(f"ERROR: Network topology is unavailable.")

    nodes = topology[0]['node']
    list_link = topology[0]['link']
    for node in nodes:
        node_id = node['node-id']
        if "openflow" in node_id:
            switch = set_switch(node)
            list_switch.append(switch)
        else:
            host = set_host(node)
            list_host.append(host)

    list_switch.sort(key=lambda s: s.node_name)
    list_host.sort(key=lambda h: h.node_name)

    list_links = set_link(list_link, list_host, list_switch)
    return list_switch, list_host


def set_switch(node):
    node_id = node['node-id']
    node_name = 's' + node_id.split(":")[-1]
    node_link = list()
    node_flow = list()
    return Switch(node_id, node_name, node_link, node_flow)


def set_host(node):
    host_tracker_attachment_points = node['host-tracker-service:attachment-points'][0]
    host_tracker_addresses = node['host-tracker-service:addresses'][0]
    node_ip = host_tracker_addresses['ip']
    node_id = node['node-id']
    # Chi dung neu mininet co --mac de tao Mac don gian 00:00:00:00:00:01
    node_name = 'h' + str(int(node_ip.split(".")[-1]))
    node_mac = host_tracker_addresses['mac']
    node_link = list()
    return Host(node_id, node_name, node_mac, node_ip, node_link)


def set_link(links, list_host, list_switch):
    links.sort(key=lambda l: l['link-id'])
    list_link = []
    for link in links:
        node_link = Link(None, None, None, None)
        src = link['source']['source-node']
        if src.startswith('host'):
            for idx, h in enumerate(list_host):
                if h.node_id == src:
                    src_host = h
                    break
            src_index = idx
            node_link.src_id = src_host.node_id
            node_link.src_name = src_host.node_name
        else:
            for idx, s in enumerate(list_switch):
                if s.node_id == src:
                    src_switch = s
                    break
            src_index = idx
            node_link.src_id = src_switch.node_id
            node_link.src_name = src_switch.node_name
            node_link.src_port = int(link['source']['source-tp'][-1])

        dst = link['destination']['dest-node']
        if dst.startswith('host'):
            for idx, h in enumerate(list_host):
                if h.node_id == dst:
                    dst_host = h
                    break
            node_link.dst_id = dst_host.node_id
            node_link.dst_name = dst_host.node_name
        else:
            for idx, s in enumerate(list_switch):
                if s.node_id == dst:
                    dst_switch = s
                    break
            # dst_index = idx
            node_link.dst_id = dst_switch.node_id
            node_link.dst_name = dst_switch.node_name
            node_link.dst_port = int(link['destination']['dest-tp'][-1])
        if src.startswith('host'):
            list_host[src_index].node_link.append(node_link)
        else:
            list_switch[src_index].node_link.append(node_link)
        list_link.append(node_link)
    return list_link


def get_flow(switch):
    url = OPERATION_URL + "/opendaylight-inventory:nodes/node/" + \
        switch.node_id + "/flow-node-inventory:table/0/"
    data = ODLRequest.get(url)
    list_flow = data['flow-node-inventory:table'][0]['flow']
    for f in list_flow:
        flow_id = f['id']
        match = f['match']
        port_in = match['in-port']
        action = f['instructions']['instruction'][0]['apply-actions']['action'][0]
        output_action = action['output-action']
        port_out = output_action['output-node-connector']

        src_mac = match['ethernet-match']['ethernet-source']['address']
        dst_mac = match['ethernet-match']['ethernet-destination']['address']
        flow = Flow(flow_id, 0, switch.node_id,
                    port_in, port_out, src_mac, dst_mac)
        flow = Flow(flow_id, 0, switch.node_id,
                    port_in, port_out, None, None)
        switch.node_flow.append(flow)
    switch.node_flow = list()


def get_all_flow(list_switch):
    for switch in list_switch:
        get_flow(switch)


def change_flow_id(switch):
    url = OPERATION_URL + "/opendaylight-inventory:nodes/node/" + \
        switch.node_id + "/flow-node-inventory:table/0/"
    data = ODLRequest.get(url)
    list_flow = data['flow-node-inventory:table'][0]['flow']
    for idx, f in enumerate(list_flow):
        body = {"flow-node-inventory:flow": []}
        f['id'] = str(idx)
        body["flow-node-inventory:flow"].append(f)
        url = CONF_URL + "/opendaylight-inventory:nodes/node/" + switch.node_id + \
            "/flow-node-inventory:table/0/flow/" + f['id']
        body = json.dumps(body)
        ODLRequest.put(url, body)


def delete_flow(switch):
    change_flow_id(switch)
    # print(
        # f"*** {YELLOW}Processing:{RESET} Deleting flow table of switch {switch.node_name} ***")
    url = OPERATION_URL + "/opendaylight-inventory:nodes/node/" + switch.node_id + "/table/0"
    data = ODLRequest.get(url)

    list_flow = data["flow-node-inventory:table"][0]['flow']
    for f in list_flow:
        url = CONF_URL + "/opendaylight-inventory:nodes/node/" + switch.node_id + \
            "/flow-node-inventory:table/0/flow/" + f['id']
        ODLRequest.delete(url)


def delete_all_flow(list_switch):
    for s in list_switch:
        delete_flow(s)
