import os
import traceback

from PySide6.QtCore import QThread, Signal

from dcvt.dataset import *
from config_manager import ConfigManager

TEST_SAVE_PATH_DIR = "/Users/chaerui/project/side_project/test_tmp"

class ConvertWork(QThread):
    signal_update_progress = Signal(int)
    signal_start_or_stop_convert = None
    file_path = ""
    adjust_point = False
    input_label = None
    output_label = None

    def __init__(self, parent):
        super().__init__(parent)
        self._load_config()

    def _load_config(self):
        config = ConfigManager()
        config.load_config()

        self.converter_version = config.converter_version
        self.labelme_version = config.labelme_version

    def set_signal(self, signal):
        self.signal_start_or_stop_convert = signal

    def set_file_path(self, file_path):
        self.file_path = file_path

    def set_input_label(self, input_label):
        if input_label is None or len(input_label.strip()) == 0:
            self.input_label = None
        else:
            self.input_label = input_label

    def set_output_label(self, output_label):
        if output_label is None or len(output_label.strip()) == 0:
            self.output_label = None
        else:
            self.output_label = output_label

    def set_adjust_point(self, adjust):
        self.adjust_point = adjust

    def run(self):
        try:
            print("Start Converting..")
            print(f"Converter Versions : {self.converter_version}")
            print(f"labelme Versions : {self.labelme_version}")

            offset = 0.0
            offset += 10
            self.signal_update_progress.emit(offset)

            if self.input_label == "voc":
                search_ext = ".xml"
            elif self.input_label == "ade20k":
                search_ext = ".png"
            else:
                search_ext = ".json"

            label_paths = []
            for root, dirs, files in os.walk(self.file_path):
                for f in files:
                    if not f.endswith(search_ext):
                        continue
                    file_path = os.path.join(root, f)
                    label_paths.append(file_path)

            if not label_paths:
                offset += 90
                self.signal_update_progress.emit(offset)
            else:
                offset += 10
                self.signal_update_progress.emit(offset)

                progress_amount = 80.0 / len(label_paths)

                convert_object = None
                outpath = os.path.dirname(os.path.dirname(label_paths[-1]))

                for idx, p in enumerate(label_paths, 1):
                    result_data, convert_ext, convert_object = self._convert_dataset(
                        idx-1, p, self.input_label, self.output_label, convert_object
                    )
                    if convert_object is None:
                        self._save_label(result_data, p, convert_ext=convert_ext)

                    offset += progress_amount
                    self.signal_update_progress.emit(round(offset))

                if convert_object:
                    self._save_label(convert_object, outpath, label_paths)

        except Exception as e:
            self.signal_start_or_stop_convert.emit(False, traceback.format_exc())
        else:
            self.signal_start_or_stop_convert.emit(False, "")

    @staticmethod
    def _convert_dataset(idx:int, label_path:str, input_label_type:str, convert_label_type:str, convert_object:object):
        BACKGROUND_LABEL = 0
        LINE_DETAIL_EPSILON = 0.0005  # small
        # LINE_DETAIL_EPSILON = 0.0003  # medium
        # LINE_DETAIL_EPSILON = 0.0002  # large
        combine = False

        if input_label_type == "voc":
            label_object = VocDataSet()
            return
        elif input_label_type == "ade20k":
            label_object = Ade20kDataSet()
            return
        elif input_label_type == "coco":
            label_object = CocoDataSet()
            return
        else:
            label_object = LabelmeDataSet()

        if convert_label_type == "voc":
            convert_object = VocDataSet()
            convert_ext = "xml"
        elif convert_label_type == "ade20k":
            convert_object = Ade20kDataSet()
            convert_ext = "png"
            return
        elif convert_label_type == "coco":
            if convert_object is None:
                convert_object = CocoDataSet()
            combine= True
            convert_ext = "json"
        else:
            convert_object = LabelmeDataSet()
            convert_ext = "json"

        label_object.load_label_from_file(label_path)

        convert_object = label_object.convert_dataset_by_convert_type(
            convert_object, convert_label_type, idx= idx
        )

        if combine:
            return convert_object, convert_ext, convert_object
        else:
            return convert_object, convert_ext, None

    @staticmethod
    def _save_label(result_data, label_path, convert_ext='json', file_paths=[]):
        if os.path.isdir(label_path):
            label_path = label_path
        else:
            label_path = ".".join(label_path.split(".")[:-1]) + f".{convert_ext}"

        result_data.save(label_path)
