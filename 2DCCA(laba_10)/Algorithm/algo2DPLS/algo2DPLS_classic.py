import cv2
import numpy as np
from abstract.abstract import AlgoAbstract
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class Algo2DPLS(AlgoAbstract):
    def __init__(self, d: int = 10, distantion = lambda x, y: np.linalg.norm(x - y), isMax: bool = False) -> None:
        self.U = None
        self.V = None
        self.W = None
        self.X_c = None
        self.Y_c = None
        self.links_x = None
        self.links_y = None
        self.d = d
        self.distantion = distantion
        self.reg_coef_S: float = 5 * 10**(-4)
        self.isMax = isMax
    
    def fit(self, X: list, Y: list, withRRPP: bool = False) -> None:
        
        self.X_c = np.mean(X, axis=0)
        self.Y_c = np.mean(Y, axis=0)
        
        X -= self.X_c
        Y -= self.Y_c         
            
        C_rxy = self._calculate_covarianсу_matrix(X, Y, for_r=True)
        C_ryx = self._calculate_covarianсу_matrix(Y, X, for_r=True)
        
        C_cxy = self._calculate_covarianсу_matrix(X, Y, for_r=False)
        C_cyx = self._calculate_covarianсу_matrix(Y, X, for_r=False)
        
        
        S_1r = C_rxy @ C_ryx
        S_1c = C_cxy @ C_cyx
        S_2r = C_ryx @ C_rxy
        S_2c = C_cyx @ C_cxy
        
        
        S_1r = S_1r + self.reg_coef_S * np.identity(S_1r.shape[0])
        S_2r = S_2r + self.reg_coef_S * np.identity(S_2r.shape[0])
        S_1c = S_1c + self.reg_coef_S * np.identity(S_1c.shape[0])
        S_2c = S_2c + self.reg_coef_S * np.identity(S_2c.shape[0])
        
        l_1r, v_x1 = np.linalg.eig(S_1r)
        l_1c, v_x2 = np.linalg.eig(S_1c)
        l_2r, v_y1 = np.linalg.eig(S_2r)
        l_2c, v_y2 = np.linalg.eig(S_2c)
        
        v_x1 = v_x1[:, l_1r.argsort()[::-1]]
        v_y1 = v_y1[:, l_2r.argsort()[::-1]]
        v_x2 = v_x2[:, l_1c.argsort()[::-1]]
        v_y2 = v_y2[:, l_2c.argsort()[::-1]]
        
        # Создание сетки подграфиков 2x2
        fig, axs = plt.subplots(2, 2)
        
        # Первый подграфик
        axs[0, 0].bar([i+1 for i in range(len(l_1r))], l_1r, color="blue")
        axs[0, 0].legend(["Lr1"])
        
        # Второй подграфик
        axs[0, 1].bar([i+1 for i in range(len(l_1c))], l_1c, color="orange")
        axs[0, 1].legend(["Lc1"])
        
        # Третий подграфик
        axs[1, 0].bar([i+1 for i in range(len(l_2r))], l_2r, color="green")
        axs[1, 0].legend(["Lr2"])
        
        # Четвертый подграфик
        axs[1, 1].bar([i+1 for i in range(len(l_2c))], l_2c, color="red")
        axs[1, 1].legend(["Lc2"])
        
        plt.show()
                
        self.W = {"x": [None, None],"y": [None, None]}
        
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
        
        # for s in "x", "y":
        #     for n in 0, 1:
        #         self.W[s][n] /= np.linalg.norm(self.W[s][n])
        
        self.U = self.transform(X + self.X_c, isX=True)
        self.V = self.transform(Y + self.Y_c, isX=False)
        
    def transform(self, matrix_set: np.ndarray, isX: bool=True) -> np.ndarray:
        result = list()
        if isX:
            for i in range(len(matrix_set)):
                result.append(self.W["x"][0].T @ (matrix_set[i] - self.X_c) @ self.W["x"][1])
        else:
            for i in range(len(matrix_set)):
                result.append(self.W["y"][0].T @ (matrix_set[i] - self.X_c) @ self.W["y"][1])
        
        return np.array(result)  
             
        
    def predict(self, matrixes: list, isX: bool = True) -> tuple[int, float]:
        matrixes_transform = self.transform(matrixes, isX=isX)
        matrixes_train = self.U if isX else self.V
        
        matrix_distantion = np.zeros((len(matrixes), len(matrixes_train)), dtype="float64")
        
        for udx, m_transform in enumerate(matrixes_transform):
            for vdx, m_train in enumerate(matrixes_train):
                distantion = self.distantion(m_transform, m_train)
                matrix_distantion[udx][vdx] = distantion
                
        results = list()
        for vector in matrix_distantion:
            if self.isMax:
                results.append([vector.argmax(), vector.max()])
            else:
                results.append([vector.argmin(), vector.min()])
          
        return results                
            
    def _calculate_covarianсу_matrix(self, matrixes_1: np.ndarray, matrixes_2: np.ndarray, 
                                     for_r: bool = True) -> np.ndarray:
        if for_r:
            C = np.sum([matrixes_1[i] @ matrixes_2[i].T for i in range(len(matrixes_1))], axis=0)
        else:
            C = np.sum([matrixes_1[i].T @ matrixes_2[i] for i in range(len(matrixes_1))], axis=0)
        return C
               
    def _get_pictures(self, links_x: list[str], links_y: list[str]) -> tuple[np.ndarray, np.ndarray]:
        self.links_x = links_x
        self.links_y = links_y
        X = list()
        Y = list()
        for filenameX, filenameY in zip(self.links_x, self.links_y):
            imageX = cv2.imread(filenameX, 0).astype("float64")
            X.append(imageX)
            imageY = cv2.imread(filenameY, 0).astype("float64")
            Y.append(imageY)
        return X, Y
    