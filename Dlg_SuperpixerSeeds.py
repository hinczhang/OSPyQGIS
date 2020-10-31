# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dlg_SuperpixerSeeds.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(560, 567)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 521, 544))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_r = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_r.setObjectName("label_r")
        self.verticalLayout.addWidget(self.label_r)
        self.comboBox_r = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_r.setObjectName("comboBox_r")
        self.verticalLayout.addWidget(self.comboBox_r)
        self.label_g = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_g.setObjectName("label_g")
        self.verticalLayout.addWidget(self.label_g)
        self.comboBox_g = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_g.setObjectName("comboBox_g")
        self.verticalLayout.addWidget(self.comboBox_g)
        self.label_b = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_b.setObjectName("label_b")
        self.verticalLayout.addWidget(self.label_b)
        self.comboBox_b = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_b.setObjectName("comboBox_b")
        self.verticalLayout.addWidget(self.comboBox_b)
        self.label_num_superpixers = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_num_superpixers.setObjectName("label_num_superpixers")
        self.verticalLayout.addWidget(self.label_num_superpixers)
        self.spinBox_num_superpixers = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_num_superpixers.setMinimum(1)
        self.spinBox_num_superpixers.setMaximum(99999999)
        self.spinBox_num_superpixers.setProperty("value", 500)
        self.spinBox_num_superpixers.setObjectName("spinBox_num_superpixers")
        self.verticalLayout.addWidget(self.spinBox_num_superpixers)
        self.label_levels = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_levels.setObjectName("label_levels")
        self.verticalLayout.addWidget(self.label_levels)
        self.spinBox_levels = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_levels.setMinimum(1)
        self.spinBox_levels.setProperty("value", 15)
        self.spinBox_levels.setObjectName("spinBox_levels")
        self.verticalLayout.addWidget(self.spinBox_levels)
        self.label_histogram_bins = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_histogram_bins.setObjectName("label_histogram_bins")
        self.verticalLayout.addWidget(self.label_histogram_bins)
        self.spinBox_historam_bins = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_historam_bins.setMinimum(1)
        self.spinBox_historam_bins.setProperty("value", 5)
        self.spinBox_historam_bins.setObjectName("spinBox_historam_bins")
        self.verticalLayout.addWidget(self.spinBox_historam_bins)
        self.label_num = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_num.setObjectName("label_num")
        self.verticalLayout.addWidget(self.label_num)
        self.spinBox_num = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_num.setMinimum(1)
        self.spinBox_num.setProperty("value", 10)
        self.spinBox_num.setObjectName("spinBox_num")
        self.verticalLayout.addWidget(self.spinBox_num)
        self.label_name = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_name.setObjectName("label_name")
        self.verticalLayout.addWidget(self.label_name)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_name = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.horizontalLayout.addWidget(self.lineEdit_name)
        self.pushButton_name = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_name.setObjectName("pushButton_name")
        self.horizontalLayout.addWidget(self.pushButton_name)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_null = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_null.setText("")
        self.label_null.setObjectName("label_null")
        self.verticalLayout.addWidget(self.label_null)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_2.addWidget(self.checkBox)
        self.pushButton_ok = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout_2.addWidget(self.pushButton_ok)
        self.pushButton_cancel = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout_2.addWidget(self.pushButton_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_r.setText(_translate("Dialog", "R波段"))
        self.label_g.setText(_translate("Dialog", "G波段"))
        self.label_b.setText(_translate("Dialog", "B波段"))
        self.label_num_superpixers.setText(_translate("Dialog", "期望超像素数目"))
        self.label_levels.setText(_translate("Dialog", "块级别数"))
        self.label_histogram_bins.setText(_translate("Dialog", "直方图bins"))
        self.label_num.setText(_translate("Dialog", "迭代次数"))
        self.label_name.setText(_translate("Dialog", "保存位置"))
        self.pushButton_name.setText(_translate("Dialog", "选择位置"))
        self.checkBox.setText(_translate("Dialog", "是否在完成后加入到图层中"))
        self.pushButton_ok.setText(_translate("Dialog", "执行"))
        self.pushButton_cancel.setText(_translate("Dialog", "取消"))

