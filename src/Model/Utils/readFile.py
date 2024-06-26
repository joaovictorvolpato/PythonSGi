import os
from PyQt5.QtGui import QColor

from src.Model.Point import Point
from src.Model.Point3D import Point3D
from src.Model.Line import Line
from src.Model.WireFrame import Wireframe, WireFrame3D
from src.Model.Window import Window

from typing import Tuple
from typing import List

def readFile(name: str, window_controller) -> Tuple[list, list]:
    if not os.path.isfile(f"src/objects/{name}"):
        name = f"{name}.obj"
        if not os.path.isfile(f"src/objects/{name}"):
            return

    objects = None
    window = None
    vertices = None
    materials = None

    with open(f"src/objects/{name}") as file:
        content = file.readlines()

        if name.__contains__("3d"):
            print("INSIDE 3D")
            name3d, vertices3d, faces3d = parseOBJ(content)
            objects = _createObjects(vertices, materials, objects, window_controller, vertices3d, faces3d, name3d)
        else:

            content = _clearContent(content)
            vertices, materials, objects, window = _processContent(content)
            objects = _createObjects(vertices, materials, objects, window_controller)

    print('objetos: ', objects)
    for obj in objects:
        print(obj.name)
    return objects, window

def parseOBJ(lines):
    name = ""
    vertices = []
    faces = []
    for line in lines:
        if line[0] == "g":
            name = line.split()[1]
        elif(line[0] in ["v", "vt", "vn", "vp"]):
            _,x,y,z = line.split()
            vertices.append(Point3D(float(x),float(y),float(z), window=Window(), name=name, color=None))
        elif(line[0] == "f"):
            faces.append([int(x) for x in line.split()[1::]])
        elif(line[0] == "a"):
            break

    return name, vertices, faces

def _clearContent(content: List[str]) -> List[str]:
    new_content = []
    for string in content:
        new_content.append(string.replace("\n", ""))

    return new_content

def _processContent(content: List[str]):
    vertices = []
    materials_files = []
    objects = {}
    window = None

    currentObj = None

    for string in content:
        string = string.split(" ")
        if string[0] == "v":
            vertices.append([float(val) for val in string[1:]])
        elif string[0] == "mtllib":
            materials_files.append(string[1])
        elif string[0] == "o":
            objects[string[1]] = {}
            currentObj = string[1]
        elif string[0] == "usemtl":
            objects[currentObj]["material"] = string[1]
        elif string[0] == "w":
            window = [string[1], string[2]]
        elif string[0] == "l":
            objects[currentObj]["points"] = string[1:]
        elif string[0] == "p":
            objects[currentObj]["points"] = [string[1]]
        elif string[0] == "f":  # for now, the same behavior as l
            objects[currentObj]["points"] = string[1:]
        else:  # string is the list of points
            objects[currentObj]["points"] = string[0:]

    if "window" in objects.keys():
        del objects["window"]

    materials = _readMaterialFile(materials_files)
    window = [vertices[int(window[0]) - 1], vertices[int(window[1]) - 1]]

    return vertices, materials, objects, window

def _readMaterialFile(materials_files: List[str]) -> dict:
    data = {}
    for file in materials_files:
        opened_file = open(f"src/objects/{file}")
        materials = opened_file.readlines()
        materials = _clearContent(materials)

        current = None
        for string in materials:
            string = string.split(" ")
            if string[0] == "newmtl":
                data[string[1]] = []
                current = string[1]
            if string[0] == "Kd":
                data[current] = _convertToHEX(string[1:])
        opened_file.close()

    return data

def _convertToHEX(values: List[str]):
    r, g, b = [int(float(val) * 255) for val in values]
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def _createObjects(vertices, materials, objects, window, vertices3d = None, faces3d = None, name3d = None):
    objects_list = []

    if objects is None:
        print('Entrou no if objects is None')
        print('name: ', name3d)
        wireframe3D = WireFrame3D(vertices=vertices3d, faces=faces3d, name=name3d, window=window)
        print(wireframe3D.name)
        objects_list.append(wireframe3D)
        return objects_list

    for objName, data in objects.items():
        points = data["points"]
        for i in range(len(points)):
            points[i] = vertices[int(points[i]) - 1]

        color = materials[data["material"]]
        color = QColor(color)

        if len(points) == 1:  # point
            point = [float(p) for p in points[0]]
            _p = Point(point[0], point[1], window,name=objName)
            _p.color = color
            objects_list.append(_p)
        elif len(points) == 2:  # line
            point1 = points[0]
            point1 = Point(float(point1[0]), float(point1[1]), window)
            point2 = points[1]
            point2 = Point(float(point2[0]), float(point2[1]), window)
            line = Line(point1, point2, name=objName, window=window)
            line.color = color
            objects_list.append(line)
        else:  # wireframe
            point1 = Point(float(points[0][0]), float(points[0][1]), window)
            wireframe = Wireframe(point1, name=objName, window=window)

            for point in points[1:]:
                wireframe.addPoint(Point(float(point[0]), float(point[1]), window))
            wireframe.color = color
            objects_list.append(wireframe)

        if (vertices3d is not None) and (faces3d is not None):
            wireframe3D = WireFrame3D(vertices=vertices3d, faces=faces3d, name=name3d, window=window)
            objects_list.append(wireframe3D)

    return objects_list
