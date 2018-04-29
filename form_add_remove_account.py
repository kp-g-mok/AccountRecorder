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
        self.check_Skip_Total = QtWidgets.QCheckBox(self.frame_2)
        self.check_Skip_Total.setGeometry(QtCore.QRect(10, 10, 271, 41))
        self.check_Skip_Total.setObjectName("check_Skip_Total")
        self.gridLayout_3.addWidget(self.frame_2, 2, 0, 1, 1)
        self.accountNameGroup = QtWidgets.QGroupBox(Dialog)
        self.accountNameGroup.setObjectName("accountNameGroup")
        self.combo_Account_Names = QtWidgets.QComboBox(self.accountNameGroup)
        self.combo_Account_Names.setGeometry(QtCore.QRect(10, 20, 280, 22))
        self.combo_Account_Names.setEditable(True)
        self.combo_Account_Names.setObjectName("combo_Account_Names")
        self.gridLayout_3.addWidget(self.accountNameGroup, 1, 0, 1, 1)
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
        Dialog.setTabOrder(self.check_Skip_Total, self.buttonBox)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Get Account Details"))
        self.check_Skip_Total.setText(_translate("Dialog", "Skip Account from Total?"))
        self.accountNameGroup.setTitle(_translate("Dialog", "Account Name"))

