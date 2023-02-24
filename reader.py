import os
import sys
import time

import numpy as np
import matplotlib.pyplot as plt
from struct import unpack

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.file_name = -1
        self.resize(500, 500)
        self.setWindowTitle("bmp图像显示")
        self.init_ui()
    def init_ui(self):
        container = QVBoxLayout() #最外层盒子 垂直布局
        self.label = QLabel(self)
        self.label.setText('请首先上传图片(目前仅支持24位真彩色bmp图像)')
        btn = QPushButton("上传图片")
        btn.setFixedHeight(100)
        btn.clicked.connect(self.getFile)
        btn2 = QPushButton("逐行显示")
        btn2.setFixedHeight(100)
        btn2.clicked.connect(self.showImg)
        btn3 = QPushButton("灰度化显示")
        btn3.clicked.connect(self.transImg)
        btn3.setFixedHeight(100)
        container.addWidget(self.label)
        container.addWidget(btn)
        container.addWidget(btn2)
        container.addWidget(btn3)
        self.setLayout(container)

    def getFile(self, args):
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(None, "lll", os.getcwd(),"BMP Image(*.bmp);;All Files(*)")
        if not filename.endswith("bmp"):
            return
        self.file_name = filename
        self.label.setText('图像路径：%s \n请选择 逐行显示 或 灰度化显示\n注：需关闭图像窗口才可选择下个操作' % filename)

    #逐行显示
    def showImg(self, args):
        if self.file_name == -1:
            return
        img=open(self.file_name,"rb")
        img.seek(10) #移动指针到10字节处
        #从开头到图片数据要的字节数
        img_bias=unpack("<i",img.read(4))[0]
        print(img_bias)
        img.seek(18)
        #获取图像宽度和长度
        width = unpack("<i",img.read(4))[0]
        height = unpack("<i", img.read(4))[0]
        #创建储存数组
        img_np=np.zeros((height,width,3),dtype=int)
        #num=0#计算读入的总字节数
        #数据排列从左到右，从下到上

        # for y in range(height):
        #     for x in range(width):
        #         # num+=3
        #         G=unpack("B", img.read(1))[0]
        #         B=unpack("B", img.read(1))[0]
        #         R=unpack("B", img.read(1))[0]
        #         img_np[height - y - 1][x]=[R,B,G]
        #     if y % 8 == 0 or y == height - 1:
        #         plt.cla()
        #         plt.imshow(img_np)
        #         plt.pause(0.1)
        #计算需要跳过的字节数
        padding = 4 - (3 * width) % 4
        if padding == 4 :   #如果能整除4，则不跳过
            padding = 0
        #从最后一行开始遍历
        for y in range(height):
            img.seek(img_bias + (3 * width + padding) * (height - 1 - y))  #从下到上去到每行开头
            for x in range(width):
                G=unpack("B", img.read(1))[0]   #读取G分量
                B=unpack("B", img.read(1))[0]   #读取B分量
                R=unpack("B", img.read(1))[0]   #读取R分量
                img_np[y][x]=[R,B,G]
            if (y + 1) % 8 == 0:
                plt.cla()
                plt.imshow(img_np)
                plt.pause(0.1)  #每0.1s刷新8行
        plt.imshow(img_np)
        plt.show()
        img.close()

    # 灰度化
    def transImg(self, args):
        if self.file_name == -1:
            return
        img = open(self.file_name, "rb")
        img.seek(10)
        # 从开头到图片数据要的字节数
        img_bias = unpack("<i", img.read(4))[0]
        print(img_bias)
        img.seek(18)
        #获取图像宽度和长度
        width = unpack("<i", img.read(4))[0]
        height = unpack("<i", img.read(4))[0]
        # 将数据存入numpy中
        img.seek(img_bias)
        img_np = np.zeros((height, width, 3), dtype=int)
        # 数据排列从左到右，从下到上
        padding = 4 - (3 * width) % 4
        if padding == 4 :
            padding = 0
        for y in range(height):
            img.seek(img_bias + (3 * width + padding) * (height - 1 - y))
            for x in range(width):
                G = unpack("B", img.read(1))[0]  #读取G分量
                B = unpack("B", img.read(1))[0]   #读取B分量
                R = unpack("B", img.read(1))[0] #读取R分量
                img_np[y][x] = [0.3 * R + 0.59 * G + 0.11 * B]  #根据权重计算灰度
        plt.imshow(img_np)  #显示图像
        plt.show()
        img.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    app.exec()  #循环执行
