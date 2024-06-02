import tkinter as tk
import networkx as nx
from networkx import graph
from networkx import Graph


class GraphGUI:
  def __init__(self):
    self.root = tk.Tk()
    self.root.geometry("800x600")

    self.graph = Graph()

    # Окно "Рисование графа"
    self.draw_window = tk.Toplevel(self.root)
    self.draw_window.geometry("600x400")
    self.draw_canvas = tk.Canvas(self.draw_window, width=600, height=400)
    self.draw_canvas.pack()

    # Панель инструментов
    self.toolbar = tk.Frame(self.draw_window)
    self.toolbar.pack(side=tk.TOP)

    # Кнопки для рисования вершин и ребер
    self.add_node_button = tk.Button(self.toolbar, text="Добавить вершину", command=self.add_node)
    self.add_edge_button = tk.Button(self.toolbar, text="Добавить ребро", command=self.add_edge)

    # Кнопки для удаления вершин и ребер
    self.delete_node_button = tk.Button(self.toolbar, text="Удалить вершину", command=self.delete_node)
    self.delete_edge_button = tk.Button(self.toolbar, text="Удалить ребро", command=self.delete_edge)

    # Панель информации
    self.info_panel = tk.Frame(self.draw_window)
    self.info_panel.pack(side=tk.BOTTOM)

    # Окно "Поиск кратчайшего пути"
    self.path_window = tk.Toplevel(self.root)
    self.path_window.geometry("300x200")

    # Поле для ввода списка вершин
    self.nodes_label = tk.Label(self.path_window, text="Список вершин для посещения:")
    self.nodes_entry = tk.Entry(self.path_window)

    # Кнопка "Найти путь"
    self.find_path_button = tk.Button(self.path_window, text="Найти путь", command=self.find_path)

    # Поле с длиной кратчайшего пути
    self.path_length_label = tk.Label(self.path_window, text="Длина пути:")
    self.path_length_entry = tk.Entry(self.path_window)

    # Поле с отображением найденного пути
    self.path_label = tk.Label(self.path_window, text="Найденный путь:")
    self.path_text = tk.Text(self.path_window, height=5)

    # Запуск интерфейса
    self.root.mainloop()

  def add_node(self):
    # Получить координаты мыши
    x, y = self.draw_canvas.winfo_pointerx(), self.draw_canvas.winfo_pointery()

    # Создать новую вершину
    node = self.graph.add_node(x, y)

    #Отрисовать новую вершину на холсте
    self.draw_canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red")

      # Обновить информацию о выбранной вершине
    self.info_panel.update_node_info(node)

  def add_edge(self):
    x1, y1 = self.draw_canvas.winfo_pointerx(), self.draw_canvas.winfo_pointery()

    # Найти ближайшую вершину к первой координате
    start_node = self.graph.find_closest_node(x1, y1)
    x2, y2 = self.draw_canvas.winfo_pointerx(), self.draw_canvas.winfo_pointery()
    # Найти ближайшую вершину ко второй координате
    end_node = self.graph.find_closest_node(x2, y2)

    # Создать новое ребро
    self.graph.add_edge(start_node, end_node)

    # Отрисовать новое ребро на холсте
    self.draw_canvas.create_line(start_node.x, start_node.y, end_node.x, end_node.y)

    # Обновить информацию о выбранном ребре
    self.info_panel.update_edge_info(start_node, end_node)

  def delete_node(self):
    node = self.info_panel.get_selected_node()

    # Удалить вершину из графа
    self.graph.delete_node(node)

    # Удалить отображение вершины с холста
    self.draw_canvas.delete(node.id)

    # Очистить информацию о выбранной вершине
    self.info_panel.clear_node_info()

  def delete_edge(self):
    start_node, end_node = self.info_panel.get_selected_edge()

    # Удалить ребро из графа
    self.graph.delete_edge(start_node, end_node)

    # Удалить отображение ребра с холста
    # Очистить информацию о выбранном ребре
    self.info_panel.clear_edge_info()

  def find_path(self):
    # Получить список вершин из поля ввода
    nodes_str = self.nodes_entry.get()
    nodes = nodes_str.split(",")

    # Преобразовать список строк в список объектов Node
    nodes = [self.graph.nodes[node_name] for node_name in nodes]

    # Проверить, является ли граф деревом
    #if not nx.is_tree(self.graph.to_networkx()):
      #print("1")
if __name__ == "__main__":
  gui = GraphGUI()