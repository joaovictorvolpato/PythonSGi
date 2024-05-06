
from src.Model.Patterns.strategy import ProjectionStrategy
from typing import List
from src.Model.Window import Window
from src.Model.Point import Point
#from src.Model.Point3D import Point3D


class ParallelProjector(ProjectionStrategy):
    def __init__(self) -> None:
        super().__init__()

    #From a 3D point, it will project it to a 2D point using parallel projection, in this case we ignore the z coordinate
    def project(self, point, window: Window) -> (int, int): # type: ignore
        return [[1,0,-point.x/1000,0],[0,1,-point.y/1000,0],[0,0,0,0],[0,0,-1/1000,1]]

    def build_projection_matrix(self, window: Window) -> List[List[float]]:
        pass