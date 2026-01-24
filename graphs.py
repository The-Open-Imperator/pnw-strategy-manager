from utils import Sphere

space = 75
left = -500
right = 500

def make_node_label(nation: dict) -> str:
    return f"{nation['nation_name']} | 🏗️ {nation['num_cities']} | s:{nation['score']} \n 💂 {nation['soldiers']} | ⚙ {nation['tanks']} | ✈ {nation['aircraft']} | 🚢 {nation['ships']}"

def make_edge_label(war: dict) -> str:
    return f"a:{war['att_resistance']} | {war['turns_left']} | d:{war['def_resistance']}"

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
    def __init__(self, wars, nations):
        self.Nedges = 0
        self.Nnodes = 0
        numN = len(nations)
        numE = len(wars)
        self.nodes = list()
        self.edges = list()
        self.add_from_nations_wars(wars, nations)

    
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


    @staticmethod
    def count_sphere_and_enemies(nations) -> (int, int):
        nS = 0
        nE = 0
        for n in nations:
            if n.group == Sphere.ALLIANCE or n.group == Sphere.SPHERE:
                nS += 1
            else:
                nE += 1
        return (nS, nE)

    @staticmethod    
    def get_r(ID: int, Rvertex: dict) -> int:
        if Rvertex.get(ID) != None:   # Node ID is an rvertex
            return ID
        
        for nodeID, r in Rvertex.items(): # Search for ID in all Rvertex vertecies lists
            for v in r['vertecies']:
                if v.id == ID:
                    return nodeID
        print(f"Failed to find Node {nodeID} in Rvertex lists! \n")

    def kruskal_make_MST_subgraphs(self) -> dict:
        Rvertex = dict()
        for n in self.nodes:
            Rvertex[n.id] = {'vertecies': [n], 'num': 1}

        for e in self.edges:
            v1 = Graph.get_r(e.source, Rvertex)
            v2 = Graph.get_r(e.target, Rvertex)

            if v1 != v2: # Acyclic => smaller rvertex joins bigger
                if (Rvertex[v1]['num'] >= Rvertex[v2]['num']): # v2 smaller => v2 joins v1
                    Rvertex[v1]['vertecies'] += Rvertex[v2]['vertecies']
                    Rvertex[v1]['num'] += Rvertex[v2]['num']
                    Rvertex.pop(v2)
                else:                            # v1 smaller => v1 joins v2
                    Rvertex[v2]['vertecies'] += Rvertex[v1]['vertecies']
                    Rvertex[v2]['num'] += Rvertex[v1]['num']
                    Rvertex.pop(v1)

        return Rvertex
    
    def generate_layout(self):
        Rvertex = self.kruskal_make_MST_subgraphs()

        nodesLeft = 0
        nodesRight = 0
        for r, subgraph in Rvertex.items():
            nS, nE = Graph.count_sphere_and_enemies(subgraph['vertecies'])

            # calculate padding between nS nE nations 
            # s.t. the subgraphs always align on the bottom most element
            if nS > nE:
                nodesRight += (nS - nE)
            elif (nS < nE):
                nodesLeft += (nE - nS)

            # set postions
            for n in subgraph['vertecies']:
                if n.group == Sphere.ALLIANCE or n.group == Sphere.SPHERE:
                    x = left
                    y = nodesLeft
                    nodesLeft += 1
                else:
                    x = right
                    y = nodesRight
                    nodesRight += 1

                n.position = {'x': x, 'y': y*space}
 
            # padding for the next subgraph
            nodesLeft += 1
            nodesRight += 1


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
