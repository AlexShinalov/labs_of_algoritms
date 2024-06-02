import random
import networkx as nx



class Ant:
    def __init__(self, size_pop, numberGeneration, graphPaths, alpha, beta, rho):
        """ Класс реализующий муравьиный алгоритм """
        self.graphPaths = graphPaths  # веса путей заданных в графе
        self.vertexes = len(self.graphPaths) + 1  # количество вершин
        self.size_pop = size_pop  # популяция муравьёв
        self.numberGeneration = numberGeneration  # количество итераций
        self.alpha = alpha  # коэффициент важности феромонов при выборе пути
        self.beta = beta  # коэффициент значимости расстояния
        self.rho = rho  # скорость испарения феромонов
        self.generation_best_path, self.generation_best_score = [], []  # лучшие в своём поколении
        self.best_path, self.best_score = None, float('inf')

    def converter_to_nx(self, graph_list):

        graph_list = self.graphPaths
        G = nx.DiGraph()
        k = 1
        for g in graph_list:
            for j in range(len(g)):
                if (((g[j]).split('/'))[0]) != 'no':
                    G.add_edge(k, j + 1 + k, weight=int(((g[j]).split('/'))[0]))
                else:G.add_edge(k, j + 1 + k, weight=float('inf'))
            k += 1

        c = 1
        for g in graph_list:
            for j in range(len(g)):
                if (((g[j]).split('/'))[1]) != 'no':
                    G.add_edge(j + 1 + c, c, weight=int(((g[j]).split('/'))[1]))
                else:
                    G.add_edge(j + 1 + c, c, weight=float('inf'))
            c += 1

        return G

    def solution_count(self, G, solution):
        score = 0
        for i in range(len(solution) - 1):
            if G.has_edge(solution[i], solution[i + 1]) and G[solution[i]][solution[i + 1]]['weight'] != float('inf'):
                score += int(G[solution[i]][solution[i + 1]]['weight'])
            else:
                return float('inf')  # Возвращаем бесконечность, если встречается ребро с весом 'no'

        # Проверяем последнее ребро
        if G.has_edge(solution[-1], solution[0]) and G[solution[-1]][solution[0]]['weight'] != float('inf'):
            score += int(G[solution[-1]][solution[0]]['weight'])
        else:
            return float('inf')  # Возвращаем бесконечность, если встречается ребро с весом 'no'

        return score

    def find_best_way(self) -> None:
        beta=self.beta
        alpha=self.alpha
        best_score=self.best_score
        best_path=self.best_path
        G=self.converter_to_nx(self.graphPaths)
        pheromones = {(i, j): 1.0 for i, j in G.edges()}
        for _ in range(self.numberGeneration):
            ant_path=[]
            for _ in range(self.size_pop):
                current_city=random.choice(list(G.nodes()))
                path=[]
                path.append(current_city)
                while(len(path))<len(list(G.nodes)):
                    next_city=None
                    for neigbor in G.neighbors(current_city):
                        if neigbor not in path:
                            prob = (pheromones[current_city, neigbor] ** beta) /\
                                          sum((pheromones[current_city, neighbor] ** beta) * (
                                                      G[current_city][neighbor]['weight'] ** alpha) for neighbor in
                                              G.neighbors(current_city) if neighbor not in path)
                            if next_city is None or prob > random.random():
                                next_city = neigbor
                    current_city=next_city
                    path.append(next_city)
                ant_path.append(path)
            for edge in pheromones:
                pheromones[edge]*=self.rho
                for path in ant_path:
                    if edge in path:
                        pheromones[edge]+=1.0/len(path)
            print(path)
            current_score=self.solution_count(G, path)
            if current_score<best_score:
                best_score=current_score
                best_path=path

        self.best_score=best_score
        if best_path != None:
            self.best_path=[i-1 for i in best_path]




def ant_algorithm(size_pop, numberGeneration, alpha, beta, rho, graphPaths):
    if graphPaths == [] or graphPaths == [[]]:
        return [], None
    else:
        a = Ant(size_pop=int(size_pop),
                numberGeneration=int(numberGeneration),
                alpha=int(alpha), beta=int(beta), rho=float(rho),
                graphPaths=graphPaths)
        a.find_best_way()
        return a.best_path, a.best_score



# Проверка муравьиного алгоритма
print(ant_algorithm(50, 50, 1, 3, 0.5, [['3/3', 'no/no', 'no/no', '1/3', 'no/3'], ['8/3', 'no/no', 'no/no', '3/3'], ['1/8', 'no/no', '1/3'], ['1/3', 'no/5'], ['no/4']]))
