import os, sys
from qgis.core import QgsProject, QgsApplication, QgsVectorLayer, QgsRasterLayer
from qgis.gui import QgsMapCanvas, QgsMapToolPan, QgsMapToolZoom, QgsMapToolIdentify
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Dlg_clip import Ui_Dialog as Dlg_clip_class
import gdal
import numpy as np
import cv2


class Func_clip_class(QDialog, Dlg_clip_class):
    mySignal = pyqtSignal(int)

    def __init__(self, layers):
        super(Func_clip_class, self).__init__()
        self.setupUi(self)
        self.success = False
        self.show()

        # 对图层进行处理，处理成cv的numpy数组
        self.bandName = []
        self.bands = []
        self.projections = []
        self.geoTransform = []
        self.layers = []
        self.bandcount = []
        self.index = 0

        for i in range(0, len(layers)):
            self.layers.append(layers[i])
            tempCount = layers[i].bandCount()
            self.bandcount.append(tempCount)
            tempName = layers[i].name()
            tempDs = gdal.Open(layers[i].source())
            for j in range(1, tempCount + 1):
                self.bandName.append(tempName + '@' + str(j))
                tempband = np.array(tempDs.GetRasterBand(j).ReadAsArray())
                self.bands.append(tempband)
                self.projections.append(tempDs.GetProjection())
                self.geoTransform.append(tempDs.GetGeoTransform())

        for i in range(0, len(layers)):
            tempName = layers[i].name()
            self.comboBox_selectlayer.addItem(tempName)

        self.init_mapcanvas()
        self.loadMap2(layers[0])
        self.pushButton.clicked.connect(self.action)
        self.pushButton_show.clicked.connect(self.action_show_clicked)
        self.comboBox_selectlayer.currentIndexChanged.connect(self.action_comboBox_changed)

    def action_comboBox_changed(self):
        self.index = self.comboBox_selectlayer.currentIndex()
        print("currnetIndex")
        print(self.index)
        self.loadMap2(layer=self.layers[self.index])

    def action(self):
        self.Func_clip_process()
        print("OK")
        if self.checkBox.isChecked():
            self.result = QgsRasterLayer(self.path, "result_clip")
            self.mySignal.emit(1)
        self.close()

    def action_show_clicked(self):
        print("show")

        y0 = int(self.plainTextEdit_y0.toPlainText())
        y1 = int(self.plainTextEdit_y1.toPlainText())
        x0 = int(self.plainTextEdit_x0.toPlainText())
        x1 = int(self.plainTextEdit_x1.toPlainText())

        if not any([y0, y1, x0, x1]):
            print("Height or Width setValue error!")
        else:
            print(x0, x1, y0, y1)

            bandName = []
            bands = []
            projections = []
            geoTransform = []

            layers = self.layers
            print("layers: {0}".format(layers))
            index = self.index
            print("index:{0}".format(self.index))
            Count = layers[index].bandCount()
            print("the layer band count:{0}".format(Count))
            Name = layers[index].name()
            Ds = gdal.Open(layers[index].source())
            for j in range(1, Count + 1):
                bandName.append(Name + '@' + str(j))
                band = np.array(Ds.GetRasterBand(j).ReadAsArray())
                bands.append(band)
                projections.append(Ds.GetProjection())
                geoTransform.append(Ds.GetGeoTransform())
            print(bands)

            if self.bandcount[self.index] == 1:
                img1 = cv2.merge([bands[0]])
                print("shape:{0}".format(img1.shape))
                cropped1 = img1[y0:y1, x0:x1]
                cv2.imshow('img1', cropped1)
            else:
                img2 = cv2.merge([bands[0], bands[1], bands[2]])
                print("shape:{0}".format(img2.shape))
                cropped2 = img2[y0:y1, x0:x1]
                cv2.imshow('img2', cropped2)

    def Func_clip_process(self):
        print("This is func_clip, process starts now.")

        y0 = int(self.plainTextEdit_y0.toPlainText())
        y1 = int(self.plainTextEdit_y1.toPlainText())
        x0 = int(self.plainTextEdit_x0.toPlainText())
        x1 = int(self.plainTextEdit_x1.toPlainText())

        if not any([y0, y1, x0, x1]):
            print("Height or Width setValue error!")
        else:
            print(x0, x1, y0, y1)

            bandName = []
            bands = []
            projections = []
            geoTransform = []

            layers = self.layers
            print("layers: {0}".format(layers))
            index = self.index
            print("index:{0}".format(self.index))
            Count = layers[index].bandCount()
            print("the layer band count:{0}".format(Count))
            Name = layers[index].name()
            Ds = gdal.Open(layers[index].source())
            for j in range(1, Count + 1):
                bandName.append(Name + '@' + str(j))
                band = np.array(Ds.GetRasterBand(j).ReadAsArray())
                bands.append(band)
                projections.append(Ds.GetProjection())
                geoTransform.append(Ds.GetGeoTransform())
            print(bands)

            if self.bandcount[self.index] == 1:
                img1 = cv2.merge([bands[0]])
                print("shape:{0}".format(img1.shape))
                cropped1 = img1[y0:y1, x0:x1]
                # cv2.imshow('img1', img1)
                path = "processImage/result_clip1.tif"
                cv2.imwrite(path, cropped1)
                print("img1 ouput success")
                # self.result = QgsRasterLayer(path, "result_clip")
                self.path = path
            else:
                img2 = cv2.merge([bands[0], bands[1], bands[2]])
                print("shape:{0}".format(img2.shape))
                cropped2 = img2[y0:y1, x0:x1]
                # cv2.imshow('crp',cropped)
                # cv2.imshow('img2', img2)
                path = "processImage/result_clip2.tif"
                self.create_tiff(path, projections[0], geoTransform[0], cropped2)
                print("img2 ouput success")
                # self.result = QgsRasterLayer(path, "result_clip")
                self.path = path

    def create_tiff(self, fullPath, projection, geoTransform, data):
        driver = gdal.GetDriverByName("GTiff")
        if 'int8' in data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32
        outDs = driver.Create(fullPath, data.shape[1], data.shape[0], data.shape[2], datatype)
        outDs.SetGeoTransform(geoTransform)
        outDs.SetProjection(projection)
        outDs.GetRasterBand(1).WriteArray(data[:, :, 2])
        outDs.GetRasterBand(2).WriteArray(data[:, :, 1])
        outDs.GetRasterBand(3).WriteArray(data[:, :, 0])
        del outDs

    # 画布初始化
    def init_mapcanvas(self):
        # 实例化地图画布
        self.mapCanvas = QgsMapCanvas()
        self.mapCanvas.setCanvasColor(Qt.white)
        # self.mapCanvas.show()
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.mapCanvas)

    # 文件操作
    def loadMap2(self, layer):
        print("loadMap2")
        # 打开栅格图层
        self.layer = layer
        # 注册图层
        QgsProject.instance().addMapLayer(self.layer)
        self.mapCanvas.setLayers([self.layer])
        # 设置图层范围
        self.mapCanvas.setExtent(self.layer.extent())
        self.mapCanvas.refresh()


def main():
    # 实例化 QGIS 应用对象
    qgs = QgsApplication([], True)
    qgs.setPrefixPath('qgis', True)
    # 启动 QGIS
    qgs.initQgis()

    layers = []
    layers.append(QgsRasterLayer("./Image/1.tif", "1"))
    layers.append(QgsRasterLayer("./Image/2.tif", "2"))
    window = Func_clip_class(layers)
    # window.exec_()

    exit_code = qgs.exec_()
    # 退出 QGIS
    qgs.exitQgis()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
