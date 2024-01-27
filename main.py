import time
import cv2
import numpy as np
import cProfile
from minicv import Image, Images


test = Images.read("QQ截图20240127231912.png", 1)


def func():
    result = Images.findMultiColors(
        test,
        "#286256",
        [[6, 0, "#e5c077"], [10, 1, "#c77e34"], [10, 5, "#c77e34"], [5, 5, "#e5c07b"]],
        threshold=4,
        region=[429, 244, 655, 338],
    )
    print(result)


cProfile.run("func()")
