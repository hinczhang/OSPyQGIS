import os, sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qgis.gui import QgsMapCanvas, QgsMapToolPan, QgsMapToolZoom, QgsMapToolIdentify
from qgis.core import QgsProject, QgsApplication, QgsVectorLayer, QgsRasterLayer
from MainDlg import Ui_Dialog as Main_Ui_Dialog
import qdarkstyle
#CTYadd
import importlib

import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
import matplotlib.pyplot as plt
import numpy as np
import gdal
from PIL import Image

from Func_lvbo import Func_lvbo_class
from func_calculator_class import Func_calculator_class
from Func_unsupervised import Func_unsupervised_class
from Func_SuperpixerLsc import Func_SuperpixerLsc_class
from Func_SuperpixerSeeds import Func_SuperpixerSeeds_class
from Func_SuperpixerSlic import Func_SuperpixerSlic_class
from Func_clip_class import Func_clip_class
from Func_jiaodian import Func_jiaodian_class
from Func_cornerdetection_class import Func_cornerdetection_class
from Func_FAST import Func_FAST_class
from rasterpath import Func_ratserpath_class

class Main_exe(QDialog,Main_Ui_Dialog):
    def __init__(self):
        super(Main_exe,self).__init__()
        self.setupUi(self)

        self.LayerName, self.LayerPath = range(2)
        self.TreeViewModel = QStandardItemModel()
        self.main_progressBar.setValue(0)

        self.layers = []
        self.tempFileNames=[]
        self.init_mapCanvas()
        self.loadStyle()
        self.slot_connect()
        # CTYadd
        self.dlgcount = 0
        self.myaddDlg = []
        self.myaddBtn = []
        self.show()

    def slot_connect(self):
        self.main_pB_dk.clicked.connect(self.action_open_clicked)
        self.main_pB_bc.clicked.connect(self.action_save_clicked)
        self.main_pB_fd.clicked.connect(self.button_fd_clicked)
        self.main_pB_sx.clicked.connect(self.button_sx_clicked)
        self.main_pB_td.clicked.connect(self.button_td_clicked)
        self.main_pB_qt.clicked.connect(self.button_qt_clicked)
        self.main_pB_sc.clicked.connect(self.button_sc_clicked)

        self.pB_lb.clicked.connect(self.action_lb_clicked)
        self.pB_js.clicked.connect(self.action_js_clicked)
        self.pB_cj.clicked.connect(self.action_cj_clicked)
        self.pb_fl.clicked.connect(self.action_fl_clicked)
        self.pB_fg_1.clicked.connect(self.action_fg1_clicked)
        self.pB_fg_2.clicked.connect(self.action_fg2_clicked)
        self.pB_fg_3.clicked.connect(self.action_fg3_clicked)
        self.pB_jd.clicked.connect(self.action_jd_clicked)
        # self.pB_jdjc.clicked.connect(self.action_jdjc_clicked)
        self.pB_jdjc.clicked.connect(self.action_jdjc_clicked)
        self.pB_fast.clicked.connect(self.action_FAST_clicked)
        self.pB_sllj.clicked.connect(self.action_sllj_clicked)
        # CTYadd
        self.main_close.clicked.connect(self.close)
        self.main_mini.clicked.connect(self.mini)
        self.main_pushButton1.clicked.connect(self.action_add)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.main_treeView.doubleClicked.connect(self.action_showHist)

    # CTYadd
    def mini(self):
        self.setWindowState(Qt.WindowMinimized)

#region plot
    def histogram(self,layer):
        print("draw histogram")
        print(layer)

        bandcount=layer.bandCount()
        ds=gdal.Open(layer.source())
        print(ds)

        bands=[]
        if bandcount==1:
            bands.append(np.array(ds.GetRasterBand(1).ReadAsArray()))
        else:
            for i in range(1,4):
                band=np.array(ds.GetRasterBand(i).ReadAsArray())
                bands.append(band)
        print("layerband:{0}".format(bands))

        colors=['red','green','blue']
        plt.figure("直方图")
        for i in range(0, bandcount):
            arr=bands[i].flatten()
            plt.hist(arr, bins=256, color=colors[i], alpha=0.75, histtype='step')
        plt.show()
