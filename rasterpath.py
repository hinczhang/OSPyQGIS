import sys, os
from rasterpathUI import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QMessageBox, QGraphicsPixmapItem, QGraphicsScene, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QStringListModel, pyqtSignal
from qgis.core import *
import gdal
import math
import cv2
import numpy as np

class Func_ratserpath_class(QDialog, Ui_Dialog):
    mySignal = pyqtSignal(int)
    def __init__(self, layers):
        super(Func_ratserpath_class, self).__init__()
        self.setupUi(self)
        self.slot_connect()
        self.layers = layers
        self.success = False
        self.loadmap = False

        self.ras_height = 0
        self.ras_width = 0
        self.num_x = 0
        self.num_y = 0
        self.box_scale.setEnabled(False)
        self.box_scale.setPlainText('Height: '+str(self.ras_height)+'px  Width: '+str(self.ras_width)+'px')
        self.x_Box.setEnabled(False)
        self.y_Box.setEnabled(False)
        self.runButton.setEnabled(False)
        self.chooseButton.setEnabled(False)
        self.pathEdit.setEnabled(False)
        self.plainTextEdit.setEnabled(False)
        for item in layers:
            self.rasterBox.addItem(item.name())

    def slot_connect(self):
        self.rasterBox.activated.connect(self.choose_raster_changed)
        self.x_Box.valueChanged.connect(self.get_value_x)
        self.y_Box.valueChanged.connect(self.get_value_y)
        self.runButton.clicked.connect(self.processing_flow_path)
        self.chooseButton.clicked.connect(self.action_choose_path)

    def action_choose_path(self):
        file_choose, file_type = QFileDialog.getSaveFileName(self, "Raster Saving", "./processImage/","Tiff Files (*.tif)")
        self.save_path = file_choose
        self.pathEdit.setText(file_choose)
        self.runButton.setEnabled(True)

    def mouse_press_pixel(self, event):
        event = event.scenePos()
        self.x_Box.setValue(event.y())
        self.y_Box.setValue(event.x())
        self.plainTextEdit.setPlainText(str(self.band[self.x_Box.value()][self.y_Box.value()]))

    def choose_raster_changed(self):
        choose_index = self.rasterBox.currentIndex()
        if self.layers[choose_index].bandCount() != 1:
            QMessageBox.critical(self, "Error", "One band raster is needed", QMessageBox.Yes)
            return

        target_raster = self.layers[choose_index]
        self.transform_raster_type(target_raster)

    def get_value_x(self):
        self.num_x = self.x_Box.value()
        self.plainTextEdit.setPlainText(str(self.band[self.num_x][self.num_y]))

    def get_value_y(self):
        self.num_y = self.y_Box.value()
        self.plainTextEdit.setPlainText(str(self.band[self.num_x][self.num_y]))

    def transform_raster_type(self, raster):
        dataSource = gdal.Open(raster.source())
        self.projection = dataSource.GetProjection()
        self.geoTransform = dataSource.GetGeoTransform()
        self.band = np.array(dataSource.GetRasterBand(1).ReadAsArray())
        self.ras_height, self.ras_width = self.band.shape
        self.box_scale.setPlainText('Height: ' + str(self.ras_height) + 'px' + '    Width: ' + str(self.ras_width)+'px')
        self.x_Box.setEnabled(True)
        self.y_Box.setEnabled(True)

        self.x_Box.setRange(1, self.ras_height-1)
        self.y_Box.setRange(1, self.ras_width-1)
        coloredImg = cv2.merge([self.band, self.band, self.band])
        coloredImg = coloredImg.astype(np.uint8)
        #coloredImg = cv2.normalize(coloredImg, None, 0, 255, cv2.NORM_MINMAX)
        temp = cv2.cvtColor(coloredImg, cv2.COLOR_BGR2RGB)
        #cv2.imwrite("./processImage/temp.bmp", temp)
        #temp = cv2.imread("./processImage/temp.bmp")
        frame = QImage(temp.data, temp.shape[1], temp.shape[0], 3*temp.shape[1], QImage.Format_RGB888)
        print('load')
        try:
            pix = QPixmap.fromImage(frame)
        except:
            print('load faliled')
            try:
                os.remove("./processImage/temp.bmp")
            except:
                pass
            return
        print('load finished')

        item = QGraphicsPixmapItem(pix)
        self.scene = QGraphicsScene()
        self.scene.addItem(item)

        self.graphicsView.setScene(self.scene)
        try:
            os.remove("./processImage/temp.bmp")
        except:
            pass
        self.scene.mousePressEvent=self.mouse_press_pixel
        try:
            os.remove("./processImage/temp.bmp")
        except:
            pass
        self.chooseButton.setEnabled(True)

    def processing_flow_path(self):
        band = self.band
        pointArrayX = [self.num_x-1]
        pointArrayY = [self.num_y-1]
        x = self.num_x-1
        y = self.num_y-1

        while True:
            nowPoint = band[x][y]
            print(nowPoint)
            direction = [(float(nowPoint)-float(band[x-1][y-1]))/math.sqrt(2), float(nowPoint)-float(band[x][y-1]),
                         (float(nowPoint)-float(band[x+1][y-1]))/math.sqrt(2), float(nowPoint)-float(band[x+1][y]),
                         (float(nowPoint)-float(band[x+1][y+1]))/math.sqrt(2), float(nowPoint)-float(band[x][y+1]),
                         (float(nowPoint)-float(band[x-1][y+1]))/math.sqrt(2), float(nowPoint)-float(band[x-1][y])]
            max_index = 0
            max_num = -9999
            for index in range(0, 8):
                if max_num < direction[index]:
                    max_num = direction[index]
                    max_index = index
            print(max_num,max_index)
            if max_num < 0:
                break
            if max_num == 0:
                flag = False
                for itemX, itemY in zip(pointArrayX, pointArrayY):
                    if x == itemX and y == itemY:
                        flag = True
                        break
                if flag:
                    break
            if max_index == 0:
                x = x - 1
                y = y - 1
            elif max_index == 1:
                y = y - 1
            elif max_index == 2:
                x = x + 1
                y = y - 1
            elif max_index == 3:
                x = x + 1
            elif max_index == 4:
                x = x + 1
                y = y + 1
            elif max_index == 5:
                y = y + 1
            elif max_index == 6:
                x = x - 1
                y = y + 1
            else:
                x = x - 1

            if x < 1 or x > self.ras_height - 1 or y < 1 or y > self.ras_width - 1:
                break
            else:
                pointArrayX.append(x)
                pointArrayY.append(y)
        if len(pointArrayX) < 20:
            QMessageBox.warning(self, "warning", "path is too short", QMessageBox.Yes)
        single_band = band

        coloredImg = cv2.merge([single_band, single_band, single_band])
        cv2.imwrite("./processImage/temp.bmp",coloredImg)
        coloredImg = cv2.imread("./processImage/temp.bmp")
        try:
            os.remove("./processImage/temp.bmp")
        except:
            pass
        for index in range(0, len(pointArrayX)-2):
            cv2.line(coloredImg, (pointArrayY[index], pointArrayX[index]), (pointArrayY[index+1], pointArrayX[index+1]), (255, 0, 0), 3)
        self.craete_tiff(np.array(coloredImg))
        self.success = True
        self.loadmap = True
        self.mySignal.emit(1)
        self.close()


    def craete_tiff(self, target_img):
        driver = gdal.GetDriverByName("GTiff")
        datatype = 0
        if 'int8' in target_img.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in target_img.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32
        outDs = driver.Create(self.save_path, target_img.shape[1], target_img.shape[0], target_img.shape[2], datatype)
        outDs.SetGeoTransform(self.geoTransform)
        outDs.SetProjection(self.projection)
        outDs.GetRasterBand(1).WriteArray(target_img[:, :, 2])
        outDs.GetRasterBand(2).WriteArray(target_img[:, :, 1])
        outDs.GetRasterBand(3).WriteArray(target_img[:, :, 0])
        del outDs
        self.result = QgsRasterLayer(self.save_path)
        QMessageBox.information(self, "success", "Task Finished!", QMessageBox.Yes)

def main():
    qgs = QgsApplication([], True)
    qgs.setPrefixPath('qgis', True)
    qgs.initQgis()

    layers = []
    layers.append(QgsRasterLayer("./Image/1.tif", "1"))
    layers.append(QgsRasterLayer("./Image/2.tif", "2"))
    layers.append(QgsRasterLayer("./Image/3.tif", "3"))
    layers.append(QgsRasterLayer("./Image/1/5.tif", "6"))
    layers.append(QgsRasterLayer("./Image/dem.tif", "dem"))
    window = Func_ratserpath_class(layers)
    window.show()

    exit_code = qgs.exec_()
    qgs.exitQgis()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
