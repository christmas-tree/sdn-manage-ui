import requests
from requests.auth import HTTPBasicAuth
import json
from urllib.parse import urljoin
from server.config import ODL_CREDS, BASE_URL

class ODLRequest:

    @staticmethod
    def _getParams(url):
        headers = {'Content-Type': 'application/json'}
        auth = HTTPBasicAuth(
            ODL_CREDS['username'], ODL_CREDS['password'])
        url = urljoin(BASE_URL, url)
        return url, headers, auth

    @staticmethod
    def _processResp(resp):
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def get(_url):
        url, headers, auth = ODLRequest._getParams(_url)
        resp = requests.get(url, headers=headers, auth=auth)
        return ODLRequest._processResp(resp)

    @staticmethod
    def put(_url, dict_obj):
        url, headers, auth = ODLRequest._getParams(_url)
        resp = requests.put(url, json.dumps(dict_obj), headers=headers, auth=auth)
        return ODLRequest._processResp(resp)

    @staticmethod
    def delete(_url):
        url, headers, auth = ODLRequest._getParams(_url)
        resp = requests.delete(url, headers=headers, auth=auth)
        return ODLRequest._processResp(resp)


def dijkstra(graph, src, dst, visited=[], distances={}, predecessors={}):
    """ Tinh toan duong di nho nhat tu src toi dest
    """
    # kiem tra ngoai le
    if src not in graph:
        raise TypeError('The root of the shortest path tree cannot be found')
    if dst not in graph:
        raise TypeError('The target of the shortest path cannot be found')
    if src == dst:  # base case cho ham de qui
        path = []
        pred = dst
        while pred != None:
            path.append(pred)
            pred = predecessors.get(pred, None)
        return tuple(reversed(path))

    else:
        if not visited:  # this sets the source destination to 0 once because visited list
            distances[src] = 0
        # tham cac hang xom cua node
        for neighbor in graph[src]:
            if neighbor not in visited:  # kiem tra duong di tot hon voi cac not chua duoc tham
                # khoi tao khoang cach moi bang gia tri cua quang duong trc do + gia tri khoang cach toi node moi
                new_distance = distances[src] + graph[src][neighbor]
                # neu gia tri moi nho hon khoang cach toi hang xom thi chon duong di moi( hoac la vo cung neu cac node khong lien ke)
                if new_distance < distances.get(neighbor, float('inf')):
                    # thiet lap cac tham so moi
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = src
        # danh dau la da tham
        visited.append(src)
        # de quy toi node chua tham va khoang cach la ngan nhat
        unvisited = {}
        for k in graph:
            if k not in visited:
                # khoi tao khoang cach cho cac node chua tham
                unvisited[k] = distances.get(k, float('inf'))
        x = 0
        # chon node co khoang cach nho nhat
        x = min(unvisited, key=unvisited.get)
        # chay ham thuat toan dijkstra de qui
        return dijkstra(graph, x, dst, visited, distances, predecessors)


def dijkstraRouteHelperFunction(links, list_switch, list_host, src, dst):
    graphDic = {}  # empty dictionary

    for node in list_switch:  # make switch dictionary without links
        graphDic[node.node_id] = {}
    for node in list_host:
        graphDic[node.node_id] = {}
    for edge in links:  # adds each link to each switch
        graphDic[edge.src_id][edge.dst_id] = 1
        graphDic[edge.dst_id][edge.src_id] = 1

    path = dijkstra(graphDic, src, dst, visited=[],
                    distances={}, predecessors={})
    return path


def customRouteHelperFunction(links, switchs, hosts, src, dst, selected_switchs):
    graphDic = {}  # empty dictionary
    path = []
    for node in switchs:  # make switch dictionary without links
        graphDic[node.node_id] = {}
    for node in hosts:
        graphDic[node.node_id] = {}
    for edge in links:  # adds each link to each switch
        graphDic[edge.src_id][edge.dest_id] = 1
        graphDic[edge.dest_id][edge.src_id] = 1
    tmp_switchs = None
    for switch in selected_switchs:
        if(switch in path):
            continue
        tmp_path = dijkstra(graphDic, src, switch, visited=[],
                            distances={}, predecessors={})
        for point in tmp_path:
            if (point == tmp_switchs):
                continue
            path.append(point)
        src = switch
        tmp_switchs = switch
    tmp_path = dijkstra(graphDic, src, dst, visited=[],
                        distances={}, predecessors={})
    for point in tmp_path:
        if (point == tmp_switchs):
            continue
        path.append(point)
    return path
