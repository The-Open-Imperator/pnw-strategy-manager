space = 75
left = -500
right = 500

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
            return Sphere.map_allianceID_to_sphere(alliance)
        if type(alliance) == dict:
            return Sphere.map_alliance_to_sphere(alliance)


class Edge:
    def __init__(self, source: int, target: int, label: str, group: str):
        self.source = source
        self.target = target
        self.label = label
        self.group = group

    def to_dict(self):
        d = dict()
        d['data'] = {'source': str(self.source), 'target': str(self.target), 'label': self.label}
        d['data']['group'] = self.group
        d['type'] = 'edge'

        return d

class Node:
    def __init__(self, ID: int, label: str, group: str):
        self.id = ID
        self.label = label
        self.group = group
        self.position = {'x': 0, 'y':0}

    def to_dict(self):
        d = dict()
        d['data'] = {'id': str(self.id), 'label': self.label, 'group': self.group}
        d['position'] = self.position
        d['type'] = 'node'

        return d

class Graph:
    def __init__(self, nations, wars):
        self.Nedges = 0
        self.Nnodes = 0
        numN = len(nations)
        numE = len(wars)
        self.nodes = list()
        self.edges = list()
        #self.nodes = [Node]* numN
        #self.edges = [Edge]* numE
        #self.add_from_nations_wars(nations, wars)

    
    def add_from_nations_wars(self, wars, nations):
        for ID, n in nations.items():
            self.add_node(int(ID), make_node_label(n), Sphere.get(n.get('alliance')))
        for w in wars:
            l = make_edge_label(w)
            s = Sphere.get(w['att_alliance_id'])
            self.add_edge(int(w['att_id']), int(w['def_id']), l, s)

    def add_node(self, ID, label, group):
        self.nodes.append(Node(ID, label, group))
        self.Nnodes += 1

    def add_edge(self, source, target, label, group):
        self.edges.append(Edge(source, target, label, group))
        self.Nedges += 1

    def generate_layout(self):
        NnodeLeftUp = 0
        NnodeLeftDown = 0
        NnodeRightUp = 0
        NnodeRightDown = 0

        for n in self.nodes:
            print(n.label)
            if n.group == Sphere.ALLIANCE or n.group == Sphere.SPHERE:
                x = left
                y = NnodeLeftUp
                NnodeLeftUp += 1
            else:
                x = right
                y = NnodeRightUp
                NnodeRightUp += 1

            n.position = {'x': x, 'y': y*space}

    def get_all(self):
        n = list()
        for i in self.nodes:
            n.append(i.to_dict())
        for i in self.edges:
            n.append(i.to_dict())
        
        return n



if __name__ == '__main__':
    wars = {}
    g = Graph('a', 'b')
    g.add_node(1, 'Node 1', 'sphere')
    print(g.nodes[0].group)
    g.add_node(2, 'Node 2', 'sphere')
    g.add_edge(1, 2, '1-2', 'sphere')
    print(g.get_all())
