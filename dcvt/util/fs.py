import json
from xml.etree.ElementTree import Element, dump, parse
from xml.dom import minidom
import xml.etree.ElementTree as ET

from dcvt.dataset.voc.Voc import VocDataSet


class DcvtFileManager:
    def save_json(self, data: dict, out_path: str) -> None:
        with open(out_path, "w") as f:
            json.dumps(data, f, ensure_ascii=False)

    def save_xml_by_voc(self, data: VocDataSet, out_path: str) -> None:
        voc_data = data.voc_dump()
        voc_xml = minidom.parseString(ET.tostring(voc_data)).toprettyxml(indent="  ")

        with open(out_path, "w") as f:
            f.write(voc_xml)
