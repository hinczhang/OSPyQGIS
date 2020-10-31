# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dlg_clip.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(729, 644)
        self.plainTextEdit_y0 = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit_y0.setGeometry(QtCore.QRect(310, 120, 81, 31))
        self.plainTextEdit_y0.setObjectName("plainTextEdit_y0")
        self.plainTextEdit_x1 = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit_x1.setGeometry(QtCore.QRect(600, 290, 81, 31))
        self.plainTextEdit_x1.setObjectName("plainTextEdit_x1")
        self.plainTextEdit_y1 = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit_y1.setGeometry(QtCore.QRect(310, 490, 81, 31))
        self.plainTextEdit_y1.setObjectName("plainTextEdit_y1")
        self.plainTextEdit_x0 = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit_x0.setGeometry(QtCore.QRect(30, 290, 81, 31))
        self.plainTextEdit_x0.setObjectName("plainTextEdit_x0")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(139, 169, 431, 301))
        self.widget.setObjectName("widget")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(370, 580, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.comboBox_selectlayer = QtWidgets.QComboBox(Dialog)
        self.comboBox_selectlayer.setGeometry(QtCore.QRect(110, 60, 501, 31))
        self.comboBox_selectlayer.setObjectName("comboBox_selectlayer")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(110, 30, 161, 16))
        self.label.setObjectName("label")
        self.pushButton_show = QtWidgets.QPushButton(Dialog)
        self.pushButton_show.setGeometry(QtCore.QRect(230, 580, 93, 28))
        self.pushButton_show.setObjectName("pushButton_show")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(140, 540, 211, 19))
        self.checkBox.setObjectName("checkBox")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(270, 120, 31, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(270, 490, 31, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(610, 250, 31, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(40, 250, 31, 31))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "RasterClip"))
        self.plainTextEdit_y0.setPlainText(_translate("Dialog", "0"))
        self.plainTextEdit_x1.setPlainText(_translate("Dialog", "500"))
        self.plainTextEdit_y1.setPlainText(_translate("Dialog", "500"))
        self.plainTextEdit_x0.setPlainText(_translate("Dialog", "0"))
        self.pushButton.setText(_translate("Dialog", "process"))
        self.label.setText(_translate("Dialog", "Layer to clip"))
        self.pushButton_show.setText(_translate("Dialog", "show"))
        self.checkBox.setText(_translate("Dialog", "add to main window"))
        self.label_2.setText(_translate("Dialog", "y0"))
        self.label_3.setText(_translate("Dialog", "y1"))
        self.label_4.setText(_translate("Dialog", "x1"))
        self.label_5.setText(_translate("Dialog", "x0"))
