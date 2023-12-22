import math
import cv2
import numpy as np

from minicv.Colors import Colors


class Image:
    def __init__(self, image: cv2.Mat) -> None:
        self.data = image

    def getWidth(self):
        return self.data.shape[1]

    def getHeight(self):
        return self.data.shape[0]

    def saveTo(self, path: str):
        Images.save(self.data, str)

    def pixel(self, x: int, y: int):
        """pixel 返回图片image在点(x, y)处的像素的ARGB值

        该值的格式为0xAARRGGBB,是一个"32位整数"

        Args:
            x (int): 横坐标
            y (int): 纵坐标
        """
        b, g, r = self.data[y, x]
        return "#{:02x}{:02x}{:02x}".format(r, g, b)


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x  # 横坐标
        self.y = y  # 纵坐标


class Images:
    def read(path: str, flag=0):
        """
        read 读取图像

        Args:
            path (str): 图像路径
            flag (int) :
                - 0 (默认) 返回Mat格式图像
                - 1 返回Image对象

        Returns:
            opencv格式图像 (np.array):
        """
        matData = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
        return matData if flag == 0 else Image(matData)

    def save(img: cv2.Mat | Image, path="save.png"):
        """
        save 保存图像到路径

        Args:
            img (mat): opencv格式图像
            path (str): 路径 默认保存到当前路径下save.png
        """
        imgData = img.data if isinstance(img, Image) else img
        cv2.imencode(ext=".png", img=imgData)[1].tofile(path)

    def getPixel(img: cv2.Mat | Image, x, y):
        """
        getPixel 返回图片image在点(x, y)处的像素的RGB值。

        Args:
            img (Mat): opencv图像
            x (int): 横坐标
            y (int): 纵坐标

        Returns:
            坐标颜色值 (str):
        """
        imgData = img.data if isinstance(img, Image) else img
        b, g, r = imgData[y, x]
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def findColor(img: cv2.Mat | Image, color, region=None, threshold=4):
        """
        findColor 找色功能

        Args:
            img (mat): opencv格式图像
            color (str): 颜色值字符串
            region (list, optional): [xmin,ymin,xmax,ymax]. Defaults to None.
            threshold (int, optional): 颜色相似度. Defaults to 4.

        Returns:
            x (int):
            y (int):
        """
        imgData = img.data if isinstance(img, Image) else img
        x_min, y_min, x_max, y_max = region or (
            0,
            0,
            imgData.shape[1],
            imgData.shape[0],
        )
        imgData = imgData[y_min:y_max, x_min:x_max]
        # 将颜色值转换为 RGB 分量值
        r, g, b = np.array([int(color[i : i + 2], 16) for i in (1, 3, 5)])
        # 计算颜色差
        diff = np.abs(imgData - [b, g, r])
        # 判断颜色是否匹配
        match = np.logical_and.reduce(diff <= threshold, axis=2)
        # 获取匹配像素点的坐标
        y, x = np.where(match)
        if len(x) == 0:
            return None
        else:
            return x[0] + x_min, y[0] + y_min

    def findAllColor(img: cv2.Mat | Image, color, region=None, threshold=4):
        """
        findAllColor 找到全图中所有符合要求的像素点

        Args:
            img (mat): opencv格式图像
            color (str): 颜色值字符串
            region (list, optional): [xmin,ymin,xmax,ymax]. Defaults to None.
            threshold (int, optional): 颜色相似度. Defaults to 4.

        Returns:
            颜色值所有点 (list): [(x,y),(x,y),(x,y)]
        """
        imgData = img.data if isinstance(img, Image) else img
        x_min, y_min, x_max, y_max = region or (
            0,
            0,
            imgData.shape[1],
            imgData.shape[0],
        )
        imgData = imgData[y_min:y_max, x_min:x_max]
        # 将颜色值转换为 RGB 分量值
        r, g, b = np.array([int(color[i : i + 2], 16) for i in (1, 3, 5)])
        # 计算颜色差
        diff = np.abs(imgData - [b, g, r])
        # 判断颜色是否匹配
        match = np.logical_and.reduce(diff <= threshold, axis=2)
        # 获取匹配像素点的坐标
        y, x = np.where(match)
        if len(x) == 0:
            return None
        else:
            return[(x[i] + x_min, y[i] + y_min) for i in range(len(x))]
        

    def findMultiColors(
        img: cv2.Mat | Image, firstColor, colors, region=None, threshold=4
    ):
        """
        findMultiColors 多点找色

        Args:
            img (mat): opencv格式图像
            firstColor (str): 第一个图像的颜色值
            colors (list): [(x,y,color),(x,y,color)] x为相对第一个点偏移的坐标值,color为颜色值"#112233"
            region (list, optional): 范围数组[xmin,ymin,xmax,ymax]. Defaults to None.
            threshold (int, optional): 相似度. Defaults to 4.

        Returns:
            x (int): 第一个点的横坐标
            y (int): 第一个点的纵坐标

        """
        imgData = img.data if isinstance(img, Image) else img
        firstColorPoints = Images.findAllColor(
            imgData, firstColor, region=region, threshold=threshold
        )
        if firstColorPoints is None:
            return None
        for x0, y0 in firstColorPoints:
            for x, y, target_color in colors:
                if not Colors.isSimilar(
                    Colors.parseColor(target_color),
                    Colors.parseColor(Images.getPixel(imgData, x + x0, y + y0)),
                    threshold=threshold,
                ):
                    break
            return x0, y0
        return None

    def findImage(
        img: cv2.Mat | Image, template, threshold=0.8, region=None, level=None
    ):
        """
        findImage 模板匹配

        Args:
            - img (mat): opencv格式图像
            - template (mat): opencv格式图像
            - threshold (float, optional): 匹配度. Defaults to 0.8.
            - region (list, optional): 范围[xmin,ymin,xmax,ymax]. Defaults to None.
            - level (int, optional): 图像金字塔等级.

        Returns:
            - max_loc (list): xmin,ymin,xmax,ymax
        """
        # 设置查找区域
        imgData = img.data if isinstance(img, Image) else img
        templateData = template.data if isinstance(template, Image) else template
        x_min, y_min, x_max, y_max = region or (
            0,
            0,
            imgData.shape[1],
            imgData.shape[0],
        )
        imgData = imgData[y_min:y_max, x_min:x_max]
        if level is None:
            level =  select_pyramid_level(imgData, templateData)
        imgData = Images.grayscale(imgData)
        templateData = Images.grayscale(templateData)

        img_array = [imgData]
        template_array = [templateData]
        for i in range(level):
            imgData = cv2.pyrDown(imgData)
            templateData = cv2.pyrDown(templateData)
            img_array.append(imgData)
            template_array.append(templateData)

        for i, img_level, template_level in list(
            zip(range(level + 1), img_array, template_array)
        )[::-1]:
            # 匹配模板图像
            res = cv2.matchTemplate(img_level, template_level, cv2.TM_CCOEFF_NORMED)
            # 选择相似度最高的一个结果
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val > threshold:
                # 转换坐标系
                max_loc = (max_loc[0] * (2**i), max_loc[1] * (2**i))
                if region is not None:
                    max_loc = (max_loc[0] + x_min, max_loc[1] + y_min)
                return [
                    max_loc[0],
                    max_loc[1],
                    max_loc[0] + template_array[0].shape[1],
                    max_loc[1] + template_array[0].shape[0],
                ]
        return None

    def bytes2opencv(data) -> cv2.Mat:
        """bytes to opencv

        Args:
            data (byte): bytes

        Returns:
            opencv格式图像 (np.array):
        """
        return cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)

    def bytes2image(data) -> Image:
        return Image(Images.bytes2opencv(data))

    def grayscale(img: cv2.Mat | Image) -> cv2.Mat:
        imgData = img.data if isinstance(img, Image) else img
        # 如果图像已经是灰度图像，则直接返回
        if imgData.ndim == 2 or (imgData.ndim == 3 and imgData.shape[2] == 1):
            return imgData
        # 将彩色图像转换为灰度图像
        return cv2.cvtColor(imgData, cv2.COLOR_BGR2GRAY)
        


def select_pyramid_level(img, template):
    min_dim = min(img.shape[0], img.shape[1], template.shape[0], template.shape[1])
    if min_dim < 32:
        return 0
    max_level = int(math.log2(min_dim // 16))
    return min(6, max_level)
