import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.nodes = None
        self.edges = None

    def build_weighted_graph(self):
        self.G.clear()

        geni = DAO.read_gene()
        interazioni = DAO.read_interazione()

        self.id_map = {}
        for g in geni:
            self.id_map[g.id] = g.cromosoma

        pesi_archi = {}

        cromosomi_unici = set(self.id_map.values())
        self.G.add_nodes_from(cromosomi_unici)

        for i in interazioni:
            if i.id_gene1 in self.id_map and i.id_gene2 in self.id_map:
                c1 = self.id_map[i.id_gene1]
                c2 = self.id_map[i.id_gene2]

                if c1!=c2:
                    n1, n2 = sorted((c1, c2))
                    key = n1, n2
                    if key not in pesi_archi:
                        pesi_archi[key] = 0
                    pesi_archi[key] += float(i.correlazione)

        for (c1,c2), weight in pesi_archi.items():
            self.G.add_edge(c1, c2, weight=weight)

    def get_min_max_weights(self):
        all_weights = list(nx.get_edge_attributes(self.G, 'weight').values())
        return min(all_weights), max(all_weights)

    def count_edges(self, soglia):
        self.massimi = 0
        self.minimi = 0

        for u, v, data in self.G.edges(data=True):
            peso = data['weight']
            if peso > soglia:
                self.massimi += 1
            elif peso < soglia:
                self.minimi += 1
        return self.massimi, self.minimi












