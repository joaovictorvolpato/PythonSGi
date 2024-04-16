from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from src.Model.DisplayFile import DisplayFile
from src.Model.Drawable import Drawable
from src.Model.Patterns.strategy import Strategy
from src.Model.Clipping.PointClipper import PointClipper
from src.Model.Clipping.WireframeClipper import WireframeClipper
from src.Model.Clipping.LineClipper import CohenSutherland, LiangBarsky
from src.Model.Window import Window
from copy import deepcopy


class Clipper():
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, strategy = CohenSutherland(), wireframe_clipper = WireframeClipper(), point_clipper = PointClipper()) -> None:
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

    def clip(self, display_file:DisplayFile) -> List[Drawable]:
        __inside_window = []

        print("Called clip")
        clipped_points = self._point_clipper.clip(display_file)
        __inside_window.extend(clipped_points)

        for line in display_file.lines:
            clipped_line = self.line_clipper.clipping_algorithm(deepcopy(line), windowobj = Window())
            if clipped_line is not None:
                __inside_window.append(clipped_line)

        #ret = self._wireframe_clipper.clip(display_file)
        #__inside_window.extend(ret)

        return __inside_window
        