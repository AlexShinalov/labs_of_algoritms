import random
import tkinter as tk
from tkinter import ttk
from abstract.abstract import AlgoAbstract
from Helpers.Correlation import Correlatin
from Helpers.Images import Images
from tkinter import filedialog
from tkinter.messagebox import showinfo, askyesno
from tkinter.simpledialog import askstring

# Класс GUI, основанный на tk.Tk, для создания графического интерфейса
class GUI(tk.Tk):
    def __init__(self, title, algo: AlgoAbstract):
        tk.Tk.__init__(self)
        self.title(title) # Установка заголовка окна
        self.algo = algo(distantion=Correlatin.distantion, isMax=False) # Инициализация алгоритма
        self.create_menu() # Создание меню
        self.create_table() # Создание таблицы
        self.directories = {"train": None, "test": None} # Инициализация словаря для хранения путей к директориям

    # Создание меню в окне
    def create_menu(self) -> None:
        menu = tk.Menu(self)
        self.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Датасет", menu=file_menu)
        file_menu.add_command(label="Обучающий датасет", command=lambda: self.add_directory("train"))
        file_menu.add_command(label="Датасет для определения", command=lambda: self.add_directory("test"))
        
        algo_menu = tk.Menu(menu)
        menu.add_cascade(label="Алгоритм", menu=algo_menu)
        algo_menu.add_command(label="Запуск", command=lambda: self.start_algorithm(isTest=False))
        algo_menu.add_command(label="Протестировать", command=lambda: self.start_algorithm(isTest=True))

    # Создание таблицы в окне
    def create_table(self) -> None:
        self.tree = ttk.Treeview(self, columns=("termal", "visible"), show="headings")
        self.tree.heading("visible", text="В видимом свете")
        self.tree.heading("termal", text="Термальное")
        self.tree.pack(side="top", fill="both", expand=True)

    # Добавление строки в таблицу
    def add_row(self, value1, value2):
        self.tree.insert("", "end", values=(value1, value2))
        
    # Выбор директории с датасетом
    def add_directory(self, role: str) -> None:
        showinfo(title="директрия", message="Укажите директори, в которой находится датасет. Изображения должны быть в разных папках."
                 "После того как программа отработает, в таблице в соответствующих строках будут ссылки на 2 ибозражения"
                 )
        
        file_path = filedialog.askdirectory()
        self.directories[role] = file_path
        
   # Запуск алгоритма с возможностью тестирования
    def start_algorithm(self, isTest: bool = False) -> None:
        """
        Запускает алгоритм обучения или тестирования в зависимости от параметра isTest.
        
        Параметры:
        - isTest (bool): Флаг, указывающий на необходимость тестирования алгоритма.
        
        Предполагается, что перед вызовом этой функции были выбраны директории с обучающими и тестовыми наборами данных.
        """
        
        # Если isTest истинно, выполняем тестирование алгоритма
        if isTest:
            # Генерация случайных чисел для выбора обучающих и тестовых наборов
            train_num = random.randint(1, 5)
            test_num = random.randint(1, 5)
            
            # Загрузка ссылок на изображения для тестирования
            links_x, links_y = Images.get_links(num_test=4, dataset="dataset_old")
            # Загрузка изображений по ссылкам
            X = Images.get_pictures(links_x)
            Y = Images.get_pictures(links_y)
            # Обучение алгоритма на загруженных изображениях
            self.algo.fit(X, Y, withRRPP=False)
            
            # Загрузка ссылок на изображения для тестирования
            links = Images.get_links(num_test=3, dataset="dataset_old")
            
            # Тестирование алгоритма на каждом изображении
            for index in 0, 1:
                matrix = Images.get_pictures(links[index])
                # Предсказание результатов на основе тестового набора
                result = self.algo.predict(matrix, isX=True if index == 0 else False)
                
                # Подсчет количества правильных предсказаний
                k = 0
                for m in range(len(result)):
                    if m == result[m][0]:
                        k += 1
                    # Вывод результатов предсказания
                    print(m, result[m])
                
                # Отображение информации о тестировании
                showinfo(
                    title=f"использовались train: {train_num} и test: {test_num}",
                    message=f"для {'termal' if index == 0 else 'visible'}\n"
                    f"количество угаданных: {k} \n"
                    f"всего: {len(result)} \n"
                    f"вероятнотсь угадывания: {round(k / len(result), 5)} \n"
                )
        
        # Если isTest ложно, выполняем обучение алгоритма
        else:
            # Загрузка ссылок на изображения для обучения
            links_train = Images.get_links_for_gui(self.directories["train"])
            # Загрузка изображений по ссылкам
            X = Images.get_pictures(links_train[0])
            Y = Images.get_pictures(links_train[1])
            
            # Запрос у пользователя о необходимости выполнения РРПП
            withRRPP = askyesno(title="РРПП", message="Необходимо ли делать РРПП?") 
            if withRRPP:
                # Запрос у пользователя количества компонент для РРПП
                count_RRPP = int(askstring(title="РРПП", prompt="Сколько брать компонент?"))
                self.algo.d = count_RRPP
            
            # Обучение алгоритма на загруженных изображениях
            self.algo.fit(X, Y, withRRPP=withRRPP)
            
            # Запрос у пользователя о типе определения
            isX = askyesno(title="Определение", message="Вы хотите по термальному определить в видимом свете?") 
            
            # Загрузка ссылок на изображения для тестирования
            links_test = Images.get_links_for_gui(self.directories["test"])
            # Выбор изображений для тестирования в зависимости от выбора пользователя
            matrix = Images.get_pictures(links_train[0]) if isX else Images.get_pictures(links_train[1])
            
            # Предсказание результатов на основе тестового набора
            result = self.algo.predict(matrix, isX=isX)
            
            # Обработка и вывод результатов предсказания
            for index, answer in enumerate(result):
                print(index, answer)
                # Определение ссылок на изображения для добавления в таблицу
                if not isX:
                    termal_link = links_test[0][answer[0]]
                    visible_link = links_test[0][index]
                else:
                    termal_link = links_test[0][index]
                    visible_link = links_test[0][answer[0]]
                # Добавление строки в таблицу с результатами
                self.add_row(f"{termal_link.split('/')[-2]}/{termal_link.split('/')[-1]}", f"{visible_link.split('/')[-2]}/{visible_link.split('/')[-1]}")
    