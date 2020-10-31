# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dlg_cornerDetection.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(729, 565)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(330, 250, 281, 171))
        self.widget.setObjectName("widget")
        self.comboBox_selectlayer = QtWidgets.QComboBox(Dialog)
        self.comboBox_selectlayer.setGeometry(QtCore.QRect(110, 60, 501, 31))
        self.comboBox_selectlayer.setObjectName("comboBox_selectlayer")
        self.plainTextEdit_coef_1 = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit_coef_1.setGeometry(QtCore.QRect(210, 250, 81, 31))
        self.plainTextEdit_coef_1.setObjectName("plainTextEdit_coef_1")
        self.plainTextEdit_coef_2 = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit_coef_2.setGeometry(QtCore.QRect(210, 320, 81, 31))
        self.plainTextEdit_coef_2.setObjectName("plainTextEdit_coef_2")
        self.comboBox_selectmethod = QtWidgets.QComboBox(Dialog)
        self.comboBox_selectmethod.setGeometry(QtCore.QRect(110, 150, 501, 31))
        self.comboBox_selectmethod.setObjectName("comboBox_selectmethod")
        self.plainTextEdit_coef_3 = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit_coef_3.setGeometry(QtCore.QRect(210, 390, 81, 31))
        self.plainTextEdit_coef_3.setObjectName("plainTextEdit_coef_3")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(110, 30, 72, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(110, 120, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(110, 210, 151, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(330, 210, 72, 15))
        self.label_4.setObjectName("label_4")
        self.label_coef_1 = QtWidgets.QLabel(Dialog)
        self.label_coef_1.setGeometry(QtCore.QRect(110, 260, 72, 15))
        self.label_coef_1.setObjectName("label_coef_1")
        self.label_coef_2 = QtWidgets.QLabel(Dialog)
        self.label_coef_2.setGeometry(QtCore.QRect(110, 330, 72, 15))
        self.label_coef_2.setObjectName("label_coef_2")
        self.label_coef_3 = QtWidgets.QLabel(Dialog)
        self.label_coef_3.setGeometry(QtCore.QRect(110, 400, 72, 15))
        self.label_coef_3.setObjectName("label_coef_3")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(110, 450, 231, 19))
        self.checkBox.setObjectName("checkBox")
        self.pushButton_process = QtWidgets.QPushButton(Dialog)
        self.pushButton_process.setGeometry(QtCore.QRect(350, 500, 93, 28))
        self.pushButton_process.setObjectName("pushButton_process")
        self.pushButton_show = QtWidgets.QPushButton(Dialog)
        self.pushButton_show.setGeometry(QtCore.QRect(230, 500, 93, 28))
        self.pushButton_show.setObjectName("pushButton_show")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "CornerDetection"))
        self.plainTextEdit_coef_1.setPlainText(_translate("Dialog", "2"))
        self.plainTextEdit_coef_2.setPlainText(_translate("Dialog", "3"))
        self.plainTextEdit_coef_3.setPlainText(_translate("Dialog", "0.04"))
        self.label.setText(_translate("Dialog", "Layer"))
        self.label_2.setText(_translate("Dialog", "Method"))
        self.label_3.setText(_translate("Dialog", "Coef Settings"))
        self.label_4.setText(_translate("Dialog", "Preview"))
        self.label_coef_1.setText(_translate("Dialog", "blocksize"))
        self.label_coef_2.setText(_translate("Dialog", "ksize"))
        self.label_coef_3.setText(_translate("Dialog", "k"))
        self.checkBox.setText(_translate("Dialog", "Add to Main Window"))
        self.pushButton_process.setText(_translate("Dialog", "process"))
        self.pushButton_show.setText(_translate("Dialog", "show"))
