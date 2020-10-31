# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rasterpathUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(606, 581)
        self.rasterBox = QtWidgets.QComboBox(Dialog)
        self.rasterBox.setGeometry(QtCore.QRect(140, 40, 421, 31))
        self.rasterBox.setObjectName("rasterBox")
        self.box_scale = QtWidgets.QPlainTextEdit(Dialog)
        self.box_scale.setGeometry(QtCore.QRect(140, 110, 421, 31))
        self.box_scale.setObjectName("box_scale")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(140, 170, 41, 31))
        self.label.setStyleSheet("font: 16pt \"Arial\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(270, 170, 41, 31))
        self.label_2.setStyleSheet("font: 16pt \"Arial\";")
        self.label_2.setObjectName("label_2")
        self.x_Box = QtWidgets.QSpinBox(Dialog)
        self.x_Box.setGeometry(QtCore.QRect(180, 170, 71, 31))
        self.x_Box.setObjectName("x_Box")
        self.y_Box = QtWidgets.QSpinBox(Dialog)
        self.y_Box.setGeometry(QtCore.QRect(310, 170, 71, 31))
        self.y_Box.setObjectName("y_Box")
        self.runButton = QtWidgets.QPushButton(Dialog)
        self.runButton.setGeometry(QtCore.QRect(460, 530, 93, 28))
        self.runButton.setObjectName("runButton")
        self.graphicsView = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView.setGeometry(QtCore.QRect(30, 220, 531, 291))
        self.graphicsView.setObjectName("graphicsView")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 40, 101, 31))
        self.label_3.setStyleSheet("font: 14pt \"Arial\";")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 110, 101, 31))
        self.label_4.setStyleSheet("font: 14pt \"Arial\";")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 170, 101, 31))
        self.label_5.setStyleSheet("font: 14pt \"Arial\";")
        self.label_5.setObjectName("label_5")
        self.pathEdit = QtWidgets.QLineEdit(Dialog)
        self.pathEdit.setGeometry(QtCore.QRect(30, 530, 361, 31))
        self.pathEdit.setObjectName("pathEdit")
        self.chooseButton = QtWidgets.QPushButton(Dialog)
        self.chooseButton.setGeometry(QtCore.QRect(400, 530, 31, 31))
        self.chooseButton.setObjectName("chooseButton")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(400, 170, 81, 31))
        self.label_6.setStyleSheet("font: 16pt \"Arial\";")
        self.label_6.setObjectName("label_6")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(490, 170, 71, 31))
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "X:"))
        self.label_2.setText(_translate("Dialog", "Y:"))
        self.runButton.setText(_translate("Dialog", "RUN"))
        self.label_3.setText(_translate("Dialog", "选择DEM"))
        self.label_4.setText(_translate("Dialog", "DEM长宽"))
        self.label_5.setText(_translate("Dialog", "起始点"))
        self.chooseButton.setText(_translate("Dialog", "..."))
        self.label_6.setText(_translate("Dialog", "Value:"))
