from PyQt5 import QtCore, QtGui, QtWidgets
__author__ = 'Gareth Mok'


class AddRemoveAccountGroup(QtGui.QDialog):
    def __init__(self, names, remove, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.name = ''
        self.start_date = ''
        self.account_group_type = ''

        self.clearFocus()
        self.frameOptional.setDisabled(remove)
        self.combo_Account_Names.setEditable(not remove)
        for name in names:
            self.combo_Account_Names.addItem(name)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.btn_accepted_clicked)

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
        
        self.gridLayoutMain = QtWidgets.QGridLayout()
        self.gridLayoutMain.setObjectName("gridLayoutMain")
        self.frameOptional = QtWidgets.QFrame(Dialog)
        self.frameOptional.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameOptional.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameOptional.setObjectName("frameOptional")
        self.gridLayoutOptional = QtWidgets.QGridLayout(self.frameOptional)
        self.gridLayoutOptional.setObjectName("gridLayoutOptional")
        self.startDateGroup = QtWidgets.QGroupBox(self.frameOptional)
        self.startDateGroup.setObjectName("startDateGroup")
        
        self.lin_Start_Date = QtWidgets.QLineEdit(self.startDateGroup)
        self.lin_Start_Date.setGeometry(QtCore.QRect(10, 20, 281, 21))
        self.lin_Start_Date.setObjectName("lin_Start_Date")
        self.gridLayoutOptional.addWidget(self.startDateGroup, 0, 0, 1, 1)
        
        self.radioGroup = QtWidgets.QGroupBox(self.frameOptional)
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
        self.gridLayoutOptional.addWidget(self.radioGroup, 1, 0, 1, 1)
        self.gridLayoutMain.addWidget(self.frameOptional, 1, 0, 1, 1)
        
        self.accountNameGroup = QtWidgets.QGroupBox(Dialog)
        self.accountNameGroup.setObjectName("accountNameGroup")
        self.combo_Account_Names = QtWidgets.QComboBox(self.accountNameGroup)
        self.combo_Account_Names.setGeometry(QtCore.QRect(20, 70, 280, 22))
        self.combo_Account_Names.setEditable(True)
        self.combo_Account_Names.setObjectName("combo_Account_Names")
        self.gridLayoutMain.addWidget(self.accountNameGroup, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayoutMain, 0, 0, 1, 1)

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
        self.accountNameGroup.setTitle(_translate("Dialog", "Account Name"))
        self.startDateGroup.setTitle(_translate("Dialog", "Start Date"))
        self.lin_Start_Date.setPlaceholderText(_translate("Dialog", "Input Start Date in YYYY-MM format"))
        self.radioGroup.setTitle(_translate("Dialog", "Account Group Type"))
        self.radio_Monthly.setToolTip(_translate("Dialog", "<html><head/><body><p>Dates are in &quot;MM/YYYY&quot; form</p></body></html>"))
        self.radio_Monthly.setText(_translate("Dialog", "Monthly"))
        self.radio_Quarterly.setToolTip(_translate("Dialog", "<html><head/><body><p>Dates are in &quot;QQ YYYY&quot; form</p></body></html>"))
        self.radio_Quarterly.setText(_translate("Dialog", "Quarterly"))
        self.radio_Yearly.setToolTip(_translate("Dialog", "<html><head/><body><p>Dates are in &quot;YYYY&quot; form</p></body></html>"))
        self.radio_Yearly.setText(_translate("Dialog", "Yearly"))

    def btn_accepted_clicked(self):
        self.name = self.combo_Account_Names.currentText()
        self.start_date = self.lin_Start_Date.text()
        if self.radio_Monthly.isChecked():
            self.account_group_type = 'Monthly'
        elif self.radio_Quarterly.isChecked():
            self.account_group_type = 'Quarterly'
        elif self.radio_Yearly.isChecked():
            self.account_group_type = 'Yearly'

    @staticmethod
    def get_account_group_details(names, remove=False, parent=None):
        """
        ok, name, link, last = Select.select_result()
        :param parent:
        :return:
        """
        dialog = AddRemoveAccountGroup(names, remove, parent)
        result = dialog.exec_()

        return dialog.name, dialog.start_date, dialog.account_group_type, result == QtGui.QDialog.Accepted
