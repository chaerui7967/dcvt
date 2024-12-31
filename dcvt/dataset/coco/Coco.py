from dcvt.util import DcvtFileManager

fs = DcvtFileManager()


class CocoDataSet:
    def __init__(self):
        pass

    def convert_dataset_by_convert_type(
        self, convert_object: object, convert_label_type: str
    ):
        if convert_label_type == "labelme":
            pass
        elif convert_label_type == "ade20k":
            pass
        elif convert_label_type == "voc":
            pass

    def load_label_from_file(self, label_path: str) -> None:
        pass
