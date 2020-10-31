import sys, os
from qgis.core import *
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from PyQt5.QtCore import QStringListModel, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAbstractItemView, QMessageBox
from dataloader_dialog_base import Ui_MainWindow


class Func_calculator_class(QMainWindow, Ui_MainWindow):

    mySignal = pyqtSignal(int)

    def __init__(self, layers):
        super(Func_calculator_class, self).__init__()
        self.setupUi(self)
        self.content = ""
        self.slot_connect()
        self.success = False
        self.loadmap = False
        self.show()

        rasterList = []
        for item in layers:
            rasterList.append({"layer": item, "name": item.name()})
        # 读取栅格信息
        slm=QStringListModel()
        self.totalEntities=rasterList
        self.rasters=[]
        self.rasterList=[]
        for raster in rasterList:
            self.rasters.append(raster['layer'])
            for i in range(1, raster['layer'].bandCount()+1):
                self.rasterList.append(raster['name']+'@'+str(i))

        self.ref = []
        slm.setStringList(self.rasterList)
        self.listView.setModel(slm)
        self.listView.doubleClicked.connect(self.action_choose_raster)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # 信号和槽的连接
    def slot_connect(self):
        # 按钮控件
        self.b0.clicked.connect(lambda: self.action_add_content('0'))
        self.b1.clicked.connect(lambda: self.action_add_content('1'))
        self.b2.clicked.connect(lambda: self.action_add_content('2'))
        self.b3.clicked.connect(lambda: self.action_add_content('3'))
        self.b4.clicked.connect(lambda: self.action_add_content('4'))
        self.b5.clicked.connect(lambda: self.action_add_content('5'))
        self.b6.clicked.connect(lambda: self.action_add_content('6'))
        self.b7.clicked.connect(lambda: self.action_add_content('7'))
        self.b8.clicked.connect(lambda: self.action_add_content('8'))
        self.b9.clicked.connect(lambda: self.action_add_content('9'))
        self.bDot.clicked.connect(lambda: self.action_add_content('.'))
        self.ClearB.clicked.connect(self.action_clear_content)
        self.multiple.clicked.connect(lambda: self.action_add_content('*'))
        self.divise.clicked.connect(lambda: self.action_add_content('/'))
        self.add.clicked.connect(lambda: self.action_add_content('+'))
        self.subtract.clicked.connect(lambda: self.action_add_content('-'))
        self.isEqual.clicked.connect(lambda: self.action_add_content('='))
        self.lowerB.clicked.connect(lambda: self.action_add_content('<'))
        self.BiggerEqualB.clicked.connect(lambda: self.action_add_content('>='))
        self.LOwerEqualB.clicked.connect(lambda: self.action_add_content('<='))
        self.BiggerB.clicked.connect(lambda: self.action_add_content('>'))
        self.isNotEqual.clicked.connect(lambda: self.action_add_content('!='))
        self.absB.clicked.connect(lambda: self.action_add_content('ABS('))
        self.powerB.clicked.connect(lambda: self.action_add_content('^'))
        self.sqrtB.clicked.connect(lambda: self.action_add_content('sqrt('))
        self.leftParen.clicked.connect(lambda: self.action_add_content('('))
        self.rightParen.clicked.connect(lambda: self.action_add_content(')'))
        self.sinB.clicked.connect(lambda: self.action_add_content('sin('))
        self.cosB.clicked.connect(lambda: self.action_add_content('cos('))
        self.tanB.clicked.connect(lambda: self.action_add_content('tan('))
        self.asinB.clicked.connect(lambda: self.action_add_content('asin('))
        self.acosB.clicked.connect(lambda: self.action_add_content('acos('))
        self.atanB.clicked.connect(lambda: self.action_add_content('atan('))
        self.lnB.clicked.connect(lambda: self.action_add_content('ln('))
        self.logB.clicked.connect(lambda: self.action_add_content('log10('))
        self.minB.clicked.connect(lambda: self.action_add_content('MIN('))
        self.maxB.clicked.connect(lambda: self.action_add_content('MAX('))

        # EditText控件
        self.textEdit.textChanged.connect(self.action_changed_text)

        # 执行控件
        self.runButton.clicked.connect(self.action_run_calculator)
        self.runButton.setEnabled(False)

        # 选择路径
        self.loadPath.clicked.connect(self.action_load_path)
        self.lineEdit.setEnabled(False)

    def action_add_content(self, n):
        position = self.get_cursor()
        if position == 0:
            position = len(self.content)
        temp = list(self.content)
        temp.insert(position, n)
        self.content = ''.join(temp)

        self.textEdit.setText(self.content)

    def action_clear_content(self):
        self.content = ""
        self.textEdit.setText(self.content)

    def action_choose_raster(self, qModelIndex):
        position = self.get_cursor()
        if position == 0:
            position = len(self.content)
        raster = "\"" + self.rasterList[qModelIndex.row()] + "\""
        temp = list(self.content)
        temp.insert(position, raster)
        self.content = ''.join(temp)

        self.ref.append(self.rasterList[qModelIndex.row()])
        self.textEdit.setText(self.content)

    def action_changed_text(self):
        self.content = self.textEdit.toPlainText()

    def findRaster(self,index):
        index=index.split('@')[0]
        for item in self.totalEntities:
            if item['name']==index:
                return item['layer']

    def action_run_calculator(self):
        formula = self.content
        print(formula)
        rlayer = self.rasters[0]

        entries=[]
        width=[]
        height=[]
        for index in range(0,len(self.ref)):
            entry = QgsRasterCalculatorEntry()
            entry.ref = self.ref[index]
            entry.bandNumber = 1
            entry.raster = self.findRaster(entry.ref)
            width.append(entry.raster.width())
            height.append(entry.raster.height())
            entries.append(entry)

        calc = QgsRasterCalculator(formula, self.save_path, 'GTiff', rlayer.extent(), min(width), min(height), entries)
        callback = calc.processCalculation()
        self.return_info(callback)

    def action_load_path(self):
        file_choose, file_type = QFileDialog.getSaveFileName(self, "Raster Saving", "./processImage/", "Tiff Files (*.tif)")
        self.save_path = file_choose
        self.lineEdit.setText(self.save_path)
        self.runButton.setEnabled(True)

    def get_cursor(self):
        tc = self.textEdit.textCursor()
        return tc.position()

    def return_info(self, msg):
        if msg == 0:
            QMessageBox.information(self, 'Callback', 'Success!', QMessageBox.Yes)
            self.result = QgsRasterLayer(self.save_path, (self.save_path.split('/')[-1]).split('.')[0])
            #os.remove(self.save_path)
            self.success = True
            self.loadmap = True
            self.mySignal.emit(1)
            self.close()
        elif msg == 1:
            QMessageBox.critical(self, 'Error', 'Create Output Error!', QMessageBox.Yes)
        elif msg == 2:
            QMessageBox.critical(self, 'Error', 'Input Layer Error!', QMessageBox.Yes)
        elif msg == 3:
            QMessageBox.warning(self, 'Warning', 'Canceled', QMessageBox.Yes)
        elif msg == 4:
            QMessageBox.critical(self, 'Error', 'Parser Error!', QMessageBox.Yes)
        elif msg == 5:
            QMessageBox.critical(self, 'Error', 'Memory Error!', QMessageBox.Yes)
        elif msg == 6:
            QMessageBox.critical(self, 'Error', 'Band Error!', QMessageBox.Yes)
        elif msg == 7:
            QMessageBox.critical(self, 'Error', 'Calculation Error!', QMessageBox.Yes)

