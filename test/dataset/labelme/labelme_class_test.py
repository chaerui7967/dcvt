import unittest

from dcvt.dataset.labelme.Labelme import LabelmeDataSet, LabelmeShape


class LabelmeClassTest(unittest.TestCase):
    def test_make_shape_dict(self):
        label = "a"
        a_points = [[10, 10], [20, 20]]

        label_shape = LabelmeShape(label, a_points)
        shape = label_shape.make_labelmeshape_dict()

        self.assertEqual(shape["label"], label)
        self.assertEqual(shape["points"], a_points)

    def test_make_labelme(self):
        flags = {}
        img_path = "./a.jpeg"
        img_data = None
        img_h = 100
        img_w = 200
        version = "0.0.1"
        labelObj = LabelmeDataSet(
            version, img_path, img_h, img_w, flags=flags, img_data=img_data
        )

        labels = ["a", "b"]
        points = [[[10, 10], [20, 20]], [[30, 30], [40, 40]]]

        for i in range(2):
            labelObj.set_labelmeshape(labels[i], points[i])

        self.assertIsInstance(labelObj.shapes, list)
        self.assertEqual(len(labelObj.shapes), len(points))

        labelObj_dict = labelObj.make_label_dict()

        self.assertEqual(labelObj_dict["imagePath"], img_path)
        self.assertEqual(labelObj_dict["imageHeight"], img_h)
        self.assertEqual(labelObj_dict["imageWidth"], img_w)
