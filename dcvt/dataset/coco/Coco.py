from typing import List
import os
from datetime import datetime

from dcvt.util import DcvtFileManager, DcvtCalculation
from dcvt.labelmap import Default_map

fs = DcvtFileManager()
calc = DcvtCalculation()


class CocoInfo:
    def __init__(self):
        current_date = datetime.now()

        self.description: str = None
        self.url: str = None
        self.version: str = None
        self.year: int = current_date.year
        self.contributor: str = None
        self.date_created: str = current_date.strftime("%Y-%m-%d %H:%M:%S.%f")

    def set_cocoInfo(self, description: str, url: str, version: str, contributor: str):

        self.description = description
        self.url = url
        self.version = version
        self.contributor = contributor

        return self

    def make_cocoinfo_dict(self) -> dict:
        return {
            "description": self.description,
            "url": self.url,
            "version": self.version,
            "year": self.year,
            "contributor": self.contributor,
            "date_created": self.date_created,
        }


class CocoLicenses:
    def __init__(self):
        self.url: str = None
        self.id: int = 0
        self.name: str = None

    def set_cocoLicenses(self, url: str, license_id: int, name: str):
        self.url = url
        self.id = license_id
        self.name = name
        return self

    def make_cocolicenses_dict(self) -> dict:
        return {"url": self.url, "id": self.id, "name": self.name}


class CocoImages:
    def __init__(self):
        self.license: int = 0
        self.url: str = None
        self.file_name: str = ""
        self.height: int = 0
        self.width: int = 0
        self.date_captured: str = None
        self.id: int = 0

    def set_cocoImages(
        self,
        file_name: str,
        height: int,
        width: int,
        image_id: int,
        license: int = 0,
        url: str = None,
        date_captured: str = None,
    ):
        self.license = license
        self.url = url
        self.file_name = file_name
        self.height = height
        self.width = width
        self.date_captured = date_captured
        self.id = image_id
        return self

    def make_cocoimages_dict(self) -> dict:
        return {
            "license": self.license,
            "url": self.url,
            "file_name": self.file_name,
            "height": self.height,
            "width": self.date_captured,
            "id": self.id,
        }


class CocoAnnotations:
    def __init__(self):
        self.id: int = 0
        self.image_id: int = 0
        self.category_id: int = 0
        self.name: str = ""
        self.segmentation: List[list] = []
        self.area: int = 0
        self.bbox: list = []
        self.iscrowd: int = 0
        self.labelmap: List[dict] = []

    def set_cocoAnnotations(
        self,
        anno_id: int,
        image_id: int,
        category_id: int,
        segmentation: List[list],
        area: int,
        bbox: list,
        iscrowd: int = 0,
        labelmap: List[dict] = Default_map,
        label_name: str = "",
    ):
        self.id = anno_id
        self.image_id = image_id
        self.category_id = category_id
        self.labelmap = labelmap
        if label_name != "":
            self.name = label_name
        else:
            self.name = self._search_label_name_by_id(self.category_id, labelmap)
        self.segmentation = segmentation
        self.area = area
        self.bbox = bbox
        self.iscrowd = iscrowd
        return self

    @staticmethod
    def _search_label_name_by_id(cat_id, labelmap):
        return fs.find_label_name_by_id(cat_id, labelmap)

    def make_cocoanno_dict(self) -> dict:
        return {
            "id": self.id,
            "image_id": self.image_id,
            "category_id": self.category_id,
            "segmentation": calc.points_flatten(self.segmentation),
            "area": self.area,
            "bbox": self.bbox,
            "iscrowd": self.iscrowd,
        }


class CocoCategories:
    def __init__(self):
        self.supercategory: str = None
        self.id: int = 0
        self.name: str = ""

    def set_cocoCategories(self, cat_id: int, name: str, supercategory: str = None):
        self.supercategory = supercategory
        self.id = cat_id
        self.name = name
        return self

    def make_cococat_dict(self) -> dict:
        return {"supercategory": self.supercategory, "id": self.id, "name": self.name}


class CocoDataSet:
    def __init__(self):
        self.info: CocoInfo = CocoInfo()
        self.licenses: List[CocoLicenses] = [CocoLicenses()]
        self.images: List[CocoImages] = []
        self.type: str = "instances"
        self.annotations: List[CocoAnnotations] = []
        self.categories: List[CocoCategories] = []

    def convert_dataset_by_convert_type(
        self, convert_object: object, convert_label_type: str, idx: int = 0
    ):
        if convert_label_type == "labelme":
            pass
        elif convert_label_type == "ade20k":
            pass
        elif convert_label_type == "voc":
            pass

    def load_label_from_file(self, label_path: str) -> None:
        pass

    def _set_labelmap(self, labelmap: List[dict]):
        category_list = []
        for label in labelmap:
            cat = CocoCategories()
            cat.set_cocoCategories(label["id"], label["name"])
            category_list.append(cat)

        self.categories = category_list

    def set_cocoDataset(
        self,
        type: str = "instances",
        labelmap: List[dict] = Default_map,
    ):
        self._set_labelmap(labelmap)
        self.type = type

    def add_cocoImages(
        self,
        file_name: str,
        height: int,
        width: int,
        img_id: int,
        license: int = 0,
        url: str = None,
        date_cap: str = None,
    ) -> None:
        coco_image = CocoImages()
        coco_image.set_cocoImages(
            file_name, height, width, img_id, license, url, date_cap
        )
        self.images.append(coco_image)

    def add_cocoAnno(
        self,
        image_id: int,
        cat_id: int,
        seg: List[list],
        bbox: list,
        iscrowd: int = 0,
    ) -> None:
        coco_anno = CocoAnnotations()

        area = calc.cal_area(seg)
        anno_id = len(self.annotations)
        coco_anno.set_cocoAnnotations(
            anno_id, image_id, cat_id, seg, area, bbox, iscrowd
        )
        self.annotations.append(coco_anno)

    def add_cocoCat(self, cat_id: int, name: str, super_cat: str = None) -> None:
        coco_cat = CocoCategories()
        coco_cat.set_cocoCategories(cat_id, name, super_cat)
        self.categories.append(coco_cat)

    def make_coco_dict(self) -> dict:
        data = {
            "info": self.info.make_cocoinfo_dict(),
            "licenses": [i.make_cocolicenses_dict() for i in self.licenses],
            "images": [i.make_cocoimages_dict() for i in self.images],
            "type": self.type,
            "annotations": [i.make_cocoanno_dict() for i in self.annotations],
            "categories": [i.make_cococat_dict() for i in self.categories],
        }

        print("Complete labelme dict..")
        return data

    def save(self, output_path: str, save_vis) -> None:
        data = self.make_coco_dict()
        output_path = os.path.join(output_path, 'annotations.json')
        fs.save_json(data, output_path)
