from __future__ import annotations
from typing import List
from src.Model.DisplayFile import DisplayFile
from src.Model.Drawable import Drawable
from src.Model.Patterns.strategy import Strategy
from src.Model.Clipping.PointClipper import PointClipper
from src.Model.Clipping.WireframeClipper import WeilerAtherton, SutherlandHodgman
from src.Model.Clipping.LineClipper import CohenSutherland, LiangBarsky
from src.Model.Window import Window
from copy import deepcopy


class Clipper():
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, strategy = LiangBarsky(), wireframe_clipper = SutherlandHodgman(), point_clipper = PointClipper()) -> None:
        """
        Usually, the Context accepts a strategy through the constructor, but
        also provides a setter to change it at runtime.
        """

        self._point_clipper = point_clipper
        self._line_clipper = strategy
        self._wireframe_clipper = wireframe_clipper

    @property
    def line_clipper(self) -> Strategy:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """

        return self._line_clipper

    @line_clipper.setter
    def line_clipper(self, line_clipper: Strategy) -> None:
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """

        if not isinstance(line_clipper, Strategy):
            return

        self._line_clipper = line_clipper

    @property
    def wireframe_clipper(self) -> Strategy:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """

        return self._wireframe_clipper

    @wireframe_clipper.setter
    def wireframe_clipper(self, wireframe_clipper: Strategy) -> None:
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """

        if not isinstance(wireframe_clipper, Strategy):
            return

        self._wireframe_clipper = wireframe_clipper

    def clip(self, display_file:DisplayFile) -> List[Drawable]:
        __inside_window = []

        clipped_points = self._point_clipper.clip(display_file)
        __inside_window.extend(clipped_points)

        for line in display_file.lines:
            clipped_line = self.line_clipper.clipping_algorithm(deepcopy(line), windowobj = Window())
            if clipped_line is not None:
                __inside_window.append(clipped_line)

        for wireframe in display_file.wireframes:
            clipped_wireframe = self._wireframe_clipper.clipping_algorithm(deepcopy(wireframe), windowobj=Window())
            if clipped_wireframe is not None:
                __inside_window.append(clipped_wireframe)

        for curve in display_file.curves:
            __inside_window.append(curve)

        return __inside_window
