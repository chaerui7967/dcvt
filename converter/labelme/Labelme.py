import json


class Labelme:
    def __init__(self):
        self.version: str
        self.flag: str
        self.shape: list
        self.imagePath: str
        self.imageHeight: str
        self.imageWidth: str
        self.imageData: str
