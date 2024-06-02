from tkinter import *
from tkinter import ttk

from annealing_window import Annealing_Window
from neighbour_window import Neighbor_Window
from window import *
from swarm_window import *
from body import threads, stop_events
from ant_window import *



def on_exit():

    for event in stop_events:
        event.set()
    print(stop_events)
    root.quit()


# Создаётся окно пользователя
root = Tk()
root.title("Program")
root.geometry('1050x670')
root.protocol('WM_DELETE_WINDOW', on_exit)

# Зададим стиль для вкладок
style = ttk.Style()
style.theme_use('vista')
style.configure('TNotebook', background='white')
style.configure('TNotebook.Tab', foreground='black',  background="gray")
style.map('TNotebook.Tab', foreground=[('selected', 'black')], background=[('selected', "#d1dbe0")])

# Вкладки
ntb = ttk.Notebook(root, style='TNotebook')
ntb.pack(fill='both', expand=True)

# Генетический алгоритм
'''frame_genetic = Frame(ntb, bg="#d1dbe0")
ntb.add(frame_genetic, text="Генетический алгоритм")
Genetic_Window(frame_genetic)


# Роевой алгоритм
frame_swarm = Frame(ntb, bg="#d1dbe0")
ntb.add(frame_swarm, text="Алгоритм роя частиц")
Swarm_Window(frame_swarm)'''


# Метод отжига
frame_annealing = Frame(ntb, bg="#B3E5FC")
ntb.add(frame_annealing, text="Метод отжига")
Annealing_Window(frame_annealing)
# Метод ближайшего соседа
frame_neighbor = Frame(ntb, bg="#B3E5FC")
ntb.add(frame_neighbor, text="Метод ближайшего соседа")
Neighbor_Window(frame_neighbor)

# Муравьиный алгоритм
frame_ant = Frame(ntb, bg="#B3E5FC")
ntb.add(frame_ant, text="Муравьиный алгоритм")
Ant_Window(frame_ant)

root.mainloop()
root.update()
print("Tkinter finished")

# Дожидаемся закрытия потоков
for thread in threads:
    thread.join()
print(threads)
