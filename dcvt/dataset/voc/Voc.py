from typing import List
from xml.etree.ElementTree import Element, SubElement, dump, parse


class VocSource:
    def __int__(self, database="Unknown"):
        self.database: str = database

    def xml_dump(self) -> Element:
        voc_source = Element("source")
        SubElement(voc_source, "database").text = self.database
        return voc_source


class VocSize:
    def __int__(self, width: int, height: int, depth: int = 3):
        self.width: int = width
        self.height: int = height
        self.depth: int = depth

    def xml_dump(self) -> Element:
        voc_size = Element("size")
        SubElement(voc_size, "width").text = self.width
        SubElement(voc_size, "height").text = self.height
        SubElement(voc_size, "depth").text = self.depth
        return voc_size


class VocObject:
    def __int__(
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

    def set_bnd_box(self, xmin: int, ymin: int, xmax: int, ymax: int) -> None:
        self.bndbox = VocBndbox(xmin, ymin, xmax, ymax)

    def xml_dump(self) -> Element:
        voc_object = Element("object")
        SubElement(voc_object, "name").text = self.name
        SubElement(voc_object, "pose").text = self.pose
        SubElement(voc_object, "truncated").text = self.truncated
        SubElement(voc_object, "difficult").text = self.difficult
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
        SubElement(voc_bndbox, "xmin").text = self.xmin
        SubElement(voc_bndbox, "ymin").text = self.ymin
        SubElement(voc_bndbox, "xmax").text = self.xmax
        SubElement(voc_bndbox, "ymax").text = self.ymax
        return voc_bndbox


class VocDataSet:
    def __init__(
        self,
        folder: str,
        filename: str,
        path: str,
        seg: int = 0,
    ):
        self.folder: str = folder
        self.filename: str = filename
        self.path: str = path
        self.source: VocSource = VocSource()
        self.size: VocSize
        self.segmented: int = seg
        self.object: List[VocObject] = []

    def set_source(self, database) -> None:
        self.source = VocSource(database)

    def set_size(self, width: int, height: int, depth: int = 3):
        self.size = VocSize(width, height, depth)

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

    def voc_dump(self) -> Element:
        voc_dataset = Element("annotation")
        SubElement(voc_dataset, "folder").text = self.folder
        SubElement(voc_dataset, "filename").text = self.filename
        SubElement(voc_dataset, "path").text = self.path
        source = self.source.xml_dump()
        voc_dataset.append(source)
        size = self.size.xml_dump()
        voc_dataset.append(size)
        SubElement(voc_dataset, "segmented").text = self.segmented
        for obj in self.object:
            voc_dataset.append(obj.xml_dump())

        return voc_dataset