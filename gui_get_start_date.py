from PyQt5 import QtCore, QtGui, QtWidgets
__author__ = 'Gareth Mok'


class GetStartDate(QtGui.QDialog):
    def __init__(self, date_placeholder_text, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.date = ''

        self.lin_Start_Date.setPlaceholderText(date_placeholder_text)
        self.clearFocus()
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.btn_accepted_clicked)

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
        self.startDateGroup = QtWidgets.QGroupBox(Dialog)
        self.startDateGroup.setObjectName("startDateGroup")
        self.lin_Start_Date = QtWidgets.QLineEdit(self.startDateGroup)
        self.lin_Start_Date.setGeometry(QtCore.QRect(10, 20, 281, 21))
        self.lin_Start_Date.setObjectName("lin_Start_Date")
        self.gridLayout_3.addWidget(self.startDateGroup, 1, 0, 1, 1)
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
        Dialog.setTabOrder(self.lin_Start_Date, self.buttonBox)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Get Database Start Date"))
        self.startDateGroup.setTitle(_translate("Dialog", "Start Date"))
        self.lin_Start_Date.setPlaceholderText(_translate("Dialog", "Input Start Date in YYYY-MM format"))

    def btn_accepted_clicked(self):
        self.date = self.lin_Start_Date.text()

    @staticmethod
    def get_start_date(date_placeholder_text, parent=None):
        """
        ok, name, link, last = Select.select_result()
        :param parent:
        :return:
        """
        dialog = GetStartDate(date_placeholder_text, parent)
        result = dialog.exec_()

        return dialog.date, result == QtGui.QDialog.Accepted
