from typing import List

import cv2
import numpy as np

from dcvt.util import DcvtFileManager, DcvtCalculation
from dcvt.labelmap import Default_map

fs = DcvtFileManager()
calc = DcvtCalculation()


class Ade20kObject:
    def __init__(self):
        self.name: str = ""
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
        self.name = label_name
        self.label_id = label_id
        self.points = points
        self._get_area()
        self.color = color

    def _get_area(self):
        self.area = calc.cal_area(self.points)

    def cvt_point_as_int(self):
        return [[int(x[0]), int(x[1])] for x in self.points]


class Ade20kDataSet:
    def __init__(self):
        self.image_path: str = None
        self.height: int = 0
        self.width: int = 0
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

    def set_ade20k_data(
        self, image_path: str, height: int, width: int, annotation_path: str
    ):
        self.image_path = image_path
        self.height = height
        self.width = width
        self.annotation_path = annotation_path

    def add_object(self, label_id, points, labelmap=Default_map):
        ade20k_object = Ade20kObject()
        label_name = fs.find_label_name_by_id(label_id, labelmap)
        color = fs.find_label_color_by_id(label_id, labelmap)
        ade20k_object.set_object(label_id, points, color, label_name)
        self.objects.append(ade20k_object)

    def _sort_label_by_area(self):
        self.objects = sorted(self.objects, key=lambda x: x.area, reverse=True)

    def show_label_eval(self):
        pass

    def _make_label_dict(self) -> dict:
        self._sort_label_by_area()
        label_dict = dict()
        for object in self.objects:
            if str(object.label_id) not in label_dict.keys():
                label_dict[str(object.label_id)] = [object.points]
            else:
                label_dict[str(object.label_id)].append(object.points)
        return label_dict

    def save(self, output_path: str, save_vis:bool) -> None:
        self._sort_label_by_area()
        label_data = np.zeros((self.height, self.width), np.uint8)
        vis_data = np.zeros((self.height, self.width), np.uint8)

        for obj in self.objects:
            points = np.array(obj.points, dtype=np.int32)
            points = points.reshape((-1, 1, 2))
            cv2.fillPoly(label_data, [points], obj.label_id)
            if save_vis:
                cv2.fillPoly(label_data, [points], obj.color)
        cv2.imwrite(output_path, label_data)
        if save_vis:
            vis_output_path = fs.make_vis_file_name(output_path)
            cv2.imwrite(vis_output_path, vis_data)
