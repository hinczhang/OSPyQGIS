import os
import cv2
import gdal
import numpy as np
from qgis.core import QgsRasterLayer
from PyQt5.QtWidgets import QDialog
from Dlg_SuperpixerSeeds import Ui_Dialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import  QFileDialog, QMessageBox


class Func_SuperpixerSeeds_class(QDialog, Ui_Dialog):
    mySignal = pyqtSignal(int)  # 规定信号
    def __init__(self, layers):
        super(Func_SuperpixerSeeds_class, self).__init__()
        self.setupUi(self)
        # 连接函数
        self.slot_connect()
        # 状态变量、信息变量初始化
        self.success = False
        self.errorMessage = ''
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

    def slot_connect(self):
        self.pushButton_ok.clicked.connect(self.pushButton_ok_clicked)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_name.clicked.connect(self.pushButton_name_clicked)


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

    def pushButton_ok_clicked(self):
        index_r = self.comboBox_r.currentIndex()
        index_g = self.comboBox_g.currentIndex()
        index_b = self.comboBox_b.currentIndex()
        fullpath = self.lineEdit_name.text()
        if self.bands[index_r].shape[0] != self.bands[index_g].shape[0] or self.bands[index_r].shape[0] != self.bands[index_b].shape[0] or self.bands[index_r].shape[1] != self.bands[index_g].shape[1] or self.bands[index_r].shape[1] != self.bands[index_b].shape[1]:
            QMessageBox.critical(self, '波段错误', '选择的RGB波段的长宽不相等，请重新选择')
            return
        if fullpath == '':
            QMessageBox.information(self, '位置为空', '请选择生成文件的保存位置')
            return
        img = cv2.merge([self.bands[index_b], self.bands[index_g], self.bands[index_r]])
        num_superpixers = self.spinBox_num_superpixers.value()
        levels = self.spinBox_levels.value()
        historam_bins = self.spinBox_historam_bins.value()
        num = self.spinBox_num.value()
        seeds = cv2.ximgproc.createSuperpixelSEEDS(img.shape[1],img.shape[0],img.shape[2],num_superpixers,levels,3,historam_bins,True)
        seeds.iterate(img, num)  #输入图像大小必须与初始化形状相同，迭代次数为10
        mask_seeds = seeds.getLabelContourMask()
        mask_inv_seeds = cv2.bitwise_not(mask_seeds)
        img_seeds = cv2.bitwise_and(img,img,mask =  mask_inv_seeds)
        self.create_tiff(fullpath, self.projections[index_r], self.geoTransform[index_r], img_seeds)
        if self.checkBox.isChecked():
            (tempPath, tempAllFileName) = os.path.split(fullpath)
            (tempFileName, extendName) = os.path.splitext(tempAllFileName)
            self.result = QgsRasterLayer(fullpath, tempFileName)
            self.mySignal.emit(1)
        else:
            self.mySignal.emit(0)
        self.close()

    def pushButton_name_clicked(self):
        fullpath, format = QFileDialog.getSaveFileName(self, '保存数据', '', '*.tif')
        if os.path.exists(fullpath):
            os.remove(fullpath)
        self.lineEdit_name.setText(fullpath)
