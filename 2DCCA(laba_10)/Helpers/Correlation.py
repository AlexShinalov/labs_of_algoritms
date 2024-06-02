import numpy as np

class Correlatin:
    @staticmethod
    def average(matrix1: np.ndarray, matrix2: np.ndarray) -> float:
        # Вычисление среднего значения каждой матрицы
        M1 = matrix1.mean()
        M2 = matrix2.mean()

        # Вычитание среднего значения из соответствующих элементов каждой матрицы
        A = np.subtract(matrix1, M1)
        B = np.subtract(matrix2, M2)

        # Вычисление корреляционного коэффициента
        alpha = np.sum(A*B) / (np.sqrt(np.sum(A**2) * np.sum(B**2)))
        return alpha

    @staticmethod
    def cov(matrix1: np.ndarray, matrix2: np.ndarray) -> float:
        # Преобразование матриц в одномерные массивы
        vector1 = matrix1.flatten()
        vector2 = matrix2.flatten()
        
        # Вычисление ковариационной матрицы
        cov_matrix = np.cov(vector1, vector2)
        
        # Вычисление матрицы стандартных отклонений
        std_matrix = np.sqrt(np.diag(cov_matrix))
        
        # Вычисление корреляционной матрицы
        corr_matrix = cov_matrix / np.outer(std_matrix, std_matrix)
        
        # Получение коэффициента корреляции из корреляционной матрицы
        correlation_coefficient = corr_matrix[0, 1]
        
        return correlation_coefficient
    
    @staticmethod
    def pirson(matrix1: np.ndarray, matrix2: np.ndarray) -> float:
            # Преобразование матриц в одномерные массивы
            vector1 = matrix1.flatten()
            vector2 = matrix2.flatten()

            # Вычисление средних значений
            mean1 = np.mean(vector1)
            mean2 = np.mean(vector2)

            # Вычисление ковариации
            covariance = np.cov(vector1, vector2)[0][1]

            # Вычисление стандартных отклонений
            std1 = np.std(vector1)
            std2 = np.std(vector2)

            # Расчет коэффициента корреляции Пирсона
            correlation_coefficient = covariance / (std1 * std2)

            return correlation_coefficient

    @staticmethod
    def cov_set(X: np.ndarray, Y: np.ndarray) -> float:
        return sum([Correlatin.cov(x, y) for x, y in zip(X, Y)]) / len(X)
    
    @staticmethod
    def cov_element(matrix: np.ndarray) -> float:
        # Вычисление корреляций между каждой парой переменных
        correlations = np.corrcoef(matrix, rowvar=False)

        # Суммирование корреляций
        sum_of_correlations = np.sum(correlations)

        # Количество пар переменных
        num_pairs = matrix.shape[1] * (matrix.shape[1] - 1) / 2

        # Расчет средней корреляции
        average_correlation = sum_of_correlations / num_pairs
        
        return average_correlation
    
    @staticmethod
    def distantion(X: np.ndarray, Y: np.ndarray) -> float:
        return np.sum(np.abs(X - Y))