from typing import List
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom
import xml.etree.ElementTree as ET

from dcvt.util import DcvtFileManager

fs = DcvtFileManager()


class VocSource:
    def __init__(self, database="Unknown"):
        self.database: str = database

    def set_database(self, database: str):
        self.database = database
        return self

    def xml_dump(self) -> Element:
        voc_source = Element("source")
        SubElement(voc_source, "database").text = self.database
        return voc_source


class VocSize:
    def __init__(self):
        self.width: int = 0
        self.height: int = 0
        self.depth: int = 3

    def set_voc_size(self, width: int, height: int, depth: int = 3):
        self.width: int = width
        self.height: int = height
        self.depth: int = depth
        return self

    def xml_dump(self) -> Element:
        voc_size = Element("size")
        SubElement(voc_size, "width").text = str(self.width)
        SubElement(voc_size, "height").text = str(self.height)
        SubElement(voc_size, "depth").text = str(self.depth)
        return voc_size


class VocObject:
    def __init__(
        self,
        name: str,
        pose: str = "Unspecified",
        truncated: int = 0,
        difficult: int = 0,
    ):
        self.name: str = name
        self.pose: str = pose
        self.truncated: int = truncated
        self.difficult: int = difficult
        self.bndbox: VocBndbox

    def set_bnd_box(self, xmin: int, ymin: int, xmax: int, ymax: int):
        self.bndbox = VocBndbox(xmin, ymin, xmax, ymax)
        return self

    def xml_dump(self) -> Element:
        voc_object = Element("object")
        SubElement(voc_object, "name").text = self.name
        SubElement(voc_object, "pose").text = self.pose
        SubElement(voc_object, "truncated").text = str(self.truncated)
        SubElement(voc_object, "difficult").text = str(self.difficult)
        voc_object.append(self.bndbox.xml_dump())
        return voc_object


class VocBndbox:
    def __init__(self, xmin: int, ymin: int, xmax: int, ymax: int):
        self.xmin: int = xmin
        self.ymin: int = ymin
        self.xmax: int = xmax
        self.ymax: int = ymax

    def xml_dump(self) -> Element:
        voc_bndbox = Element("bndbox")
        SubElement(voc_bndbox, "xmin").text = str(self.xmin)
        SubElement(voc_bndbox, "ymin").text = str(self.ymin)
        SubElement(voc_bndbox, "xmax").text = str(self.xmax)
        SubElement(voc_bndbox, "ymax").text = str(self.ymax)
        return voc_bndbox


class VocDataSet:
    def __init__(self):
        self.folder: str = None
        self.filename: str = None
        self.path: str = None
        self.source: VocSource = VocSource()
        self.size: VocSize = VocSize()
        self.segmented: int = 0
        self.object: List[VocObject] = []

    def convert_dataset_by_convert_type(self, convert_label_type: str):
        if convert_label_type == "labelme":
            pass
        elif convert_label_type == "ade20k":
            pass
        elif convert_label_type == "coco":
            pass

    def load_label_from_file(self, label_path: str) -> None:
        label_xml = fs.load_from_xml(label_path)

        for i in label_xml:
            if i.tag == "folder":
                self.folder = i.text
            elif i.tag == "filename":
                self.filename = i.text
            elif i.tag == "path":
                self.path = i.text
            elif i.tag == "source":
                self.set_source(i.text)
            elif i.tag == "size":
                self.set_size_by_et(i)
            elif i.tag == "segmented":
                self.segmented = int(i.text)
            elif i.tag == "object":
                self.set_object_by_et(i)

    def set_voc_data(self, folder: str, filename: str, path: str, seg: int = 0):
        self.folder: str = folder
        self.filename: str = filename
        self.path: str = path
        self.segmented: int = seg

    def set_source(self, database):
        self.source = self.source.set_database(database)

    def set_size(self, width: int, height: int, depth: int = 3) -> None:
        self.size = self.size.set_voc_size(width, height, depth)

    def add_object(
        self,
        name: str,
        xmin: int,
        ymin: int,
        xmax: int,
        ymax: int,
        pose: str = "Unspecified",
        trun: int = 0,
        diff: int = 0,
    ) -> None:
        vocObj = VocObject(name, pose, trun, diff)
        vocObj.set_bnd_box(xmin, ymin, xmax, ymax)
        self.object.append(vocObj)

    def set_size_by_et(self, object: Element) -> None:
        width = 0
        height = 0
        depth = 3

        for i in object:
            if i.tag == "width":
                width = int(i.text)
            elif i.tag == "height":
                height = int(i.text)
            elif i.tag == "depth":
                depth = int(i.text)

        self.set_size(width, height, depth)

    def get_bndbox_by_et(self, object: Element):
        xmin = 0
        ymin = 0
        xmax = 0
        ymax = 0

        for i in object:
            if i.tag == "xmin":
                xmin = int(i.text)
            elif i.tag == "ymin":
                ymin = int(i.text)
            elif i.tag == "xmax":
                xmax = int(i.text)
            elif i.tag == "ymax":
                ymax = int(i.text)

        return xmin, ymin, xmax, ymax

    def set_object_by_et(self, object: Element):
        name = ""
        pose = "Unspecified"
        trunc = 0
        diffic = 0
        xmin = 0
        ymin = 0
        xmax = 0
        ymax = 0

        for i in object:
            if i.tag == "name":
                name = i.text
            elif i.tag == "pose":
                pose = i.text
            elif i.tag == "truncated":
                trunc = int(i.text)
            elif i.tag == "difficult":
                diffic = int(i.text)
            elif i.tag == "bndbox":
                xmin, ymin, xmax, ymax = self.get_bndbox_by_et(i)

        self.add_object(name, xmin, ymin, xmax, ymax, pose, trunc, diffic)

    def save(self, output_path: str) -> None:
        voc_dataset = Element("annotation")
        SubElement(voc_dataset, "folder").text = self.folder
        SubElement(voc_dataset, "filename").text = self.filename
        SubElement(voc_dataset, "path").text = self.path
        source = self.source.xml_dump()
        voc_dataset.append(source)
        size = self.size.xml_dump()
        voc_dataset.append(size)
        SubElement(voc_dataset, "segmented").text = str(self.segmented)
        for obj in self.object:
            voc_dataset.append(obj.xml_dump())

        voc_xml = minidom.parseString(ET.tostring(voc_dataset)).toprettyxml(
            indent="    "
        )

        with open(output_path, "w") as f:
            f.write(voc_xml)
