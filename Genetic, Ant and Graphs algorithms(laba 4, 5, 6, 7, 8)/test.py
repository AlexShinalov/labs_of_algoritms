import networkx as nx
import heapq

def dijkstra(G, source, target):

    #if not nx.is_tree(G):
        #raise nx.NetworkXError("Not a tree")


    distance = {vertex: float('inf') for vertex in G.nodes()}
    distance[source] = 0

    pq = [(0, source)]

    while pq:
        current_dist, current_vertex = heapq.heappop(pq)
        neighbors = [vertex for vertex in G.neighbors(current_vertex)]

        if current_vertex == target:
            return nx.shortest_path(G, source, target)

        for neighbor in neighbors:
            if neighbor in distance:
                distance_to_neighbor = current_dist + 1

                if distance_to_neighbor < distance[neighbor]:
                    distance[neighbor] = distance_to_neighbor
                    print(distance)
                    heapq.heappush(pq, (distance_to_neighbor, neighbor))
                    print(pq)





Gr = nx.Graph()
Gr.add_edges_from([
  ('1', '2'),
  ('1', '3'),
  ('2', '4'),
  ('3', '4'),
  ('3', '5'),
])

path = dijkstra(Gr, '1', '4')

print(f"Кратчайший путь: {path}")