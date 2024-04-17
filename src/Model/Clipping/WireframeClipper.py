from src.Model.WireFrame import Wireframe
from src.Model.Line import Line
from src.Model.Point import Point
from src.Model.Clipping.LineClipper import Position
from src.Model.Window import Window
from src.Model.Clipping.LineClipper import CohenSutherland, LiangBarsky
from src.Model.Patterns.strategy import Strategy
from copy import deepcopy


class WeilerAtherton(Strategy):
    def clip(self, wireframe: Wireframe, windowobj: Window) -> Wireframe:

        _line_clipper = LiangBarsky()

        vertices = wireframe.points

        for point in vertices:
            point.normalizePoint()

        if all([self.outside_window(p) for p in vertices]):
            return None
        elif all([not self.outside_window(p) for p in vertices]):
            return wireframe
        
        _boarder = 20
        window_max = Point(windowobj.xw_max, windowobj.yw_max, window=Window())
        window_min = Point(windowobj.xw_min, windowobj.yw_min, window=Window())

        window_min.x = window_min.x + _boarder
        window_min.y = window_min.y + _boarder

        window_min.normalizePoint()
        window_max.x = window_max.x - _boarder
        window_max.y = window_max.y - _boarder
        window_max.normalizePoint()

        window_vertices_numbers = [((window_min.x_normalized, window_max.y_normalized), 0), ((window_max.x_normalized, window_max.y_normalized), 0), ((window_max.x_normalized, window_min.y_normalized), 0), ((window_min.x_normalized, window_min.y_normalized), 0)]
        object_vertices = [(c, 0) for c in vertices]
        window_vertices = deepcopy(window_vertices_numbers)

        number_points = len(object_vertices)
        enter_points = []
        for index in range(number_points):
            p0 = vertices[index]
            p1 = vertices[(index + 1) % number_points]

            linha = _line_clipper.clipping_algorithm(Line(p0, p1),windowobj=Window())
            if linha != None:
                if linha.end != p1:
                    point_index = object_vertices.index((p0, 0)) + 1
                    object_vertices.insert(point_index, (linha.end, 2))
                    window_vertices = self.w_a_get_window_index(window_vertices_numbers, window_vertices, linha.end, 2)

                if linha.start != p0:
                    point_index = object_vertices.index((p0, 0)) + 1
                    object_vertices.insert(point_index, (linha.start, 1))
                    enter_points.append((linha.start, 1))
                    window_vertices = self.w_a_get_window_index(window_vertices_numbers, window_vertices, linha.start, 1)

        new_polygons = []
        new_points = []
        if enter_points != []:
            while enter_points != []:
                reference_point = enter_points.pop(0)
                rf_p, _ = reference_point
                inside_points = [rf_p]
                point_index = object_vertices.index(reference_point) + 1
                new_points.append(reference_point)

                obj_len = len(object_vertices)
                for aux_index in range(obj_len):
                    (p, c) = object_vertices[(point_index + aux_index) % obj_len]
                    new_points.append((p, c))
                    inside_points.append(p)
                    if c != 0:
                        break
                
                last_point = new_points[-1]
                point_index = window_vertices.index(last_point)
                window_len = len(window_vertices)
                for aux_index in range(window_len):
                    (p, c) = window_vertices[(point_index + aux_index) % window_len]
                    new_points.append((p, c))
                    inside_points.append(p)
                    if c != 0:
                        break

                new_polygons.append(inside_points)
            coordinates = new_polygons
        else:
            coordinates = [vertices]

        new_wireframe = Wireframe(coordinates[0][0])
        new_wireframe.points = coordinates[0]
        new_wireframe.is_filled = wireframe.is_filled
        new_wireframe.color = wireframe.color
        return new_wireframe

    def w_a_get_window_index(window_vertices,finalwindow, point: Point, code):
        point.normalizePoint()
        x = point.x_normalized
        y = point.y_normalized
        window_vertices_copy = deepcopy(window_vertices)
        if x == window_vertices[1][0][0] or x > window_vertices[1][0][0]:
            index = window_vertices_copy.index(((window_vertices[2][0][0], window_vertices[2][0][1]), 0))
            finalwindow.insert(index, (point, code))
        if x == window_vertices[0][0][0] or x < window_vertices[0][0][0]:
            index = window_vertices_copy.index(((window_vertices[0][0][0], window_vertices[0][0][1]), 0))
            finalwindow.insert(index, (point, code))
        if y == window_vertices[1][0][1] or y > window_vertices[1][0][1]:
            index = window_vertices_copy.index(((window_vertices[1][0][0], window_vertices[1][0][1]), 0))
            finalwindow.insert(index, (point, code))
        if y == window_vertices[2][0][1] or y < window_vertices[2][0][1]:
            index = window_vertices_copy.index(((window_vertices[3][0][0], window_vertices[3][0][1]), 0))
            finalwindow.insert(index, (point, code))
        return finalwindow

    def outside_window(point):
        return (point.x_normalized > 1 or point.x_normalized < -1) or (point.y_normalized > 1 or point.y_normalized < -1)

