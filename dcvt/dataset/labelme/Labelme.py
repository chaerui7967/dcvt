from typing import List


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
            "points": self.points,
            "group_id": self.group_id,
            "shape_type": self.shape_type,
            "flags": self.flags,
        }
        return data


class LabelmeDataSet:
    def __init__(
        self,
        version: str,
        img_path: str,
        img_h: int,
        img_w: int,
        flags: dict = {},
        img_data: str = None,
    ):
        self.version: str = version
        self.flags: dict = flags
        self.shapes: List[LabelmeShape] = []
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
            "shapes": [],
            "imagePath": self.imagePath,
            "imageData": self.imageData,
            "imageHeight": self.imageHeight,
            "imageWidth": self.imageWidth,
        }

        for shape in self.shapes:
            assert isinstance(shape, LabelmeShape)
            data["shapes"].append(shape.make_labelmeshape_dict())

        print("Complete labelme dict..")
        return data
