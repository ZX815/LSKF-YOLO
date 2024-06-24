import cv2 as cv
import os

path = os.getcwd()  # 获取代码所在目录
tif_list = [x for x in os.listdir(path) if x.endswith(".tif")]  # 获取目录中所有tif格式图像列表
for num, i in enumerate(tif_list):  # 遍历列表
    img = cv.imread(i, -1)  # 读取列表中的tif图像
    cv.imwrite(i.split('.')[0] + ".jpg", img)  # tif 格式转 jpg 并按原名称命名