
from typing import List
from src.Model.DisplayFile import DisplayFile
from src.Model.Drawable import Drawable
from src.Model.Point import Point
from src.Model.Window import Window

class PointClipper():
    def clip(self, display_file: DisplayFile) -> List[Drawable]:
        __inside_window = []

        #print("Called point clipper")
        for point in display_file.points:
            if self.checkBoundaries(point, point.window):
                #print("WINDOW OBJECT MEMORY ADDRESS IN CLIPPER")
                #print(point.window)
                __inside_window.append(point)

        return __inside_window
                

    def checkBoundaries(self, point: Point, window: Window):
        if point.x < (window.xw_min+20) or point.x > (window.xw_max-20) or point.y < (window.yw_min+20) or point.y > (window.yw_max-20):
            print("Point is outside window")
            return False
        print("Point is inside window")
        return True
    
    