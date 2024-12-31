from typing import List
import numpy as np


class DcvtCalculation:
    @staticmethod
    def cal_area(points: List[list]) -> int:
        pass

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
