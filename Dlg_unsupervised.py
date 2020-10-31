# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dlg_unsupervised.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dlg_unsupervised(object):
    def setupUi(self, Dlg_unsupervised):
        Dlg_unsupervised.setObjectName("Dlg_unsupervised")
        Dlg_unsupervised.resize(691, 658)
        self.label_g = QtWidgets.QLabel(Dlg_unsupervised)
        self.label_g.setGeometry(QtCore.QRect(140, 160, 72, 15))
        self.label_g.setObjectName("label_g")
        self.label_b = QtWidgets.QLabel(Dlg_unsupervised)
        self.label_b.setGeometry(QtCore.QRect(140, 240, 72, 15))
        self.label_b.setObjectName("label_b")
        self.pushButton = QtWidgets.QPushButton(Dlg_unsupervised)
        self.pushButton.setGeometry(QtCore.QRect(280, 580, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.comboBox_r = QtWidgets.QComboBox(Dlg_unsupervised)
        self.comboBox_r.setGeometry(QtCore.QRect(140, 100, 431, 22))
        self.comboBox_r.setObjectName("comboBox_r")
        self.label_r = QtWidgets.QLabel(Dlg_unsupervised)
        self.label_r.setGeometry(QtCore.QRect(140, 70, 72, 15))
        self.label_r.setObjectName("label_r")
        self.comboBox_b = QtWidgets.QComboBox(Dlg_unsupervised)
        self.comboBox_b.setGeometry(QtCore.QRect(140, 270, 431, 22))
        self.comboBox_b.setObjectName("comboBox_b")
        self.comboBox_g = QtWidgets.QComboBox(Dlg_unsupervised)
        self.comboBox_g.setGeometry(QtCore.QRect(140, 190, 431, 22))
        self.comboBox_g.setObjectName("comboBox_g")
        self.lineEdit = QtWidgets.QLineEdit(Dlg_unsupervised)
        self.lineEdit.setGeometry(QtCore.QRect(140, 380, 113, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_b_2 = QtWidgets.QLabel(Dlg_unsupervised)
        self.label_b_2.setGeometry(QtCore.QRect(140, 350, 111, 16))
        self.label_b_2.setObjectName("label_b_2")
        self.label_b_3 = QtWidgets.QLabel(Dlg_unsupervised)
        self.label_b_3.setGeometry(QtCore.QRect(400, 350, 111, 16))
        self.label_b_3.setObjectName("label_b_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dlg_unsupervised)
        self.lineEdit_2.setGeometry(QtCore.QRect(400, 380, 113, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_b_4 = QtWidgets.QLabel(Dlg_unsupervised)
        self.label_b_4.setGeometry(QtCore.QRect(260, 440, 161, 16))
        self.label_b_4.setObjectName("label_b_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dlg_unsupervised)
        self.lineEdit_3.setGeometry(QtCore.QRect(270, 480, 113, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.retranslateUi(Dlg_unsupervised)
        QtCore.QMetaObject.connectSlotsByName(Dlg_unsupervised)

    def retranslateUi(self, Dlg_unsupervised):
        _translate = QtCore.QCoreApplication.translate
        Dlg_unsupervised.setWindowTitle(_translate("Dlg_unsupervised", "非监督分类"))
        self.label_g.setText(_translate("Dlg_unsupervised", "G波段"))
        self.label_b.setText(_translate("Dlg_unsupervised", "B波段"))
        self.pushButton.setText(_translate("Dlg_unsupervised", "确定"))
        self.label_r.setText(_translate("Dlg_unsupervised", "R波段"))
        self.label_b_2.setText(_translate("Dlg_unsupervised", "输入迭代次数"))
        self.label_b_3.setText(_translate("Dlg_unsupervised", "输入精确度"))
        self.label_b_4.setText(_translate("Dlg_unsupervised", "输入聚类的最终数目"))
