import os, sys
import cv2
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from qgis.gui import QgsMapCanvas, QgsMapToolPan, QgsMapToolZoom, QgsMapToolIdentify
from qgis.core import QgsProject, QgsApplication, QgsVectorLayer, QgsRasterLayer
from Dlg_jiaodian import Dlg_jiaodian_class
import gdal
import qdarkstyle

class Func_jiaodian_class(QDialog,Dlg_jiaodian_class):
    mySignal=pyqtSignal(int)
    # result=""

    def __init__(self,layers):
        super(Func_jiaodian_class,self).__init__()
        self.setupUi(self)

        self.lineEdit_name.setText("processImage/result_jiaodian.tif")

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
        for i in [3,5,7]:
            ffName=str(i)+"x"+str(i)
            self.comboBox_daxiao.addItem(ffName,i)

        self.comboBox_fangfa.addItem("最大值", 0)
        self.comboBox_fangfa.addItem("最小值", 1)
        self.comboBox_fangfa.addItem("平均值", 2)
        self.comboBox_fangfa.addItem("中位数", 3)

        # print(layer)
        self.pushButton.clicked.connect(self.action)
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.savefile)



    def action(self):
        self.Func_jiaodian_def()
        self.close()

    def savefile(self):
        fullpath, format = QFileDialog.getSaveFileName(self, '保存数据', '', '*.tif')
        if os.path.exists(fullpath):
            os.remove(fullpath)
        self.lineEdit_name.setText(fullpath)

    def Func_jiaodian_def(self):
        # 卷积

        index_b=self.comboBox_b.currentIndex()
        index_g = self.comboBox_g.currentIndex()
        index_r = self.comboBox_r.currentIndex()
        fullpath = self.lineEdit_name.text()
        if self.bands[index_r].shape[0] != self.bands[index_g].shape[0] or self.bands[index_r].shape[0] != \
                self.bands[index_b].shape[0] or self.bands[index_r].shape[1] != self.bands[index_g].shape[1] or \
                self.bands[index_r].shape[1] != self.bands[index_b].shape[1]:
            QMessageBox.critical(self, '波段错误', '选择的RGB波段的长宽不相等，请重新选择')
            self.mySignal.emit(-1)
            return
        if fullpath == '':
            QMessageBox.information(self, '位置为空', '请选择生成文件的保存位置')
            self.mySignal.emit(-1)
            return

        img = cv2.merge([self.bands[index_b], self.bands[index_g], self.bands[index_r]])
        rows = img.shape[0]
        cols = img.shape[1]
        if self.checkBox_2.isChecked():
            image=cv2.resize(img,(int(cols/4),int(rows/4)))
        else:
            image = cv2.resize(img, (int(cols), int(rows)))
        B,G,R=cv2.split(image)
        # rows, cols = image.shape
        rows=image.shape[0]
        cols=image.shape[1]

        # 窗口的宽高均为奇数
        # winH, winW = winSize
        winH=(self.comboBox_daxiao.currentIndex()+1)*2+1
        winW=winH
        print(winH)
        halfWinH = int((winH - 1) / 2)
        halfWinW = int((winW - 1) / 2)

        # 中值滤波后的输出图像
        medianBlurImageB = np.zeros(B.shape, B.dtype)
        medianBlurImageG = np.zeros(B.shape, B.dtype)
        medianBlurImageR = np.zeros(B.shape, B.dtype)

        for r in range(rows):
            for c in range(cols):
                # 判断边界
                rTop = 0 if r - halfWinH < 0 else r - halfWinH
                rBottom = rows - 1 if r + halfWinH > rows - 1 else r + halfWinH
                cLeft = 0 if c - halfWinW < 0 else c - halfWinW
                cRight = cols if c + halfWinW > cols - 1 else c + halfWinW

                # 取邻域
                regionb = B[rTop:rBottom + 1, cLeft:cRight + 1]
                regiong = G[rTop:rBottom + 1, cLeft:cRight + 1]
                regionr = R[rTop:rBottom + 1, cLeft:cRight + 1]
                # 求中值np.median   np.max  np.mean
                if self.comboBox_fangfa.currentIndex()==0:
                    medianBlurImageB[r][c] = np.max(regionb)
                    medianBlurImageG[r][c] = np.max(regiong)
                    medianBlurImageR[r][c] = np.max(regionr)
                elif self.comboBox_fangfa.currentIndex()==1:
                    medianBlurImageB[r][c] = np.min(regionb)
                    medianBlurImageG[r][c] = np.min(regiong)
                    medianBlurImageR[r][c] = np.min(regionr)
                elif self.comboBox_fangfa.currentIndex() == 2:
                    medianBlurImageB[r][c] = np.mean(regionb)
                    medianBlurImageG[r][c] = np.mean(regiong)
                    medianBlurImageR[r][c] = np.mean(regionr)
                elif self.comboBox_fangfa.currentIndex() == 3:
                    medianBlurImageB[r][c] = np.median(regionb)
                    medianBlurImageG[r][c] = np.median(regiong)
                    medianBlurImageR[r][c] = np.median(regionr)

        medianBlurImage = cv2.merge([medianBlurImageB, medianBlurImageG, medianBlurImageR])

        cv2.imwrite(fullpath, medianBlurImage)

        if self.checkBox.isChecked():
            (tempPath, tempAllFileName) = os.path.split(fullpath)
            (tempFileName, extendName) = os.path.splitext(tempAllFileName)
            self.result = QgsRasterLayer(fullpath, tempFileName)
            self.mySignal.emit(1)
        else:
            self.mySignal.emit(0)
        self.result=QgsRasterLayer(fullpath, "result_jiaodian")

if __name__ == '__main__':
    qgs = QgsApplication([], True)
    qgs.setPrefixPath('qgis', True)
    # 启动QGIS
    qgs.initQgis()
    layers = []

    app = QApplication(sys.argv)
    rlayer = QgsRasterLayer("D:/kaiyuanGIS/OSPyQGIS/venv/Image/1.tif", "city")
    vlayer = QgsVectorLayer("D://开源GIS//代码示例与数据//data//polygons.shp", "shp", "ogr")
    layers.append(rlayer)
    a=Func_jiaodian_class(layers)
    a.exec_()

    exit_code = qgs.exec_()
    qgs.exitQgis()
    sys.exit(exit_code)
    # sys.exit(app.exec_())