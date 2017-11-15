from PyQt5 import QtGui

__author__ = 'Gareth Mok'


def date_serializer(database_type, input_date):
    """
    Takes a parsed string from date_parser and converts it into a string of the %Y-%m format
    :type database_type: str
    :type input_date: str
    :param database_type: database types - 'Monthly', 'Quarterly', or 'Yearly'
    :param input_date: date formatted in the below fashion
            MM/YYYY format for 'Monthly' type
            QQ YYYY format for 'Quarterly' type
            YYYY format for 'Yearly' type
    :return: string date of the date format %Y-%m
    """
    database_types = ['Monthly', 'Quarterly', 'Yearly']
    if database_type not in database_types:
        raise ValueError('Value Error: Invalid type. Type must be "Monthly", "Quarterly", or "Yearly"')

    if database_type == "Monthly":
        month, year = input_date.split("/")
        return '{0}-{1}'.format(year, month)
    elif database_type == "Quarterly":
        quarter, year = input_date.split(" ")
        month = int(quarter[1]) * 3 - 1
        return '{0}-{1:02d}'.format(year, month)
    elif database_type == "Yearly":
        return '{0}-{1:02d}'.format(input_date, 1)


def date_placeholder_text(database_type):
    """
    Returns the appropriate placeholder text depending on the database type
    :return: a string for the place holder text
    """
    database_types = ['Monthly', 'Quarterly', 'Yearly']
    if database_type not in database_types:
        raise ValueError('Value Error: Invalid type. Type must be "Monthly", "Quarterly", or "Yearly"')
    if database_type == 'Monthly':
        return 'Input Start Date in MM/YYYY format'
    elif database_type == 'Quarterly':
        return 'Input Start Date in QQ YYYY format'
    elif database_type == 'Yearly':
        return 'Input Start Date in YYYY format'


def error_message(err_msg):
    msg = QtGui.QMessageBox()
    msg.setIcon(QtGui.QMessageBox.Critical)
    msg.setText("Error when running utility.")
    msg.setInformativeText(str(err_msg))
    msg.setWindowTitle("Error Message")
    msg.setStandardButtons(QtGui.QMessageBox.Ok)

    msg.exec_()