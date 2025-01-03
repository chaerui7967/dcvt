from typing import List

import cv2
import numpy as np

from dcvt.util import DcvtFileManager, DcvtCalculation

fs = DcvtFileManager()
calc = DcvtCalculation()

class Ade20kObject:
    def __init__(self):
        self.label_name: str = ""
        self.label_id: int = 0
        self.points: list = []
        self.area: int = 0
        self.color: tuple = ()

    def set_object(
        self,
        label_id: int,
        points: List[list],
        color: tuple = None,
        label_name: str = None,
    ):
        self.label_name = label_name
        self.label_id = label_id
        self.points = points
        self.area = self._get_area()
        self.color = color

    def _get_area(self) -> None:
        self.area = calc.cal_area(self.points)

    def cvt_point_as_int(self):
        return [[int(x[0]), int(x[1])] for x in self.points]


class Ade20kDataSet:
    def __init__(self):
        self.image_path: str = None
        self.annotation_path: str = None
        self.objects: List[Ade20kObject] = []
        self.background_id: int = 0

    def convert_dataset_by_convert_type(self, convert_label_type: str):
        if convert_label_type == "labelme":
            pass
        elif convert_label_type == "coco":
            pass
        elif convert_label_type == "voc":
            pass
        pass

    def load_label_from_file(self, label_path: str, image_path: str = None):
        self.image_path = image_path
        self.annotation_path = label_path
        if ".png" not in label_path:
            print("Ade20k label file must png file..")
            return
        ade_label = cv2.imread(self.annotation_path, cv2.IMREAD_GRAYSCALE)
        label, pixel = np.unique(ade_label, return_counts=True)
        label_info = dict(zip(label, pixel))

        for l, p in zip(label, pixel):
            if l == self.background_id:
                continue
            label_img = (ade_label == l).astype(np.uint8)
            contours, hierarchy = cv2.findContours(
                label_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
            )

            for idx, cnt in enumerate(contours):
                if hierarchy[0][idx][3] >= 0:
                    pass



    def set_background_id(self, background_id: int) -> None:
        self.background_id = background_id

    def _sort_label_by_area(self):
        pass

    def show_label_eval(self):
        pass

