from abc import ABC, abstractmethod
from typing import List
from src.Model.DisplayFile import DisplayFile
from src.Model.Drawable import Drawable


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
