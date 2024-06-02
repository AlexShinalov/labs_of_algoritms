from abc import ABCMeta, abstractmethod
import numpy as np

class AlgoAbstract(metaclass=ABCMeta):
    @abstractmethod
    def fit(self, X: list, Y: list, withRRPP: bool = False) -> None:
        pass
    
    @abstractmethod
    def predict(self, X: list[str], Y: list[str]) -> tuple[int, float]:
        pass
    
    @abstractmethod
    def transform(self, natrix_set: np.ndarray, isX: bool=True) -> np.ndarray:
        pass