#endregion

#region main basic op
    def loadStyle(self):
        with open("style.qss") as file:
            str = file.readlines()
            str = ''.join(str).strip('\n')
        # 设置黑色样式
        # self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setStyleSheet(str)

    def init_mapCanvas(self):
        self.mapCanvas = QgsMapCanvas()
        self.mapCanvas.setCanvasColor(Qt.white)
        self.mapCanvas.setFrameShadow(5)
        self.mapCanvas.enableAntiAliasing(True)
        layout = QVBoxLayout(self.main_wg_canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.mapCanvas)
        # 初始化TreeView
        self.TreeViewModel = self.createLayerModel(self)
        self.main_treeView.setModel(self.TreeViewModel)

    def addLayerInTreeView(self, model, layername, layerpath):
        model.insertRow(0)
        model.setData(model.index(0, self.LayerName), layername)
        model.setData(model.index(0, self.LayerPath), layerpath)

    def createLayerModel(self, parent):
        model = QStandardItemModel(0, 2, parent)
        model.setHeaderData(self.LayerName, Qt.Horizontal, "Layer")
        model.setHeaderData(self.LayerPath, Qt.Horizontal, "Path")
        return model

    def loadMap(self, fullpath):
        # print(fullpath)
        # 打开矢量图层
        # self.layer = QgsVectorLayer(fullpath, "shp", "ogr")
        (tempPath, tempAllFileName) = os.path.split(fullpath)
        (tempFileName, extendName) = os.path.splitext(tempAllFileName)
        self.layer = QgsRasterLayer(fullpath, tempFileName)
        self.layers.insert(0,self.layer)
        # 注册图层
        QgsProject.instance().addMapLayer(self.layer)
        self.mapCanvas.setLayers(self.layers)
        # 设置图层范围
        self.mapCanvas.setExtent(self.layer.extent())
        self.mapCanvas.refresh()
        # 添加treeview item
        self.addLayerInTreeView(self.TreeViewModel, tempFileName, fullpath)

    def loadMap_dlg(self, rlayer, layername):
        self.layers.insert(0,rlayer)
        # 注册图层
        QgsProject.instance().addMapLayer(rlayer)
        self.mapCanvas.setLayers(self.layers)
        # 设置图层范围
        self.mapCanvas.setExtent(rlayer.extent())
        self.mapCanvas.refresh()
        rlayername=rlayer.name()
        #self.addLayerInTreeView(self.TreeViewModel, rlayername, "result")
        self.addLayerInTreeView(self.TreeViewModel, rlayername, layername)

    def action_showHist(self):
        print("tree item clicked")
        index = self.main_treeView.currentIndex().row()
        print("current index:{0}".format(index))
        self.histogram(self.layers[index])
#endregion

#region main control
    def action_open_clicked(self):
        fullpaths, format = QFileDialog.getOpenFileNames(self, '打开数据', '', '*.tif')
        if len(fullpaths)==0:
            print("\n取消选择")
            return
        for fullpath in fullpaths:
            self.loadMap(fullpath)

    def action_save_clicked(self):
        fullpath, format = QFileDialog.getSaveFileName(self, '保存数据', '', '*.tif')
        # if os.path.exists(fullpath):
        self.mapCanvas.saveAsImage(fullpath)

    def button_fd_clicked(self):
        self.maptool = QgsMapToolZoom(self.mapCanvas, False)
        self.mapCanvas.setMapTool(self.maptool)

    def button_sx_clicked(self):
        self.maptool = QgsMapToolZoom(self.mapCanvas, True)
        self.mapCanvas.setMapTool(self.maptool)

    def button_td_clicked(self):
        self.maptool = QgsMapToolPan(self.mapCanvas)
        self.mapCanvas.setMapTool(self.maptool)

    def button_qt_clicked(self):
        self.mapCanvas.setExtent(self.layer.extent())
        self.mapCanvas.refresh()

    def button_sc_clicked(self):
        index=self.main_treeView.currentIndex().row()
        print("current index:{0}".format(index))
        self.TreeViewModel.removeRows(index,1)

        del self.layers[index]

        print("layer count:{0}".format(len(self.layers)))
        if len(self.layers)==0:
            msg_box=QMessageBox(QMessageBox.Warning,"警告","已删除所有图层！")
            msg_box.exec_()
            self.mapCanvas.setLayers(self.layers)
            #self.mapCanvas.zoomWithCenter(10000,10000,1)
        else:
            # print(self.mapCanvas.layer(index))
            self.mapCanvas.setLayers(self.layers)
            self.mapCanvas.refresh()


    def action_treeitem_doubleclickd_delItem(self): #no use
        print("tree item double clicked")
        index=self.main_treeView.currentIndex().row()
        print("current index:{0}".format(index))
        self.TreeViewModel.removeRows(index,1)
        del self.layers[index]
