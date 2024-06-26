from tkinter import ttk
import threading
from tkinter import *
import shutil
from show import ShowResult, ShowGraph
from all_functions import functions_arr
from swarm import swarm_algorithm
from simulated_annealing import annealing_algorithm
from neighbourhood import neighborhood_algorithm
from ant import  ant_algorithm
# Алгоритмы которые неявно вызываются в ClickButton
from main import *

# Массив всех потоков и их стоп-событий
threads = []
stop_events = []


class WidgetTemp:
    def __init__(self, root, main_title, img_title, table_title, algorithm):
        # Для каждого окна вызываем проверку на дурака (поток)
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.checkButtonState)
        stop_events.append(self.stop_event)
        threads.append(self.thread)

        # Какой алгоритм хотят вызвать
        self.algorithm = algorithm
        self.extremum_algorithms = ["genetic_algorithm", "swarm_algorithm"]
        self.graphs_algorithms = ["annealing_algorithm", "neighborhood_algorithm", "ant_algorithm"]

        # Фрейм в котором располагаются атрибуты ввода
        self.frame_input = Frame(root, bd=3, relief=GROOVE, background="#d1dbe0")
        frame_input_label = Label(self.frame_input, text=main_title, font=('Arial', 16), background="#d1dbe0")
        frame_input_label.pack(pady=10)
        self.frame_input.grid(column=0, row=0, rowspan=2, sticky='NSEW')
        # Фрейм в который выводиться любая графическая составляющая программы
        self.frame_img = LabelFrame(root, bd=3, relief=GROOVE, text=img_title, background="#d1dbe0")
        self.frame_img.grid(column=1, row=0, sticky='NSEW')
        # Фрейм в который выводиться таблицы
        self.frame_table = LabelFrame(root, bd=3, relief=GROOVE, text=table_title, background="#d1dbe0")
        self.frame_table.grid(column=1, row=1, sticky='NSEW')
        # Дополнительные мини-фреймы
        self.frame_btn = Frame(self.frame_img, background="#d1dbe0")
        self.frame_btn.pack(fill=BOTH, expand=1)
        self.frame_scroll = Frame(self.frame_table, background="#d1dbe0")
        self.frame_scroll.pack(fill=BOTH, expand=1)
        # Задание параметров для столбцов и строк
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=2)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        # Массив всех атрибутов ввода Spinbox и Combobox
        self.widgets_arr = []
        # Позволяем пользователю ввести точки графа
        if self.algorithm in self.graphs_algorithms:
            self.a = ShowGraph(frame_btn=self.frame_btn, frame_scroll=self.frame_scroll, frame_input=self.frame_input)

        # Запуск программы
        self.btn_start = ttk.Button(self.frame_input, text="Расчитать", command=self.clickButton, state=DISABLED)
        # Очистить старые значения
        self.btn_clean = ttk.Button(self.frame_input, text="Очистить", command=self.cleanButton, state=DISABLED)
        # Строчка в которую будет выводиться финальный ответ
        self.output_label = Label(self.frame_input, text="", background="#d1dbe0")

    def pack(self, **kwargs) -> None:
        """ Когда происходить упаковка body, пакуем и его внутренние виджеты """
        self.btn_start.pack(**kwargs)
        self.btn_clean.pack(**kwargs)
        self.output_label.pack(**kwargs)
        # Считываем массив атрибутов из *_window.py
        for child in self.frame_input.winfo_children():
            if isinstance(child, ttk.Spinbox) or isinstance(child, ttk.Combobox):
                self.widgets_arr.append(child)
        self.thread.start()

    def checkButtonState(self) -> None:
        """ Функция отвечающая за асинхронные вызовы """
        while not self.stop_event.wait(0.5):
            # Проверка, что Spinbox и Combobox не пустые
            try:
                current_input = sorted(len(widget.get()) for widget in self.widgets_arr)
                if current_input[-1] != 0:
                    self.btn_clean.configure(state=NORMAL)
                    if current_input[0] != 0:
                        self.btn_start.configure(state=NORMAL)
                    else:
                        self.btn_start.configure(state=DISABLED)
                else:
                    self.btn_clean.configure(state=DISABLED)
                    self.btn_start.configure(state=DISABLED)
            except IndexError:
                self.btn_clean.destroy()    # для методов, где нет ввода
                self.btn_start.configure(state=NORMAL)

    def cleanButton(self) -> None:
        """ По нажатию кнопки удаляем старые данные """
        for child in self.widgets_arr:
            child.set('')
        try:
            shutil.rmtree(self.algorithm[0])
        except OSError:
            pass

    def clickButton(self) -> None:
        """ По нажатию кнопки производятся расчёты """
        # def widget_value(name):
        #     return self.frame_input.nametowidget(name).get()

        # Алгоритмы на нахождение минимума
        if self.algorithm in self.extremum_algorithms:
            # Считаем
            xy, bestScore, data = globals()[self.algorithm.strip('"')](
                *list(map(lambda widget: widget.get(), self.widgets_arr[:-1])),
                function=functions_arr[self.widgets_arr[-1].current()])
            # Выводим результат
            ShowResult(data=data,
                       max_i=int(self.frame_input.nametowidget("numberGeneration").get()),
                       frame_btn=self.frame_btn,
                       frame_scroll=self.frame_scroll,
                       snapshot_name=self.algorithm[0])

            text = "x={0}; y={1}\n Значение функции: {2}".format(xy[0], xy[1], bestScore)
            self.output_label.configure(text=text, fg='black', font=('Arial', 10))
            print(text)

        # Алгоритмы на нахождение минимального Гамильтона цикла
        elif self.algorithm in self.graphs_algorithms:
            # Считаем
            self.a.prepare_graphPaths()
            best_path, best_score = globals()[self.algorithm.strip('"')](
                *list(map(lambda widget: widget.get(), self.widgets_arr)),
                graphPaths=self.a.graphPaths)
            # Выводим результат
            try:
                self.a.draw_cycle(best_path)
            except IndexError:
                pass

            best_path = [top + 1 for top in best_path]  # избавились от индексации с 0
            text = "Лучший путь: {0} \n Лучшая найденная длина: {1}".format(best_path, best_score)
            self.output_label.configure(text=text, fg='black', font=('Arial', 10))
            print(text)
