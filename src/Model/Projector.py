from __future__ import annotations
from typing import List
from src.Model.Projecting.ParallelProjector import ParallelProjector
from copy import deepcopy


class Projector():
    '''Prector is a class that is responsible for projecting 3D objects to a 2D plane, it will do so by
    an implementation of a strategy pattern, where the strategy will be the type of projection that will be used'''

    def __init__(self, strategy = ParallelProjector()) -> None:
        '''The constructor of the class, it will receive a strategy that will be used to project the objects'''

        self._strategy = strategy

    def build_projection_matrix(self, window) -> List[List[float]]:
        pass