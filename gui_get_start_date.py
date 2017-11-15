from PyQt5 import QtGui, uic
__author__ = 'Gareth Mok'

form_import = uic.loadUiType('get_start_date.ui')[0]


class GetStartDate(QtGui.QDialog, form_import):
    def __init__(self, date_placeholder_text, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.date = ''

        self.lin_Start_Date.setPlaceholderText(date_placeholder_text)
        self.clearFocus()
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.btn_accepted_clicked)

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
