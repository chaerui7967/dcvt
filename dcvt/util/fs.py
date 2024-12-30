import json
import chardet
from xml.etree.ElementTree import Element, dump, parse
from xml.dom import minidom
import xml.etree.ElementTree as ET

import chardet

from dcvt.dataset.voc import VocDataSet


class DcvtFileManager:
    def cal_area(self, points) -> int:
        pass

    def find_character_set(self, raw: bytes) -> str:
        return chardet.detect(raw)["encoding"]

    def open_file_as_str(self, path: str, force_convert: bool = True):
        with open(path, "rb") as f:
            buf = f.read()
            encodings_name = self.find_character_set(buf)
            if encodings_name not in ["cp-949", "utf-8", "euc-kr"]:
                print(f"WARNING.. {encodings_name} might result in an Error... ")
                if force_convert:
                    print(f'Convert encodings.. {encodings_name} -> "utf-8"')
                    encodings_name = "utf-8"
            return buf.decode(encodings_name)

    def load_from_json(self, path: str):
        return json.loads(path)

    def save_json(self, data: dict, out_path: str) -> None:
        with open(out_path, "w") as f:
            json.dumps(data, f, ensure_ascii=False)

    def save_xml_by_voc(self, data: VocDataSet, out_path: str) -> None:
        voc_data = data.voc_dump()
        voc_xml = minidom.parseString(ET.tostring(voc_data)).toprettyxml(indent="  ")

        with open(out_path, "w") as f:
            f.write(voc_xml)
