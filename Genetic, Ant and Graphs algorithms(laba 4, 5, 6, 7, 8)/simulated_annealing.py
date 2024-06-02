import math
import random
import copy
import networkx as nx


class SimulatedAnn:
    """ Класс реализующий метод отжига """
    def __init__(self, graphPaths, start_T, stop_T, coolingRatio, numberGeneration):
        self.graphPaths = graphPaths  # веса путей заданных в графе
        self.vertexes = len(graphPaths) + 1  # кол-во вершин
        self.coolingRatio = coolingRatio  # коэффициент охлаждения
        self.start_T = start_T  # начальная температура
        self.stop_T = stop_T  # конечная температура
        self.numberGeneration = numberGeneration  # количество попыток отыскать новый маршрут
        # задаём начальные значения
        self.best_score=float('inf')
        self.best_cost = []

    def random_way(self,graph):
        route = []
        nodes = list(graph.nodes())
        start_node = random.choice(nodes)
        route.append(start_node)



        # Пока не все узлы добавлены в маршрут
        while len(route) < len(nodes):
            last_node = route[-1]
            next_nodes = []

            # Проверяем соседей последнего узла
            for neighbor in graph.neighbors(last_node):
                if graph.has_edge(last_node, neighbor) and graph[last_node][neighbor]['weight'] != 'no' and neighbor not in route:
                    next_nodes.append(neighbor)

            if next_nodes:
                next_node = random.choice(next_nodes)
                route.append(next_node)
            else:
                remaining_nodes = set(nodes) - set(route)
                start_node = random.choice(list(remaining_nodes))
                route.append(start_node)

        return route

    def solution_count(self, G, solution):
        score = 0
        for i in range(len(solution) - 1):
            if G.has_edge(solution[i], solution[i + 1]) and G[solution[i]][solution[i + 1]]['weight'] != 'no':
                score += int(G[solution[i]][solution[i + 1]]['weight'])
            else:
                return float('inf')  # Возвращаем бесконечность, если встречается ребро с весом 'no'

        # Проверяем последнее ребро
        if G.has_edge(solution[-1], solution[0]) and G[solution[-1]][solution[0]]['weight'] != 'no':
            score += int(G[solution[-1]][solution[0]]['weight'])
        else:
            return float('inf')  # Возвращаем бесконечность, если встречается ребро с весом 'no'

        return score

    def neighbour_solution(self, solution):
        neighbour=solution.copy()
        i, j =random.sample(range(len(solution)), 2)
        neighbour[i],neighbour[j]= neighbour[j], neighbour[i]
        return neighbour

    def two_opt(self, solution):
        new_solution = solution.copy()
        i, j = random.sample(range(len(solution)), 2)
        if i > j:
            i, j = j, i
        new_solution[i:j] = reversed(new_solution[i:j])
        return new_solution
    def ac_pr(self, old_cost, new_cost, temp):
        if old_cost is None and new_cost is None:
            return 0.0
        elif old_cost is None:
            return 1.0
        elif new_cost is None:
            return 0.0
        elif new_cost < old_cost:
            return 1.0
        if temp==0:
            temp=1
        return math.exp((old_cost - new_cost) / temp)

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

    def find_best_way(self) :
        graph_list = self.graphPaths
        g=self.converter_to_nx(graph_list)

        rand_sol=self.random_way(g)
        current_solution = [int(i) for i in rand_sol]
        current_cost = self.solution_count(g, current_solution)

        while current_cost == float('inf'):
            rand_sol = self.random_way(g)
            current_solution=[int(i) for i in rand_sol]
            current_cost = self.solution_count(g, current_solution)

        self.best_cost = current_solution
        self.best_score = current_cost
        print(self.best_score, self.best_cost)

        temperatures = self.start_T
        while temperatures > self.stop_T:

            for _ in range(self.numberGeneration):

                new_sol=self.neighbour_solution(current_solution)
                new_sol_int=[]
                for i in new_sol:
                    new_sol_int.append(int(i))

                new_cost=self.solution_count(g, new_sol_int)

                if self.ac_pr(current_cost, new_cost,temperatures) > random.random():
                    current_solution = new_sol
                    current_cost = new_cost

                if new_cost is None or self.best_score is None:
                    if new_cost is None:
                        new_cost = float('inf')

                if new_cost < self.best_score:
                    self.best_score = new_cost
                    self.best_cost = new_sol


                temperatures *= self.coolingRatio

        minus_sol=[]
        for i in self.best_cost:
            minus_sol.append(i-1)

        self.best_cost=minus_sol

def annealing_algorithm(start_T, stop_T, coolingRatio, numberGeneration, graphPaths):
    if graphPaths == [] or graphPaths == [[]]:
        return [], None
    else:
        a = SimulatedAnn(numberGeneration=int(numberGeneration),
                         coolingRatio=float(coolingRatio),
                         start_T=max(int(start_T), int(stop_T)), stop_T=min(int(start_T), int(stop_T)),
                         graphPaths=graphPaths)
        a.find_best_way()

        return a.best_cost, a.best_score


# Запускаем метод имитации отжига
#print(annealing_algorithm(100000, 1, 0.1, 1000, [['3/3', 'no/no', 'no/no', '1/3', 'no/3'], ['8/3', 'no/no', 'no/no', '3/3'], ['1/8', 'no/no', '1/3'], ['1/3', 'no/5'], ['no/4']]))


