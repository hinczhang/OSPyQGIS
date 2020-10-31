import os, sys
import cv2
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from qgis.gui import QgsMapCanvas, QgsMapToolPan, QgsMapToolZoom, QgsMapToolIdentify
from qgis.core import QgsProject, QgsApplication, QgsVectorLayer, QgsRasterLayer
from Dlg_lvbo import Dlg_lvbo_class
import gdal
import qdarkstyle

class Func_lvbo_class(QDialog,Dlg_lvbo_class):
    mySignal=pyqtSignal(int)
    # result=""

    def __init__(self,layers):
        super(Func_lvbo_class,self).__init__()
        self.setupUi(self)
        self.radioButton.toggled.connect(self.btnstate1)
        self.radioButton_2.toggled.connect(self.btnstate2)
        self.radioButton_3.toggled.connect(self.btnstate3)
        self.radioButton_4.toggled.connect(self.btnstate4)
        self.radioButton_5.toggled.connect(self.btnstate5)
        self.radioButton.setChecked(True)
        self.lineEdit_name.setText("processImage/result_lvbo1.tif")


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
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.savefile)

    def btnstate1(self):
        if self.radioButton.isChecked()==True:
            self.lineEdit_2.setText("1/9")
            self.lineEdit_3.setText("1/9")
            self.lineEdit_4.setText("1/9")
            self.lineEdit_5.setText("1/9")
            self.lineEdit_6.setText("1/9")
            self.lineEdit_7.setText("1/9")
            self.lineEdit_8.setText("1/9")
            self.lineEdit_9.setText("1/9")
            self.lineEdit_10.setText("1/9")
    def btnstate2(self):
        if self.radioButton_2.isChecked() == True:
            self.lineEdit_2.setText("1/16")
            self.lineEdit_3.setText("2/16")
            self.lineEdit_4.setText("1/16")
            self.lineEdit_5.setText("2/16")
            self.lineEdit_6.setText("2/16")
            self.lineEdit_7.setText("2/16")
            self.lineEdit_8.setText("1/16")
            self.lineEdit_9.setText("2/16")
            self.lineEdit_10.setText("1/16")
    def btnstate3(self):
        if self.radioButton_3.isChecked() == True:
            self.lineEdit_2.setText("-1")
            self.lineEdit_3.setText("0")
            self.lineEdit_4.setText("1")
            self.lineEdit_5.setText("-2")
            self.lineEdit_6.setText("0")
            self.lineEdit_7.setText("2")
            self.lineEdit_8.setText("-1")
            self.lineEdit_9.setText("0")
            self.lineEdit_10.setText("1")
    def btnstate4(self):
        if self.radioButton_4.isChecked() == True:
            self.lineEdit_2.setText("1")
            self.lineEdit_3.setText("1")
            self.lineEdit_4.setText("1")
            self.lineEdit_5.setText("1")
            self.lineEdit_6.setText("-8")
            self.lineEdit_7.setText("1")
            self.lineEdit_8.setText("1")
            self.lineEdit_9.setText("1")
            self.lineEdit_10.setText("1")
    def btnstate5(self):
        if self.radioButton_5.isChecked() == True:
            self.lineEdit_2.setText("")
            self.lineEdit_3.setText("")
            self.lineEdit_4.setText("")
            self.lineEdit_5.setText("")
            self.lineEdit_6.setText("")
            self.lineEdit_7.setText("")
            self.lineEdit_8.setText("")
            self.lineEdit_9.setText("")
            self.lineEdit_10.setText("")
            self.lineEdit_2.setValidator(QIntValidator(0, 99))
            self.lineEdit_3.setValidator(QIntValidator(0, 99))
            self.lineEdit_4.setValidator(QIntValidator(0, 99))
            self.lineEdit_5.setValidator(QIntValidator(0, 99))
            self.lineEdit_6.setValidator(QIntValidator(0, 99))
            self.lineEdit_7.setValidator(QIntValidator(0, 99))
            self.lineEdit_8.setValidator(QIntValidator(0, 99))
            self.lineEdit_9.setValidator(QIntValidator(0, 99))
            self.lineEdit_10.setValidator(QIntValidator(0, 99))
            self.lineEdit_2.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.lineEdit_3.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.lineEdit_4.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.lineEdit_5.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.lineEdit_6.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.lineEdit_7.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.lineEdit_8.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.lineEdit_9.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.lineEdit_10.setFocusPolicy(QtCore.Qt.StrongFocus)

    def action(self):
        self.Func_lvbo_def()
        self.close()

    def savefile(self):
        fullpath, format = QFileDialog.getSaveFileName(self, '保存数据', '', '*.tif')
        if os.path.exists(fullpath):
            os.remove(fullpath)
        self.lineEdit_name.setText(fullpath)

    def Func_lvbo_def(self):
        # 自定义卷积核
        k11=eval(self.lineEdit_2.text())
        k12 = eval(self.lineEdit_3.text())
        k13 = eval(self.lineEdit_4.text())
        k21 = eval(self.lineEdit_5.text())
        k22 = eval(self.lineEdit_6.text())
        k23 = eval(self.lineEdit_7.text())
        k31 = eval(self.lineEdit_8.text())
        k32 = eval(self.lineEdit_9.text())
        k33 = eval(self.lineEdit_10.text())

        kernel_sharpen_1 = np.array([
            [k11, k12, k13],
            [k21, k22, k23],
            [k31, k32, k33]])

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

        output_1 = cv2.filter2D(img, -1, kernel_sharpen_1)

        cv2.imwrite(fullpath,output_1)
        if self.checkBox.isChecked():
            (tempPath, tempAllFileName) = os.path.split(fullpath)
            (tempFileName, extendName) = os.path.splitext(tempAllFileName)
            self.result = QgsRasterLayer(fullpath, tempFileName)
            self.mySignal.emit(1)
        else:
            self.mySignal.emit(0)
        self.result=QgsRasterLayer(fullpath, "result_lvbo1")

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
    a=Func_lvbo_class(layers)
    a.exec_()

    exit_code = qgs.exec_()
    qgs.exitQgis()
    sys.exit(exit_code)
    # sys.exit(app.exec_())