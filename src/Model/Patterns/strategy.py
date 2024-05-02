from abc import ABC, abstractmethod
from typing import List
from src.Model.DisplayFile import DisplayFile
from src.Model.Drawable import Drawable
from src.Model.Window import Window
import numpy as np


class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def clipping_algorithm(self, display_file:DisplayFile) -> List[Drawable]:
        pass

class ProjectionStrategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def build_projection_matrix(self, window: Window) -> np.ndarray:
        pass
