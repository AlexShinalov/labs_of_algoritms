import cv2
import numpy as np
from Helpers.Multiprocessor import Multiprocessor
from abstract.abstract import AlgoAbstract

class Algo2DPLS(AlgoAbstract):
    def __init__(self, d: int = 10, distantion = lambda x, y: np.linalg.norm(x - y), isMax: bool = True) -> None:
        self.U = None
        self.V = None
        self.W = {"x": [None, None], "y": [None, None]}
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
        
        mp = Multiprocessor()
        mp.run(self._calculate_W, X, Y, True, withRRPP=withRRPP)
        mp.run(self._calculate_W, X, Y, False, withRRPP=withRRPP)
        
        results = mp.wait()
        for result in results:
            if result[2]:
                self.W["x"][0] = result[0]
                self.W["y"][0] = result[1]
            else:
                self.W["x"][1] = result[0]
                self.W["y"][1] = result[1]
                
        
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
    
    def _calculate_W(self, X: np.ndarray, Y: np.ndarray, for_r: bool,
                     withRRPP: bool = False) -> tuple[np.ndarray, np.ndarray, bool]: 
        C_xy = self._calculate_covarianсу_matrix(X, Y, for_r=for_r)
        C_yx = self._calculate_covarianсу_matrix(Y, X, for_r=for_r)
         
        S_x =  C_xy @ C_yx
        S_y =  C_yx @ C_xy 
        
        S_x = S_x + self.reg_coef_S * np.identity(S_x.shape[0])
        S_y = S_y + self.reg_coef_S * np.identity(S_y.shape[0]) 
        
        l_x, v_x = np.linalg.eig(S_x)
        l_y, v_y = np.linalg.eig(S_y)
        
        if withRRPP:
            v_x = v_x.T[:, l_x.argsort()[-self.d:][::-1]]
            v_y = v_y.T[:, l_y.argsort()[-self.d:][::-1]]
        else:
            v_x = v_x[:, l_x.argsort()[::-1]].T
            v_y = v_y[:, l_y.argsort()[::-1]].T
        
        return v_x, v_y, for_r
               
            
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
    