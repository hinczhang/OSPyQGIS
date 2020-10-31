import os, sys
import cv2
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qgis.gui import QgsMapCanvas, QgsMapToolPan, QgsMapToolZoom, QgsMapToolIdentify
from qgis.core import QgsProject, QgsApplication, QgsVectorLayer, QgsRasterLayer
from Dlg_unsupervised import Ui_Dlg_unsupervised
import gdal
import qdarkstyle

class Func_unsupervised_class(QDialog,Ui_Dlg_unsupervised):
    mySignal=pyqtSignal(int)
    # result=""

    def __init__(self,layers):
        print("init")
        super(Func_unsupervised_class,self).__init__()
        self.setupUi(self)

        # 对图层进行处理，处理成cv的numpy数组
        self.bandName = []
        self.bands = []
        self.projections = []
        self.geoTransform = []
        for i in range(0, len(layers)):
            tempCount = layers[i].bandCount()
            tempName = layers[i].name()
            tempDs = gdal.Open(layers[i].source())
            for j in range(1, tempCount + 1):
                self.bandName.append(tempName + '@' + str(j))
                tempband = np.array(tempDs.GetRasterBand(j).ReadAsArray())
                self.bands.append(tempband)
                self.projections.append(tempDs.GetProjection())
                self.geoTransform.append(tempDs.GetGeoTransform())

        # 在选项中加载波段
        self.comboBox_r.clear()
        self.comboBox_g.clear()
        self.comboBox_b.clear()
        for i in range(0, len(self.bandName)):
            self.comboBox_r.addItem(self.bandName[i], i)
            self.comboBox_g.addItem(self.bandName[i], i)
            self.comboBox_b.addItem(self.bandName[i], i)

        # print(layer)
        self.pushButton.clicked.connect(self.action)


    def action(self):
        self.Func_unsupervised_def()
        self.mySignal.emit(1)

    def Func_unsupervised_def(self):

        # 卷积
        index_b = self.comboBox_b.currentIndex()
        index_g = self.comboBox_g.currentIndex()
        index_r = self.comboBox_r.currentIndex()

        img = cv2.merge([self.bands[index_b], self.bands[index_g], self.bands[index_r]])

        max_iter = int(self.lineEdit.text()) #迭代次数
        epsilon = float(self.lineEdit_2.text()) #精确度
        K = int(self.lineEdit_3.text())  #聚类的最终数目

        Z = img.reshape((-1, 3))
        Z = np.float32(Z)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iter, epsilon)
        ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape((img.shape))

        output_1 = res2
        #cv2.imshow('res2', res2)
        cv2.imwrite('processImage/result_unsupervised.tif', output_1)
        self.result = QgsRasterLayer("processImage/result_unsupervised.tif", "result_unsupervised")
        self.close()

if __name__ == '__main__':
    qgs = QgsApplication([], True)
    qgs.setPrefixPath('qgis', True)
    # 启动QGIS
    qgs.initQgis()
    layers = []

    app = QApplication(sys.argv)
    rlayer = QgsRasterLayer("C:/Users/22814/Desktop/1.tif", "city")
    layers.append(rlayer)
    a=Func_unsupervised_class(layers)
    a.exec_()

    exit_code = qgs.exec_()
    qgs.exitQgis()
    sys.exit(exit_code)
    # sys.exit(app.exec_())