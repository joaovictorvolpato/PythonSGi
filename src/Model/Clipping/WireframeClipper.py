from src.Model.WireFrame import Wireframe
from src.Model.Line import Line
from src.Model.Point import Point
from src.Model.Clipping.LineClipper import Position
from src.Model.Window import Window


class WireframeClipper():
    def clip(self, wireframe: Wireframe, window) -> Wireframe:
        vertices = wireframe.points

        if all([outside_window(p) for p in vertices]):
            return None

        window_vertices = [((-1, 1), 0), ((1, 1), 0), ((1, -1), 0), ((-1, -1), 0)]
        object_vertices = [(c, 0) for c in vertices]

        number_points = len(object_vertices)
        enter_points = []
        for index in range(number_points):
            p0 = vertices[index]
            p1 = vertices[(index + 1) % number_points]

            linha = cohen_sutherland(Line(p0, p1), window, Point(1, 1, window), Point(-1, -1, window))
            if linha != None:
                if linha.end != p1:
                    point_index = object_vertices.index((p0, 0)) + 1
                    object_vertices.insert(point_index, (linha.end, 2))
                    window_vertices = w_a_get_window_index(window_vertices, linha.end, 2)

                if linha.start != p0:
                    point_index = object_vertices.index((p0, 0)) + 1
                    object_vertices.insert(point_index, (linha.start, 1))
                    enter_points.append((linha.start, 1))
                    window_vertices = w_a_get_window_index(window_vertices, linha.start, 1)

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

def w_a_get_window_index(window_vertices, point, code):
    x = point.x_normalized
    y = point.y_normalized
    if x == 1:
        index = window_vertices.index(((1, -1), 0))
        window_vertices.insert(index, (point, code))
    if x == -1:
        index = window_vertices.index(((-1, 1), 0))

        window_vertices.insert(index, (point, code))
    if y == 1:
        index = window_vertices.index(((1, 1), 0))
        window_vertices.insert(index, (point, code))
    if y == -1:
        index = window_vertices.index(((-1, -1), 0))
        window_vertices.insert(index, (point, code))
    return window_vertices


def outside_window(point):
    return (point.x_normalized > 1 or point.x_normalized < -1) or (point.y_normalized > 1 or point.y_normalized < -1)

def cohen_sutherland(
    line: Line,
    window: Window,
    window_max: Point,
    window_min: Point,
) -> Line | None:
    xw_min, yw_min = [window_min.x, window_min.y]
    xw_max, yw_max = [window_max.x, window_max.y]
    window = {"xw_min": xw_min, "yw_min": yw_min, "xw_max": xw_max, "yw_max": yw_max}

    point1, point2 = line.points
    rc_point1 = _getRegionCode(point1, window)
    rc_point2 = _getRegionCode(point2, window)

    while True:
        if rc_point1 == 0 and rc_point2 == 0:
            line.setNormalCoordinates(point1, point2)
            return line
        elif (rc_point1 & rc_point2) != 0:
            return None
        else:
            newX, newY = 0, 0

            if rc_point1 != 0:
                rc_out = rc_point1
            else:
                rc_out = rc_point2

            if rc_out & Position.TOP.value:
                newX = point1.x_normalized + (
                    point2.x_normalized - point1.x_normalized
                ) * (window["yw_max"] - point1.y_normalized) / (
                    point2.y_normalized - point1.y_normalized
                )
                newY = window["yw_max"]

            elif rc_out & Position.BOTTOM.value:
                newX = point1.x_normalized + (
                    point2.x_normalized - point1.x_normalized
                ) * (window["yw_min"] - point1.y_normalized) / (
                    point2.y_normalized - point1.y_normalized
                )
                newY = window["yw_min"]

            elif rc_out & Position.RIGHT.value:
                newY = point1.y_normalized + (
                    point2.y_normalized - point1.y_normalized
                ) * (window["xw_max"] - point1.x_normalized) / (
                    point2.x_normalized - point1.x_normalized
                )
                newX = window["xw_max"]

            elif rc_out & Position.LEFT.value:
                newY = point1.y_normalized + (
                    point2.y_normalized - point1.y_normalized
                ) * (window["xw_min"] - point1.x_normalized) / (
                    point2.x_normalized - point1.x_normalized
                )
                newX = window["xw_min"]

            if rc_out == rc_point1:
                point1 = Point(point1.x, point1.y, Window)
                point1.setNormalCoordinates(newX, newY)
                rc_point1 = _getRegionCode(point1, window)
            else:
                point2 = Point(point2.x, point2.y, Window)
                point2.setNormalCoordinates(newX, newY)
                rc_point2 = _getRegionCode(point2, window)


def _getRegionCode(point1: Point, window: dict) -> int:
    x, y = [point1.x_normalized, point1.y_normalized]
    rc = Position.INSIDE.value

    if x > window["xw_max"]:
        rc |= Position.RIGHT.value
    elif x < window["xw_min"]:
        rc |= Position.LEFT.value

    if y > window["yw_max"]:
        rc |= Position.TOP.value
    elif y < window["yw_min"]:
        rc |= Position.BOTTOM.value

    return rc