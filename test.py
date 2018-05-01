# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_remove_account.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(340, 320)
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
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.startDateGroup = QtWidgets.QGroupBox(self.frame_2)
        self.startDateGroup.setObjectName("startDateGroup")
        self.lin_Start_Date = QtWidgets.QLineEdit(self.startDateGroup)
        self.lin_Start_Date.setGeometry(QtCore.QRect(10, 20, 281, 21))
        self.lin_Start_Date.setObjectName("lin_Start_Date")
        self.gridLayout_2.addWidget(self.startDateGroup, 0, 0, 1, 1)
        self.radioGroup = QtWidgets.QGroupBox(self.frame_2)
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
        self.gridLayout_2.addWidget(self.radioGroup, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame_2, 1, 0, 1, 1)
        self.accountNameGroup = QtWidgets.QGroupBox(Dialog)
        self.accountNameGroup.setObjectName("accountNameGroup")
        self.combo_Account_Names = QtWidgets.QComboBox(self.accountNameGroup)
        self.combo_Account_Names.setGeometry(QtCore.QRect(20, 70, 280, 22))
        self.combo_Account_Names.setEditable(True)
        self.combo_Account_Names.setObjectName("combo_Account_Names")
        self.gridLayout_3.addWidget(self.accountNameGroup, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.combo_Account_Names, self.lin_Start_Date)
        Dialog.setTabOrder(self.lin_Start_Date, self.radio_Monthly)
        Dialog.setTabOrder(self.radio_Monthly, self.radio_Quarterly)
        Dialog.setTabOrder(self.radio_Quarterly, self.radio_Yearly)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Get Account Details"))
        self.startDateGroup.setTitle(_translate("Dialog", "Start Date"))
        self.lin_Start_Date.setPlaceholderText(_translate("Dialog", "Input Start Date in YYYY-MM format"))
        self.radioGroup.setTitle(_translate("Dialog", "Database Type"))
        self.radio_Monthly.setToolTip(_translate("Dialog", "<html><head/><body><p>Dates are in &quot;MM/YYYY&quot; form</p></body></html>"))
        self.radio_Monthly.setText(_translate("Dialog", "Monthly"))
        self.radio_Quarterly.setToolTip(_translate("Dialog", "<html><head/><body><p>Dates are in &quot;QQ YYYY&quot; form</p></body></html>"))
        self.radio_Quarterly.setText(_translate("Dialog", "Quarterly"))
        self.radio_Yearly.setToolTip(_translate("Dialog", "<html><head/><body><p>Dates are in &quot;YYYY&quot; form</p></body></html>"))
        self.radio_Yearly.setText(_translate("Dialog", "Yearly"))
        self.accountNameGroup.setTitle(_translate("Dialog", "Account Name"))
