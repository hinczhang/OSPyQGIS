import os, sys
from qgis.core import QgsProject, QgsApplication, QgsVectorLayer, QgsRasterLayer
from qgis.gui import QgsMapCanvas, QgsMapToolPan, QgsMapToolZoom, QgsMapToolIdentify
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Dlg_cornerDetection import Ui_Dialog as Dlg_cornerdetection_class
import gdal
import numpy as np
import cv2
import matplotlib

matplotlib.use("Qt5Agg")  # 声明使用QT5
import matplotlib.pyplot as plt


class Func_cornerdetection_class(QDialog, Dlg_cornerdetection_class):
    mySignal = pyqtSignal(int)

    def __init__(self, layers):
        super(Func_cornerdetection_class, self).__init__()
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
        self.index2 = 0

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

        self.comboBox_selectmethod.addItem("Harris")
        self.comboBox_selectmethod.addItem("Shi-Tomasi")
        self.comboBox_selectmethod.addItem("SIFT")
        self.comboBox_selectmethod.addItem("SURF")

        self.init_mapcanvas()
        self.loadMap2(layers[0])
        self.comboBox_selectlayer.currentIndexChanged.connect(self.action_comboBoxLayer_changed)
        self.comboBox_selectmethod.currentIndexChanged.connect(self.action_comboBoxMethod_changed)
        self.pushButton_process.clicked.connect(self.action_process_clicked)
        self.pushButton_show.clicked.connect(self.Func_cornerdetection_show)

    def action_comboBoxLayer_changed(self):
        self.index = self.comboBox_selectlayer.currentIndex()
        print("currnet layer Index:{0}".format(self.index))
        self.loadMap2(layer=self.layers[self.index])

    def action_comboBoxMethod_changed(self):
        self.index2 = self.comboBox_selectmethod.currentIndex()
        print("currnet method Index:{0}".format(self.index2))
        if self.index2 == 0:
            self.plainTextEdit_coef_1.setPlainText("2")
            self.plainTextEdit_coef_2.setPlainText("3")
            self.plainTextEdit_coef_3.setPlainText("0.04")
            self.label_coef_1.setText("blockSize")
            self.label_coef_2.setText("ksize")
            self.label_coef_3.setText("k")
        elif self.index2 == 1:
            self.plainTextEdit_coef_1.setPlainText("25")
            self.plainTextEdit_coef_2.setPlainText("10")
            self.plainTextEdit_coef_3.setPlainText("0.01")
            self.label_coef_1.setText("maxCorners")
            self.label_coef_2.setText("minDistance")
            self.label_coef_3.setText("qualityLevel")
        else:
            self.plainTextEdit_coef_1.setPlainText("")
            self.plainTextEdit_coef_2.setPlainText("")
            self.plainTextEdit_coef_3.setPlainText("")
            self.label_coef_1.setText("coef1")
            self.label_coef_2.setText("coef2")
            self.label_coef_3.setText("coef3")
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "Cannot use cv2.SIFT, your opencv-python is free version.")
            msg_box.exec_()

    def action_process_clicked(self):
        self.Func_cornerdetection_process()
        print("OK")
        if self.checkBox.isChecked():
            self.result = QgsRasterLayer(self.path, "result_cd")
            self.mySignal.emit(1)
        self.close()

    def Func_cornerdetection_show(self):
        print("show detection result")

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

        coef1 = int(self.plainTextEdit_coef_1.toPlainText())
        coef2 = int(self.plainTextEdit_coef_2.toPlainText())
        coef3 = float(self.plainTextEdit_coef_3.toPlainText())
        print("coefs of corner detection are:{0},{1},{2}".format(coef1, coef2, coef3))

        if self.bandcount[self.index] == 1:
            tempband = cv2.convertScaleAbs(bands[0], alpha=0.003891)
            img = cv2.merge([tempband, tempband, tempband])
        else:
            img = cv2.merge([bands[0], bands[1], bands[2]])

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        method = self.comboBox_selectmethod.currentIndex()
        if method == 0:
            print("method: Harris")
            gray = np.float32(gray)
            # dst = cv2.cornerHarris(gray, 2, 3, 0.04)
            dst = cv2.cornerHarris(gray, coef1, coef2, coef3)
            dst = cv2.dilate(dst, None)
            img[dst > 0.01 * dst.max()] = (0, 0, 255)
            cv2.imshow('harris', img)
            print("success")
        elif method == 1:
            print("method: Shi-Tomasi")
            # corners=cv2.goodFeaturesToTrack(gray,25,0.01,10)
            corners = cv2.goodFeaturesToTrack(gray, coef1, coef3, coef2)
            corners = np.int0(corners)
            for i in corners:
                x, y = i.ravel()
                cv2.circle(img, (x, y), 8, (0, 0, 255), -1)
            # plt.imshow(img),plt.show()
            cv2.imshow('shi-tomasi', img)
            print("success")
        elif method == 2:
            print("method: SIFT")
            print("Cannot use cv2.SIFT, your opencv-python is free version.")
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "Cannot use cv2.SIFT, your opencv-python is free version.")
            msg_box.exec_()
            # sift=cv2.SIFT()
            # kp=sift.detect(gray,None)
            # img=cv2.drawKeyPoints(gray,kp)
            # cv2.imshow('SIFT',img)
        else:
            print("method: SURF")
            print("Cannot use cv2.SURF, your opencv-python is free version.")
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "Cannot use cv2.SURF, your opencv-python is free version.")

    def Func_cornerdetection_process(self):
        print("This is func_cornerdetection, process starts now.")

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

        coef1 = int(self.plainTextEdit_coef_1.toPlainText())
        coef2 = int(self.plainTextEdit_coef_2.toPlainText())
        coef3 = float(self.plainTextEdit_coef_3.toPlainText())
        print("coefs of corner detection are:{0},{1},{2}".format(coef1, coef2, coef3))

        if self.bandcount[self.index] == 1:
            tempband = cv2.convertScaleAbs(bands[0], alpha=0.003891)
            img = cv2.merge([tempband, tempband, tempband])
        else:
            img = cv2.merge([bands[0], bands[1], bands[2]])

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        method = self.comboBox_selectmethod.currentIndex()
        if method == 0:
            print("method: Harris")
            gray = np.float32(gray)
            # dst = cv2.cornerHarris(gray, 2, 3, 0.04)
            dst = cv2.cornerHarris(gray, coef1, coef2, coef3)
            dst = cv2.dilate(dst, None)
            img[dst > 0.01 * dst.max()] = (0, 0, 255)
            # cv2.imshow('harris', img)
            print("success")
        elif method == 1:
            print("method: Shi-Tomasi")
            # corners=cv2.goodFeaturesToTrack(gray,25,0.01,10)
            corners = cv2.goodFeaturesToTrack(gray, coef1, coef3, coef2)
            corners = np.int0(corners)
            for i in corners:
                x, y = i.ravel()
                cv2.circle(img, (x, y), 8, (0, 0, 255), -1)
            # plt.imshow(img),plt.show()
            # cv2.imshow('shi-tomasi', img)
            print("success")
        elif method == 2:
            print("method: SIFT")
            print("Cannot use cv2.SIFT, your opencv-python is free version.")
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "Cannot use cv2.SIFT, your opencv-python is free version.")
            msg_box.exec_()
            # sift=cv2.SIFT()
            # kp=sift.detect(gray,None)
            # img=cv2.drawKeyPoints(gray,kp)
            # cv2.imshow('SIFT',img)
        else:
            print("method: SURF")
            print("Cannot use cv2.SURF, your opencv-python is free version.")
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "Cannot use cv2.SURF, your opencv-python is free version.")

        self.path = "processImage/result_cornerdetect.tif"
        self.create_tiff(self.path, projections[0], geoTransform[0], img)
        print("img ouput success")

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
    window = Func_cornerdetection_class(layers)
    # window.exec_()

    exit_code = qgs.exec_()
    # 退出 QGIS
    qgs.exitQgis()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
