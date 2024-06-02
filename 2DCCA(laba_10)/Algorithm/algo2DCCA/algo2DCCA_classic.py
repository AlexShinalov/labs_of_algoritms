import cv2
import numpy as np
import matplotlib.pyplot as plt
from abstract.abstract import AlgoAbstract

# Класс Algo2DCCA наследуется от AlgoAbstract и реализует алгоритм двухмерного канонического корреляционного анализа (2DCCA).
class Algo2DCCA(AlgoAbstract):
    def __init__(self, d: int = 10, distantion = lambda x, y: np.linalg.norm(x - y), isMax: bool = False) -> None:
        # Инициализация атрибутов класса
        self.U = None
        self.V = None
        self.W = None
        self.X_c = None
        self.Y_c = None
        self.links_x = None
        self.links_y = None
        self.d = d # Количество компонент для выделения
        self.distantion = distantion # Функция расстояния между векторами
        self.reg_coef_C: float = 10**(-4) # Регуляризационный коэффициент для матриц корреляции
        self.reg_coef_S: float = 5 * 10**(-4) # Регуляризационный коэффициент для матриц сингулярных значений
        self.isMax= isMax # Флаг, указывающий на использование максимального значения в качестве результата
        
    def transform(self, matrix_set: np.ndarray, isX: bool=True) -> np.ndarray:
        # Метод transform преобразует данные с использованием матрицы W
        result = list()
        if isX:
            for i in range(len(matrix_set)):
                result.append(self.W["x"][0].T @ (matrix_set[i] - self.X_c) @ self.W["x"][1])
        else:
            for i in range(len(matrix_set)):
                result.append(self.W["y"][0].T @ (matrix_set[i] - self.X_c) @ self.W["y"][1])
        
        return np.array(result) 
    
    def fit(self, X: list, Y: list, withRRPP: bool = False) -> None:
        # Метод fit выполняет обучение модели на данных X и Y
        self.X_c = np.mean(X, axis=0) # Вычисление центроида для X
        self.Y_c = np.mean(Y, axis=0) # Вычисление центроида для Y
        X -= self.X_c # Централизация данных X
        Y -= self.Y_c # Централизация данных Y
        # Вычисление матриц корреляции для X и Y
        C_rxx = self._calculate_covarianсу_matrix(X, X, for_r=True)
        C_ryy = self._calculate_covarianсу_matrix(Y, Y, for_r=True)
        C_rxy = self._calculate_covarianсу_matrix(X, Y, for_r=True)
        C_ryx = self._calculate_covarianсу_matrix(Y, X, for_r=True)
        C_cxx = self._calculate_covarianсу_matrix(X, X, for_r=False)
        C_cyy = self._calculate_covarianсу_matrix(Y, Y, for_r=False)
        C_cxy = self._calculate_covarianсу_matrix(X, Y, for_r=False)
        C_cyx = self._calculate_covarianсу_matrix(Y, X, for_r=False)
        # Регуляризация матриц корреляции
        C_rxx = C_rxx + self.reg_coef_C * np.identity(C_rxx.shape[0]) 
        C_ryy = C_ryy + self.reg_coef_C * np.identity(C_ryy.shape[0]) 
        C_cxx = C_cxx + self.reg_coef_C * np.identity(C_cxx.shape[0])
        C_cyy = C_cyy + self.reg_coef_C * np.identity(C_cyy.shape[0]) 
        # Вычисление матриц сингулярных значений
        S_1r = np.linalg.inv(C_rxx) @ C_rxy @ np.linalg.inv(C_ryy) @ C_ryx
        S_1c = np.linalg.inv(C_cxx) @ C_cxy @ np.linalg.inv(C_cyy) @ C_cyx
        S_2r = np.linalg.inv(C_ryy) @ C_ryx @ np.linalg.inv(C_rxx) @ C_rxy
        S_2c = np.linalg.inv(C_cyy) @ C_cyx @ np.linalg.inv(C_cxx) @ C_cxy
        # Регуляризация матриц сингулярных значений
        S_1r = S_1r + self.reg_coef_S * np.identity(S_1r.shape[0])
        S_2r = S_2r + self.reg_coef_S * np.identity(S_2r.shape[0])
        S_1c = S_1c + self.reg_coef_S * np.identity(S_1c.shape[0])
        S_2c = S_2c + self.reg_coef_S * np.identity(S_2c.shape[0])
        # Вычисление собственных значений и векторов сингулярных значений
        l_1r, v_x1 = np.linalg.eig(S_1r)
        l_1c, v_x2 = np.linalg.eig(S_1c)
        l_2r, v_y1 = np.linalg.eig(S_2r)
        l_2c, v_y2 = np.linalg.eig(S_2c)
        # Нормализация векторов сингулярных значений
        v_x1 = v_x1[:, l_1r.argsort()[::-1]] / np.linalg.norm(v_x1) 
        v_y1 = v_y1[:, l_2r.argsort()[::-1]] / np.linalg.norm(v_y1)
        v_x2 = v_x2[:, l_1c.argsort()[::-1]] / np.linalg.norm(v_x2)
        v_y2 = v_y2[:, l_2c.argsort()[::-1]] / np.linalg.norm(v_y2)
        # Инициализация матрицы W для преобразования данных
        self.W = {"x": [None, None],"y": [None, None]}
        # Выбор компонент для преобразования данных
        if withRRPP:
            self.W["x"][0] = v_x1.T[:, l_1r.argsort()[-self.d:][::-1]]
            self.W["x"][1] = v_x2.T[:, l_1c.argsort()[-self.d:][::-1]]
            self.W["y"][0] = v_y1.T[:, l_2r.argsort()[-self.d:][::-1]]
            self.W["y"][1] = v_y2.T[:, l_2c.argsort()[-self.d:][::-1]]
        else:
            self.W["x"][0] = v_x1.T
            self.W["x"][1] = v_x2.T
            self.W["y"][0] = v_y1.T
            self.W["y"][1] = v_y2.T
        # Преобразование данных X и Y
        self.U = self.transform(X + self.X_c, isX=True)
        self.V = self.transform(Y + self.Y_c, isX=False) 
             
        
    def predict(self, matrixes: list, isX: bool = True) -> tuple[int, float]:
        # Преобразование входных данных с использованием метода transform
        matrixes_transform = self.transform(matrixes, isX=isX)
        # Выбор обучающих данных в зависимости от типа входных данных (X или Y)
        matrixes_train = self.U if isX else self.V

        # Инициализация матрицы расстояний между преобразованными входными данными и обучающими данными
        matrix_distantion = np.zeros((len(matrixes), len(matrixes_train)), dtype="float64")

        # Вычисление расстояний между каждой парой преобразованных входных данных и обучающих данных
        for udx, m_transform in enumerate(matrixes_transform):
            for vdx, m_train in enumerate(matrixes_train):
                # Использование пользовательской функции расстояния для вычисления расстояния между векторами
                distantion = self.distantion(m_transform, m_train)
                matrix_distantion[udx][vdx] = distantion

        # Выбор индекса и значения расстояния в зависимости от флага isMax
        results = list()
        for vector in matrix_distantion:
            if self.isMax:
                results.append([vector.argmax(), vector.max()])
            else:
                results.append([vector.argmin(), vector.min()])

        return results
    
    def _calculate_covarianсу_matrix(self, matrixes_1: np.ndarray, matrixes_2: np.ndarray, 
                                 for_r: bool = True) -> np.ndarray:
        # Проверка условия для вычисления ковариационной матрицы
        if for_r:
            # Вычисление ковариационной матрицы
            C = np.sum([matrixes_1[i] @ matrixes_2[i].T for i in range(len(matrixes_1))], axis=0)
        else:
            # Вычисление ковариационной матрицы для центрированных данных
            C = np.sum([matrixes_1[i].T @ matrixes_2[i] for i in range(len(matrixes_1))], axis=0)
        return C
