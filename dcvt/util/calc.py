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
        for point in points:
            if isinstance(point, list):
                flatten_points.extend(point)
            else:
                flatten_points.append(point)
        return flatten_points

    @staticmethod
    def get_bbox(points: List[list]) -> list:
        xmin = DcvtCalculation.get_xmin(points)
        ymin = DcvtCalculation.get_ymin(points)
        xmax = DcvtCalculation.get_xmax(points)
        ymax = DcvtCalculation.get_ymax(points)
        return [xmin, ymin, xmax, ymax]

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
