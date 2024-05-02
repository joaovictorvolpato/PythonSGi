import numpy as np
from math import sin, cos, radians


class MatrixOperations:
    def __init__(self):
        self.__translation_matrix = None
        self.__scaling_matrix = None
        self.__rotation_matrix = None

    @property
    def get_translation_matrix(self) -> np.ndarray:
        return self.__translation_matrix

    def build_translation_matrix(self, tx: float, ty: float) -> np.ndarray:
        self.__translation_matrix = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [tx,ty, 1]
        ])
        return self.__translation_matrix

    @property
    def get_scaling_matrix(self) -> np.ndarray:
        return self.__scaling_matrix
    
    def build_scaling_matrix(self, sx: float, sy: float) -> np.ndarray:
        self.__scaling_matrix = np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ])
        return self.__scaling_matrix
    
    @property
    def get_rotation_matrix(self) -> np.ndarray:
        return self.__rotation_matrix
    
    def build_rotation_matrix(self, angle: float) -> np.ndarray:
        angle = radians(angle)
        self.__rotation_matrix = np.array([
            [cos(angle), -sin(angle), 0],
            [sin(angle), cos(angle), 0],
            [    0     ,     0    , 1]
        ])
        return self.__rotation_matrix

    def matrix_multiplication(self, matrix1: np.ndarray, matrix2:np.ndarray) -> np.ndarray:
        return np.dot(matrix1, matrix2)
    
    def matrix_composition(self, list_of_matrices) -> np.ndarray:
        result = list_of_matrices[0]
        for i in range(1, len(list_of_matrices)):
            result = self.matrix_multiplication(result, list_of_matrices[i])
        return result
    
    def transpose_matrix(self, matrix: np.ndarray) -> np.ndarray:
        return np.transpose(matrix)
    
    
class MatrixOperations3D(MatrixOperations):
    def __init__(self):
        super().__init__()
        self.__translation_matrix = None
        self.__scaling_matrix = None
        self.__rotation_matrix = None

    def build_translation_matrix(self, tx: float, ty: float, tz: float) -> np.ndarray:
        self.__translation_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [float(tx), float(ty), float(tz), 1]
        ])
        return self.__translation_matrix

    def build_scaling_matrix(self, sx: float, sy: float, sz: float) -> np.ndarray:
        self.__scaling_matrix = np.array([
            [float(sx), 0, 0, 0],
            [0, float(sy), 0, 0],
            [0, 0, float(sz), 0],
            [0, 0, 0, 1]
        ])
        return self.__scaling_matrix

    def build_rotation_matrix(self, angle: float, axis: str) -> np.ndarray:
        angle = radians(angle)
        if axis == "x":
            self.__rotation_matrix = np.array([
                [1, 0, 0, 0],
                [0, cos(angle), -sin(angle), 0],
                [0, sin(angle), cos(angle), 0],
                [0, 0, 0, 1]
            ])
        elif axis == "y":
            self.__rotation_matrix = np.array([
                [cos(angle), 0, sin(angle), 0],
                [0, 1, 0, 0],
                [-sin(angle), 0, cos(angle), 0],
                [0, 0, 0, 1]
            ])
        elif axis == "z":
            self.__rotation_matrix = np.array([
                [cos(angle), -sin(angle), 0, 0],
                [sin(angle), cos(angle), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
        return self.__rotation_matrix