#endregion

#region function button
    def action_lb_clicked(self):
        self.main_progressBar.setValue(0)
        self.myDlg=Func_lvbo_class(self.layers)
        self.myDlg.mySignal.connect(self.signalCall)
        self.myDlg.show()

    def action_js_clicked(self):
        self.main_progressBar.setValue(0)
        self.myDlg=Func_calculator_class(self.layers)
        self.myDlg.mySignal.connect(self.signalCall)
        self.myDlg.show()

    def action_cj_clicked(self):
        self.main_progressBar.setValue(0)
        self.myDlg=Func_clip_class(self.layers)
        self.myDlg.mySignal.connect(self.signalCall)
        self.myDlg.show()

    def action_fl_clicked(self):
        self.main_progressBar.setValue(0)
        self.myDlg=Func_unsupervised_class(self.layers)
        self.myDlg.mySignal.connect(self.signalCall)
        self.myDlg.show()

    def action_fg1_clicked(self):
        self.main_progressBar.setValue(0)
        self.myDlg=Func_SuperpixerLsc_class(self.layers)
        self.myDlg.mySignal.connect(self.signalCall)
        self.myDlg.show()

    def action_fg2_clicked(self):
        self.main_progressBar.setValue(0)
        self.myDlg=Func_SuperpixerSeeds_class(self.layers)
        self.myDlg.mySignal.connect(self.signalCall)
        self.myDlg.show()

    def action_fg3_clicked(self):
        self.main_progressBar.setValue(0)
        self.myDlg=Func_SuperpixerSlic_class(self.layers)
        self.myDlg.mySignal.connect(self.signalCall)
        self.myDlg.show()

    def action_jd_clicked(self):
        self.main_progressBar.setValue(0)
        self.myDlg=Func_jiaodian_class(self.layers)
        self.myDlg.mySignal.connect(self.signalCall)
        self.myDlg.show()

    def action_jdjc_clicked(self):
        self.main_progressBar.setValue(0)
        self.myDlg=Func_cornerdetection_class(self.layers)
        self.myDlg.mySignal.connect(self.signalCall)
        self.myDlg.show()

    def action_FAST_clicked(self):
        self.main_progressBar.setValue(0)
        self.myDlg=Func_FAST_class(self.layers)
        self.myDlg.mySignal.connect(self.signalCall)
        self.myDlg.show()

    def action_sllj_clicked(self):
        self.main_progressBar.setValue(0)
        self.myDlg = Func_ratserpath_class(self.layers)
        self.myDlg.mySignal.connect(self.signalCall)
        self.myDlg.show()

    # CTYadd "+"op
    def action_add(self):
        fullpath, format = QFileDialog.getOpenFileName(self, '打开python主类文件', '', '*.py')
        (tempPath, tempAllFileName) = os.path.split(fullpath)
        (tempFileName, extendName) = os.path.splitext(tempAllFileName)
        model = importlib.import_module(tempFileName)
        self.tempDlg = getattr(model, tempFileName + '_class')(self.layers)
        self.tempFileNames.append(tempFileName)
        self.myaddDlg.append(self.tempDlg)
        self.myaddDlg[self.dlgcount].mySignal.connect(self.addsignalCall)
        self.myaddDlg[self.dlgcount].show()

    def addsignalCall(self, val):
        print(self.myaddDlg[self.dlgcount].result.name())
        if val == -1:
            print("error")
        elif val == 0:
            print("result has been generated.")
            addButFunc()
            self.dlgcount = self.dlgcount + 1
        elif val == 1:
            print("success")
            self.loadMap_dlg(rlayer=self.myaddDlg[self.dlgcount].result,
                             layername=self.myaddDlg[self.dlgcount].result.name())
            self.main_progressBar.setValue(100)
            self.addButFunc()
            self.dlgcount = self.dlgcount + 1

    def addButFunc(self):
        addbtn = QPushButton(self)
        self.myaddBtn.append(addbtn)
        self.myaddBtn[self.dlgcount].setGeometry((935 + 80 * self.dlgcount), 90, 80, 80)
        self.myaddBtn[self.dlgcount].setText(" ")
        stem = "add" + str(self.dlgcount)
        self.myaddBtn[self.dlgcount].setObjectName(stem)
        self.myaddBtn[self.dlgcount].show()
        if self.dlgcount==0:
            self.myaddBtn[self.dlgcount].clicked.connect(self.button_clicked0)
        elif self.dlgcount==1:
            self.myaddBtn[self.dlgcount].clicked.connect(self.button_clicked1)
        elif self.dlgcount==2:
            self.myaddBtn[self.dlgcount].clicked.connect(self.button_clicked2)
        elif self.dlgcount==3:
            self.myaddBtn[self.dlgcount].clicked.connect(self.button_clicked3)
        elif self.dlgcount==4:
            self.myaddBtn[self.dlgcount].clicked.connect(self.button_clicked4)
        elif self.dlgcount==5:
            self.myaddBtn[self.dlgcount].clicked.connect(self.button_clicked5)
        self.anim = QPropertyAnimation(self.main_pushButton1, b"geometry")
        self.anim.setDuration(500)
        self.anim.setStartValue(QRect((935 + 80 * self.dlgcount), 90, 80, 80))  # 大小100*100
        self.anim.setEndValue(QRect((935 + 80 * (self.dlgcount + 1)), 90, 80, 80))  # 大小200*200
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()

    def button_clicked0(self):
        model = importlib.import_module(self.tempFileNames[0])
        self.myaddDlg[0] = getattr(model, self.tempFileNames[0] + '_class')(self.layers)
        self.myaddDlg[0].mySignal.connect(self.addsignalCall0)
        self.myaddDlg[0].show()
    def addsignalCall0(self, val):
        print(self.myaddDlg[0].result.name())
        if val == -1:
            print("error")
        elif val == 0:
            print("result has been generated.")
        elif val == 1:
            print("success")
            self.loadMap_dlg(rlayer=self.myaddDlg[0].result,
                             layername=self.myaddDlg[0].result.name())
            self.main_progressBar.setValue(100)
    def button_clicked1(self):
        model = importlib.import_module(self.tempFileNames[1])
        self.myaddDlg[1] = getattr(model, self.tempFileNames[1] + '_class')(self.layers)
        self.myaddDlg[1].mySignal.connect(self.addsignalCall1)
        self.myaddDlg[1].show()
    def addsignalCall1(self, val):
        print(self.myaddDlg[1].result.name())
        if val == -1:
            print("error")
        elif val == 0:
            print("result has been generated.")
        elif val == 1:
            print("success")
            self.loadMap_dlg(rlayer=self.myaddDlg[1].result,
                             layername=self.myaddDlg[1].result.name())
            self.main_progressBar.setValue(100)

#endregion

    def signalCall(self,val):
        print(self.myDlg.result.name())
        if val==-1:
            print("error")
        elif val==0:
            print("result has been generated.")
        elif val==1:
            print("success")
            self.loadMap_dlg(rlayer=self.myDlg.result, layername=self.myDlg.result.name())
            self.main_progressBar.setValue(100)

if __name__ == '__main__':
    qgs = QgsApplication([], True)
    qgs.setPrefixPath('qgis', True)
    # 启动QGIS
    qgs.initQgis()
    app = QApplication(sys.argv)
    ex = Main_exe()
    exit_code = qgs.exec_()
    qgs.exitQgis()
    sys.exit(exit_code)
    # sys.exit(app.exec_())