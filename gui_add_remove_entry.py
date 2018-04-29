from PyQt5 import QtCore, QtGui, uic
__author__ = 'Gareth Mok'

form_import = uic.loadUiType('add_remove_entry.ui')[0]


class AddRemoveEntry(QtGui.QDialog, form_import):
    def __init__(self, names, remove, date_placeholder_text, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.name = ''
        self.date = ''
        self.money = ''

        self.lin_Money_Value.setDisabled(remove)
        for name in names:
            self.combo_Account_Names.addItem(name)
        self.lin_Entry_Date.setPlaceholderText(date_placeholder_text)
        self.clearFocus()
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.btn_accepted_clicked)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 320)
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
        self.entryDateGroup = QtWidgets.QGroupBox(Dialog)
        self.entryDateGroup.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.entryDateGroup.setFlat(False)
        self.entryDateGroup.setCheckable(False)
        self.entryDateGroup.setObjectName("entryDateGroup")
        self.lin_Entry_Date = QtWidgets.QLineEdit(self.entryDateGroup)
        self.lin_Entry_Date.setGeometry(QtCore.QRect(50, 20, 331, 21))
        self.lin_Entry_Date.setObjectName("lin_Entry_Date")
        self.gridLayout_3.addWidget(self.entryDateGroup, 3, 0, 1, 1)
        self.accountNameGroup = QtWidgets.QGroupBox(Dialog)
        self.accountNameGroup.setObjectName("accountNameGroup")
        self.combo_Account_Names = QtWidgets.QComboBox(self.accountNameGroup)
        self.combo_Account_Names.setGeometry(QtCore.QRect(50, 20, 331, 22))
        self.combo_Account_Names.setEditable(False)
        self.combo_Account_Names.setObjectName("combo_Account_Names")
        self.gridLayout_3.addWidget(self.accountNameGroup, 2, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3.addWidget(self.frame_2, 5, 0, 1, 1)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_3.addWidget(self.frame, 1, 0, 1, 1)
        self.moneyGroup = QtWidgets.QGroupBox(Dialog)
        self.moneyGroup.setObjectName("moneyGroup")
        self.lin_Money_Value = QtWidgets.QLineEdit(self.moneyGroup)
        self.lin_Money_Value.setGeometry(QtCore.QRect(50, 20, 331, 21))
        self.lin_Money_Value.setObjectName("lin_Money_Value")
        self.gridLayout_3.addWidget(self.moneyGroup, 4, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.combo_Account_Names, self.lin_Entry_Date)
        Dialog.setTabOrder(self.lin_Entry_Date, self.lin_Money_Value)
        Dialog.setTabOrder(self.lin_Money_Value, self.buttonBox)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Import Item"))
        self.entryDateGroup.setTitle(_translate("Dialog", "Entry Date"))
        self.lin_Entry_Date.setPlaceholderText(_translate("Dialog", "Input Date in YYYY-MM format"))
        self.accountNameGroup.setTitle(_translate("Dialog", "Account Name"))
        self.moneyGroup.setTitle(_translate("Dialog", "Entry Monetary Value"))
        self.lin_Money_Value.setPlaceholderText(_translate("Dialog", "Input the Entry Monetary Value"))

    def btn_accepted_clicked(self):
        self.name = self.combo_Account_Names.currentText()
        self.date = self.lin_Entry_Date.text()
        self.money = self.lin_Money_Value.text()

    @staticmethod
    def get_entry_details(names, remove, date_placeholder_text, parent=None):
        """
        ok, name, link, last = Select.select_result()
        :param parent:
        :return:
        """
        dialog = AddRemoveEntry(names, remove, date_placeholder_text, parent)
        result = dialog.exec_()
        return dialog.name, dialog.date, dialog.money, result == QtGui.QDialog.Accepted
