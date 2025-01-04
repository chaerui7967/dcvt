import os.path
from typing import List
import json

from dcvt.util import DcvtFileManager, DcvtCalculation
from dcvt.labelmap import Default_map

fs = DcvtFileManager()
calc = DcvtCalculation()


class LabelmeShape:
    def __init__(
        self,
        label: str,
        points: list,
        group_id: str = None,
        shape_type: str = "polygon",
        flags: dict = {},
    ):
        self.label: str = label
        self.points: list = points
        self.group_id: str = group_id
        self.shape_type: str = shape_type
        self.flags: dict = flags

    def make_labelmeshape_dict(self) -> dict:
        data = {
            "label": self.label,
            "points": [[int(x), int(y)] for x, y in self.points],
            "group_id": self.group_id,
            "shape_type": self.shape_type,
            "flags": self.flags,
        }
        return data


class LabelmeDataSet:
    def __init__(self):
        self.version: str = "0.0.0"
        self.flags: dict = {}
        self.shapes: List[LabelmeShape] = []
        self.imagePath: str = None
        self.imageHeight: int = 0
        self.imageWidth: int = 0
        self.imageData: str = None

    def convert_dataset_by_convert_type(
        self,
        convert_object: object,
        convert_label_type: str,
        idx: int = 0,
        labelmap=Default_map,
    ):
        file_name = fs.get_filename(self.imagePath)
        folder = fs.get_parents_dir(self.imagePath)
        width = self.imageWidth
        height = self.imageHeight

        if convert_label_type == "voc":
            convert_object.set_voc_data(folder, file_name, self.imagePath)
            convert_object.set_size(width, height)
            for shape in self.shapes:
                name = shape.label
                xmin = calc.get_xmin(shape.points)
                ymin = calc.get_ymin(shape.points)
                xmax = calc.get_xmax(shape.points)
                ymax = calc.get_ymax(shape.points)
                convert_object.add_object(name, xmin, ymin, xmax, ymax)
        elif convert_label_type == "ade20k":
            pass
        elif convert_label_type == "coco":
            convert_object.set_cocoDataset(labelmap=labelmap)
            convert_file_path = os.path.basename(self.imagePath)
            convert_object.add_cocoImages(f'JPEGImages/{convert_file_path}', self.imageHeight, self.imageWidth, idx)
            for shape in self.shapes:
                label_name = shape.label
                label_id = fs.find_label_id_by_name(label_name, labelmap)
                bbox = calc.get_bbox(shape.points)
                convert_object.add_cocoAnno(idx, label_id, shape.points, bbox)
        else:
            return self

        return convert_object

    def load_label_from_file(self, json_path: str):
        data = fs.open_file_as_str(json_path)
        data = json.loads(data)

        if "shapes" not in data.keys():
            print(f"Not Shapes Key...{data}")
            return

        self.set_labelme_by_data(
            data["version"],
            data["imagePath"],
            data["imageHeight"],
            data["imageWidth"],
            data["flags"],
            data["imageData"],
        )

        for data_s in data["shapes"]:
            self.set_labelmeshape(
                data_s["label"],
                data_s["points"],
                data_s["group_id"],
                data_s["shape_type"],
                data_s["flags"],
            )

    def set_labelme_by_data(
        self,
        version: str,
        img_path: str,
        img_h: int,
        img_w: int,
        flags: dict = {},
        img_data: str = None,
    ) -> None:
        self.version: str = version
        self.flags: dict = flags
        self.imagePath: str = img_path
        self.imageHeight: int = img_h
        self.imageWidth: int = img_w
        self.imageData: str = img_data

    def set_labelmeshape(
        self,
        label: str,
        points: list,
        group_id: str = None,
        shape_type: str = "polygon",
        flags: dict = {},
    ) -> None:
        shape_data = LabelmeShape(label, points, group_id, shape_type, flags)
        self.shapes.append(shape_data)

    def make_label_dict(self) -> dict:
        data = {
            "version": self.version,
            "flags": self.flags,
            "shapes": [i.make_labelmeshape_dict() for i in self.shapes],
            "imagePath": self.imagePath,
            "imageData": self.imageData,
            "imageHeight": self.imageHeight,
            "imageWidth": self.imageWidth,
        }

        print("Complete labelme dict..")
        return data

    def save(self, output_path: str) -> None:
        data = self.make_label_dict()
        fs.save_json(data, output_path)
