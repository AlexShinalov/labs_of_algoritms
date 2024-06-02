import heapq
import tkinter as tk
import networkx as nx


class DjtreeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Djtree GUI")

        self.canvas = tk.Canvas(self.master, width=600, height=400, bg='white')
        self.canvas.pack()

        self.graph = nx.Graph()
        self.nodes = []
        self.node_labels = {}
        self.node_indexes = {} 
        self.edges = []
        self.selected_node = None
        self.start_node = None

        self.canvas.bind("<Button-1>", self.create_node)
        #self.canvas.bind("<B1-Motion>", self.move_node)
        self.canvas.bind("<Button-3>", self.start_connection)
        self.canvas.bind("<ButtonRelease-3>", self.end_connection)

        self.calculate_button = tk.Button(self.master, text="Calculate Path", command=self.calculate_path)
        self.calculate_button.pack()

        self.target_entry_label = tk.Label(self.master, text="Enter target nodes (separated by commas):")
        self.target_entry_label.pack()
        self.target_entry = tk.Entry(self.master)
        self.target_entry.pack()

        self.path_label = tk.Label(self.master, text="Path: ")
        self.path_label.pack()
        self.path_display = tk.Label(self.master, text="")
        self.path_display.pack()

    def create_node(self, event):
        x, y = event.x, event.y
        node = len(self.nodes)+1
        #print(len(self.nodes))
        node_oval = self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="blue")
        node_label = self.canvas.create_text(x, y, text=str(node), fill="white")
        self.nodes.append((node, (x, y)))
        print(self.nodes)
        self.node_labels[node_oval] = node_label
        self.node_indexes[node] = node
        #print(self.node_indexes[node])
        self.graph.add_node(node)
        #print(self.graph.nodes)

    """
    def move_node(self, event):
        if self.selected_node:
            x, y = event.x, event.y
            self.canvas.coords(self.selected_node[0], x - 15, y - 15, x + 15, y + 15)
            self.canvas.coords(self.node_labels[self.selected_node[0]], x, y)
"""
    def start_connection(self, event):
        x, y = event.x, event.y
        closest_node = self.find_closest_node(x, y)
        if closest_node:
            self.start_node = closest_node

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)

    def end_connection(self, event):
        x, y = event.x, event.y
        end_node = self.find_closest_node(x, y)
        #print(end_node)
        if self.start_node and end_node and self.start_node != end_node:
            # Проверяем, существует ли уже ребро между этими узлами
                line = self.canvas.create_line(*self.start_node[1], *end_node[1], fill="black")
                self.edges.append((line, self.start_node, end_node))
                self.graph.add_edge(self.start_node[0], end_node[0])
                #print(self.graph.nodes)
        self.start_node = None
        self.remove_edge((line, self.start_node, end_node))

    def find_closest_node(self, x, y):
        closest_dist = float("inf")
        closest_node = None

        for node in self.nodes:
            nx, ny = node[1]
            dist = ((x - nx) ** 2 + (y - ny) ** 2) ** 0.5
            if dist < closest_dist:
                closest_dist = dist
                closest_node = node
        return closest_node

    def calculate_path(self):
        target_nodes = self.target_entry.get().split(',')
        path=[1]
        target_nodes.append('1')
        c=1
        star_node=self.nodes[c-1][0]
        for i in target_nodes:
            star_node = self.nodes[c-1][0]
            first = self.dijkstra(self.graph, star_node, i)
            c=int(i)
            for i in range(1, len(first)):
                path.append(first[i])

        print(path)
        if path:
            #print(path)
            self.path_display.config(text="Path: " + " -> ".join(str(node) for node in path))
        else:
            self.path_display.config(text="No path found")

    def dijkstra(self, G, source, target):

        # if not nx.is_tree(G):
        # raise nx.NetworkXError("Not a tree")

        distance = {vertex: float('inf') for vertex in G.nodes()}
        distance[source] = 0

        pq = [(0, source)]

        while pq:
            current_dist, current_vertex = heapq.heappop(pq)
            neighbors = [vertex for vertex in G.neighbors(current_vertex)]

            if current_vertex == int(target):
                return nx.shortest_path(G, source, int(target))

            for neighbor in neighbors:
                if neighbor in distance:
                    distance_to_neighbor = current_dist + 1

                    if distance_to_neighbor < distance[neighbor]:
                        distance[neighbor] = distance_to_neighbor
                        print(distance)
                        heapq.heappush(pq, (distance_to_neighbor, neighbor))
                        print(pq)
        pass



def main():
    root = tk.Tk()
    app = DjtreeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
