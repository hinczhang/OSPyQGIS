# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dlg_jiaodian.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Dlg_jiaodian_class(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(746, 557)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(390, 480, 121, 31))
        self.pushButton.setObjectName("pushButton")
        self.comboBox_r = QtWidgets.QComboBox(Dialog)
        self.comboBox_r.setGeometry(QtCore.QRect(90, 50, 541, 22))
        self.comboBox_r.setObjectName("comboBox_r")
        self.comboBox_g = QtWidgets.QComboBox(Dialog)
        self.comboBox_g.setGeometry(QtCore.QRect(90, 130, 541, 22))
        self.comboBox_g.setObjectName("comboBox_g")
        self.comboBox_b = QtWidgets.QComboBox(Dialog)
        self.comboBox_b.setGeometry(QtCore.QRect(90, 210, 541, 22))
        self.comboBox_b.setObjectName("comboBox_b")
        self.label_r = QtWidgets.QLabel(Dialog)
        self.label_r.setGeometry(QtCore.QRect(90, 20, 72, 15))
        self.label_r.setObjectName("label_r")
        self.label_g = QtWidgets.QLabel(Dialog)
        self.label_g.setGeometry(QtCore.QRect(90, 100, 72, 15))
        self.label_g.setObjectName("label_g")
        self.label_b = QtWidgets.QLabel(Dialog)
        self.label_b.setGeometry(QtCore.QRect(90, 180, 72, 15))
        self.label_b.setObjectName("label_b")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(90, 490, 241, 19))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(530, 480, 121, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(90, 430, 71, 21))
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setObjectName("label")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(590, 430, 41, 21))
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit_name = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_name.setGeometry(QtCore.QRect(210, 430, 351, 21))
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.label_b_2 = QtWidgets.QLabel(Dialog)
        self.label_b_2.setGeometry(QtCore.QRect(90, 260, 72, 15))
        self.label_b_2.setObjectName("label_b_2")
        self.comboBox_fangfa = QtWidgets.QComboBox(Dialog)
        self.comboBox_fangfa.setGeometry(QtCore.QRect(90, 290, 541, 22))
        self.comboBox_fangfa.setObjectName("comboBox_fangfa")
        self.comboBox_daxiao = QtWidgets.QComboBox(Dialog)
        self.comboBox_daxiao.setGeometry(QtCore.QRect(90, 370, 421, 22))
        self.comboBox_daxiao.setObjectName("comboBox_daxiao")
        self.label_b_3 = QtWidgets.QLabel(Dialog)
        self.label_b_3.setGeometry(QtCore.QRect(90, 340, 72, 15))
        self.label_b_3.setObjectName("label_b_3")
        self.checkBox_2 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_2.setGeometry(QtCore.QRect(560, 370, 91, 19))
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName("checkBox_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "执行"))
        self.label_r.setText(_translate("Dialog", "R波段"))
        self.label_g.setText(_translate("Dialog", "G波段"))
        self.label_b.setText(_translate("Dialog", "B波段"))
        self.checkBox.setText(_translate("Dialog", "是否在完成后加入到图层中"))
        self.pushButton_2.setText(_translate("Dialog", "取消"))
        self.label.setText(_translate("Dialog", "保存位置"))
        self.pushButton_3.setText(_translate("Dialog", "..."))
        self.label_b_2.setText(_translate("Dialog", "统计方法"))
        self.label_b_3.setText(_translate("Dialog", "区域大小"))
        self.checkBox_2.setText(_translate("Dialog", "Resize"))
