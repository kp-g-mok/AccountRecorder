# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'get_database_type.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 240)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3.addWidget(self.frame_2, 2, 0, 1, 1)
        self.radioGroup = QtWidgets.QGroupBox(Dialog)
        self.radioGroup.setObjectName("radioGroup")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.radioGroup)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 19, 281, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radio_Monthly = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radio_Monthly.setChecked(True)
        self.radio_Monthly.setObjectName("radio_Monthly")
        self.horizontalLayout.addWidget(self.radio_Monthly)
        self.radio_Quarterly = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radio_Quarterly.setObjectName("radio_Quarterly")
        self.horizontalLayout.addWidget(self.radio_Quarterly)
        self.radio_Yearly = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radio_Yearly.setObjectName("radio_Yearly")
        self.horizontalLayout.addWidget(self.radio_Yearly)
        self.gridLayout_3.addWidget(self.radioGroup, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.radio_Monthly, self.radio_Quarterly)
        Dialog.setTabOrder(self.radio_Quarterly, self.radio_Yearly)
        Dialog.setTabOrder(self.radio_Yearly, self.buttonBox)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Get Database Start Date"))
        self.radioGroup.setTitle(_translate("Dialog", "Database Type"))
        self.radio_Monthly.setToolTip(_translate("Dialog", "<html><head/><body><p>Dates are in &quot;MM/YYYY&quot; form</p></body></html>"))
        self.radio_Monthly.setText(_translate("Dialog", "Monthly"))
        self.radio_Quarterly.setToolTip(_translate("Dialog", "<html><head/><body><p>Dates are in &quot;QQ YYYY&quot; form</p></body></html>"))
        self.radio_Quarterly.setText(_translate("Dialog", "Quarterly"))
        self.radio_Yearly.setToolTip(_translate("Dialog", "<html><head/><body><p>Dates are in &quot;YYYY&quot; form</p></body></html>"))
        self.radio_Yearly.setText(_translate("Dialog", "Yearly"))

