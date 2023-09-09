# MiniCV
高性能轻量化图色库

详细文档？没有，见autojs图色文档即可，结合源代码看看吧，后续补上(~~画饼~~)

### Feature：
- 找图 
findImage(img: cv2.Mat | Image, template, threshold=0.8, region=None, level=None)
- 多点找色
findMultiColors(img: cv2.Mat | Image, firstColor, colors, region=None, threshold=4)