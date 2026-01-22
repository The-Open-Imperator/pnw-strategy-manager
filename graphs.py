space = 75

def make_node_label(nation: dict) -> str:
    return f"{nation['nation_name']} | c:{nation['num_cities']} | s:{nation['score']} \n s:{nation['soldiers']} | t:{nation['tanks']} | a:{nation['aircraft']} | s:{nation['ships']}"

def make_edge_label(war: dict) -> str:
    return f"a:{war['att_resistance']} | {war['turns_left']} | d:{war['def_resistance']}"


class Sphere():
    ALLIANCE = 'alliance'
    SPHERE = 'sphere'
    ENEMY = 'enemy'
    UNALLIED = 'unallied'
    FALLBACK = 'fallback'

    yourAlliance = "4221"
    sphereList = ["3339", "12480", "11009", "7484", "13295"]

    @staticmethod
    def map_allianceID_to_sphere(ID: str):
        if ID == '0':
            return Sphere.UNALLIED
        if ID == Sphere.yourAlliance:
            return Sphere.ALLIANCE
        if ID in Sphere.sphereList:
            return Sphere.SPHERE
        return Sphere.ENEMY

    @staticmethod
    def map_alliance_to_sphere(alliance: dict):
        if alliance == None:
            return Sphere.UNALLIED
        return Sphere.map_allianceID_to_sphere(alliance['id'])

    @staticmethod
    def get(alliance):
        if type(alliance) == str:
            return map_allianceID_to_sphere(alliance)
        if type(alliance) == dict:
            return map_alliance_to_sphere(alliance)


class Edge:
    def __init__(self, source: int, target: int, label: str, group: str):
        self.source = source
        self.target = target
        self.label = label
        self.group = group

    def to_dict(self):
        d = dict()
        d['data'] = {'source': self.source, 'target': self.target, 'label': self.label}
        d['data']['group'] = self.group
        d['type'] = 'edge'

class Node:
    def __init__(self, ID: int, label: str, group: str):
        self.id = id
        self.label = label
        self.group = group

    def to_dict(self):
        d = dict()
        d['data'] = {'id': self.id, 'label': self.label}
        d['data']['group'] = self.group
        d['type'] = 'node'

        return d

class Graph:
    def __init__(self, *args):
        self.Nedges = 0
        self.Nnodes = 0
        if len(args) == 2:
            numN = len(args[0])
            numE = len(args[1])
            self.nodes = [Node]* numN
            self.edges = [Edge]* numE
            self.add_from_nations_wars(args[0], args[1])
        else:
            self.nodes = list()
            self.edges = list()
    
    def add_from_nations_wars(self, nations, wars):
        for n in nations:
            self.add_node(int(n['id']), make_node_label(n), Sphere.get(n.get('alliance')))
        for w in wars:
            l = make_edge_label(w)
            s = Sphere.get(w['att_alliance'])
            self.add_edge(int(w['att_id']), int(w['def_id']), l, s)

    def add_node(self, ID, label, group):
        self.nodes.append(Node(ID, label, group))
        self.Nnodes += 1

    def add_edge(self, source, target, label, group):
        self.edges.append(Edge( source, target, label, group))
        self.Nedges += 1

    def generate_layout(self):
        NnodeLeftUp = 0
        NnodeLeftDown = 0
        NnodeRightUp = 0
        NnodeRightDown = 0

        for n in self.nodes:
            if n['type'] == 'edge':   # Check if object is a node
                continue

            g = n['data']['group'] 
            if g == Sphere.ALLIANCE or g == Sphere.SPHERE:
                x = left
                y = NnodeLeftUp
                NnodeLeftUp += 1
            else:
                x = right
                y = NnodeRightUp
                NnodeRightUp += 1

            n['position'] = {'x': x, 'y': y*space}
        return nodes


    def get_all(self):
        n = list()
        for i in self.nodes:
            n.append(i.to_dict())
        for i in self.edges:
            n.append(i.to_dict())
        
        return n
