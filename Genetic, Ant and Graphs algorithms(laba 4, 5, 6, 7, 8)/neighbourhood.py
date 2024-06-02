import networkx as nx
class Neighbor:
    """ Метод ближайшего соседа """
    def __init__(self, graphPaths):
        self.graphPaths = graphPaths  # веса путей заданных в графе
        self.vertexes = len(graphPaths) + 1  # кол-во вершин
        self.best_path = []  # лучший маршрут
        self.best_score = float('inf')  # наименьшая длина цикла


    def converter_to_nx(self, graph_list):

        graph_list = self.graphPaths
        G = nx.DiGraph()
        k = 1
        for g in graph_list:
            for j in range(len(g)):
                if (((g[j]).split('/'))[0]) != 'no':
                    G.add_edge(k, j + 1 + k, weight=int(((g[j]).split('/'))[0]))
                else:G.add_edge(k, j + 1 + k, weight='no')
            k += 1

        c = 1
        for g in graph_list:
            for j in range(len(g)):
                if (((g[j]).split('/'))[1]) != 'no':
                    G.add_edge(j + 1 + c, c, weight=int(((g[j]).split('/'))[1]))
                else:
                    G.add_edge(j + 1 + c, c, weight='no')
            c += 1

        return G

    def find_best_way(self) -> None:

        graph_list=self.graphPaths
        G = self.converter_to_nx(graph_list)
        for u, v, data in G.edges(data=True):print(f"({u}, {v}) - weight: {data['weight']}")

        for vert in range(len(G)):
            path_len=0
            current=vert+1
            print(current)
            visited = []
            visited.append(current)
            for i in range(self.vertexes):
                while len(visited)< len(G):
                    near_n=None
                    min_dist=float('inf')
                    for n in G.neighbors(current):
                        if n not in visited:
                            if G[current][n]['weight'] != 'no':
                                distance=G[current][n]['weight']
                                if distance < min_dist:
                                    min_dist =distance
                                    near_n = n
                            else: distance =float('inf')
                    if near_n is not None:
                        visited.append(near_n)
                        path_len+=min_dist
                        current = near_n
                    if len(visited)==len(G):
                        if G[current][1]['weight']!='no':
                            path_len+=G[current][1]['weight']
                        else: path_len =float('inf')

                if self.best_score > path_len:
                    self.best_score = path_len
                    self.best_path=[]
                    for b in visited:
                        self.best_path.append(b)

        plus_path=[i-1 for i in self.best_path]
        self.best_path=plus_path



def neighborhood_algorithm(graphPaths):
    if graphPaths == [] or graphPaths == [[]]:
        return [], None
    else:
        a = Neighbor(graphPaths=graphPaths)
        a.find_best_way()
        return a.best_path, a.best_score

#print(neighborhood_algorithm([['3/3', 'no/no', 'no/no', '1/3', 'no/3'], ['8/3', 'no/no', 'no/no', '3/3'], ['1/8', 'no/no', '1/3'], ['1/3', 'no/5'], ['no/4']]))