class SutherlandHodgman(Strategy):
    def clipping_algorithm(self, polygon: Wireframe, windowobj: Window):

        _boarder = 20
        window_max = Point(windowobj.xw_max, windowobj.yw_max, window=Window())
        window_min = Point(windowobj.xw_min, windowobj.yw_min, window=Window())

        window_min.x = window_min.x + _boarder
        window_min.y = window_min.y + _boarder

        window_min.normalizePoint()
        window_max.x = window_max.x - _boarder
        window_max.y = window_max.y - _boarder
        window_max.normalizePoint()

        clip_window = [
            (window_min.x_normalized, window_min.y_normalized),
            (window_max.x_normalized, window_min.y_normalized),
            (window_max.x_normalized, window_max.y_normalized),
            (window_min.x_normalized, window_max.y_normalized)
        ]

        print(clip_window)

        def inside(p, cp1, cp2):
            return (cp2[0] - cp1[0]) * (p[1] - cp1[1]) > (cp2[1] - cp1[1]) * (p[0] - cp1[0])

        def intersection(p1, p2, cp1, cp2):
            dc = (cp1[0] - cp2[0], cp1[1] - cp2[1])
            dp = (p1[0] - p2[0], p1[1] - p2[1])
            n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
            n2 = p1[0] * p2[1] - p1[1] * p2[0]
            n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
            return ((n1 * dp[0] - n2 * dc[0]) * n3, (n1 * dp[1] - n2 * dc[1]) * n3)

        output_list = []
        for point in polygon.points:
            point.normalizePoint()
            output_list.append((point.x_normalized, point.y_normalized))

        cp1 = clip_window[-1]

        for cp2 in clip_window:
            input_list = output_list
            output_list = []

            if len(input_list) == 0:
                return []
            p1 = input_list[-1]

            for p2 in input_list:
                if inside(p2, cp1, cp2):
                    if not inside(p1, cp1, cp2):
                        output_list.append(intersection(p1, p2, cp1, cp2))
                    output_list.append(p2)
                elif inside(p1, cp1, cp2):
                    output_list.append(intersection(p1, p2, cp1, cp2))
                p1 = p2
            cp1 = cp2

        print(output_list)

        first_point = Point(output_list[0][0], output_list[0][1], window=windowobj)
        first_point.unnormalizePoint()
        wireframeclipped = Wireframe(first_point)
        for i in range(1, len(output_list)):
            point = Point(output_list[i][0], output_list[i][1], window=windowobj)
            point.unnormalizePoint()
            wireframeclipped.addPoint(point)

        return wireframeclipped
    
    def clip(self, wireframe: Wireframe, windowobj: Window) -> Wireframe:
        return self.clipping_algorithm(wireframe, windowobj)