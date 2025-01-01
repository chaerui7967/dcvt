from typing import List
import numpy as np
from shapely.geometry import Polygon


class DcvtCalculation:
    @staticmethod
    def cal_area(points: List[list]) -> int:
        polygon = Polygon(points)
        return polygon.area

    @staticmethod
    def points_flatten(points: List[list]) -> list:
        flatten_points = []
        for x, y in points:
            flatten_points.append(x)
            flatten_points.append(y)
        return flatten_points

    @staticmethod
    def get_xmin(points: List[list]) -> int:
        return min([int(x) for x, y in points])

    @staticmethod
    def get_xmax(points: List[list]) -> int:
        return max([int(x) for x, y in points])

    @staticmethod
    def get_ymin(points: List[list]) -> int:
        return min([int(y) for x, y in points])

    @staticmethod
    def get_ymax(points: List[list]) -> int:
        return max([int(y) for x, y in points])
