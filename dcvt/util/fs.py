from typing import List

import json
import chardet
import os
import xml.etree.ElementTree as ET


class DcvtFileManager:

    @staticmethod
    def find_label_id_by_name(label_name:str, labelmap:List[dict]) -> int:
        for label in labelmap:
            if label['name'] == label_name:
                return label['id']
        return 0

    @staticmethod
    def find_label_name_by_id(label_id:int, labelmap:List[dict]) -> str:
        for label in labelmap:
            if label['id'] == label_id:
                return label['name']
        return ''

    @staticmethod
    def _find_character_set(raw: bytes) -> str:
        return chardet.detect(raw)["encoding"]

    @staticmethod
    def load_from_xml(path: str):
        return ET.parse(path).getroot()

    @staticmethod
    def load_from_json(path: str):
        return json.loads(path)

    @staticmethod
    def save_json(data: dict, out_path: str) -> None:
        with open(out_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def get_parents_dir(path: str) -> str:
        parent_dir_path = os.path.dirname(path)
        parent_dir = parent_dir_path.split("/")[-1]
        return parent_dir

    @staticmethod
    def get_filename(path: str) -> str:
        return os.path.basename(path)

    def open_file_as_str(self, path: str, force_convert: bool = True):
        with open(path, "rb") as f:
            buf = f.read()
            encodings_name = self._find_character_set(buf)
            if encodings_name not in ["cp-949", "utf-8", "euc-kr"]:
                print(f"WARNING.. {encodings_name} might result in an Error... ")
                if force_convert:
                    print(f'Convert encodings.. {encodings_name} -> "utf-8"')
                    encodings_name = "utf-8"
            return buf.decode(encodings_name)
