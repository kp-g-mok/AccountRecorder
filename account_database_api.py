import json
import os

import datetime

__author__ = 'Gareth Mok'


class Account:
    def __init__(self, filepath, database_type=None, start_date=None):
        """
        Headers are Account Names and variable
        :type filepath: str
        :type database_type: str
        :type start_date: str in %Y-%m format
        :param filepath: filepath path location
        :param database_type: database type: 'Monthly', 'Quarterly' or 'Yearly'
        :param start_date: Beginning date for the database
        :return:
        """
        assert isinstance(filepath, str)
        self.filepath = filepath
        self.data = {}

        if os.path.isfile(filepath):
            self.read()
        else:
            if database_type is None and start_date is None:
                database_type = "Monthly"
                now = datetime.datetime.now()
                start_date = str(now.year) + "-" + str(now.month)
            else:
                assert isinstance(database_type, str)
                assert isinstance(start_date, str)

                self.check_date_format(start_date)
                database_types = ['Monthly', 'Quarterly', 'Yearly']
                if database_type not in database_types:
                    raise ValueError('Value Error: Invalid type. Type must be "Monthly", "Quarterly", or "Yearly"')

            self.data['Type'] = database_type
            self.data['Start Date'] = start_date
            self.data['End Date'] = start_date
            self.data['Accounts'] = {}
            self.data['Latest Dates'] = {}
            self.write()

    def new(self):
        with open(self.filepath, 'w') as outfile:
            json.dump({}, outfile, indent=4)
        self.read()

    def read(self):
        with open(self.filepath, 'r') as readfile:
            self.data = json.load(readfile)

    def write(self):
        with open(self.filepath, 'w') as outfile:
            json.dump(self.data, outfile, indent=4)
        self.read()

    def get_type(self):
        self.read()
        return self.data['Type']

    def get_start_date(self):
        self.read()
        return self.date_parser(self.data['Start Date'])

    def get_end_date(self):
        self.read()
        return self.date_parser(self.data['End Date'])

    def set_start_date(self, input_date):
        """
        Setter for Start Date of Account Database
        :type input_date: str in '%Y-%m' format
        :param input_date: New start date for account database
        """
        assert isinstance(input_date, str)
        self.check_date_format(input_date)

        self.read()
        self.data['Start Date'] = input_date
        self.write()

    def set_end_date(self, input_date):
        """
        Setter for Start Date of Account Database
        :type input_date: positive int
        :param input_date: New end date for account database
        """
        assert isinstance(input_date, str)

        self.check_date_format(input_date)

        self.read()
        self.data['End Date'] = input_date
        self.write()

    def get_iterations(self):
        """
        Get the number of iterations this account database requires between the starting and ending date
        of the account
        :return: an int for the number of months, quarters, or years that are between the starting and ending dates
        """

        self.read()
        start_date = self.get_start_date()
        end_date = self.get_end_date()

        if self.get_type() == "Monthly":
            # Format: MM/YYYY
            start_month, start_year = [int(piece) for piece in start_date.split("/")]
            end_month, end_year = [int(piece) for piece in end_date.split("/")]
            return (end_year - start_year) * 12 + (end_month - start_month) + 1
        elif self.get_type() == "Quarterly":
            # Format: Q# YYYYY
            start_quarter = int(start_date.split(" ")[0][1])  # Get the number after the Q
            start_year = int(start_date.split(" ")[1])
            end_quarter = int(end_date.split(" ")[0][1])
            end_year = int(end_date.split(" ")[1])

            return (end_year - start_year) * 4 + (end_quarter - start_quarter) + 1
        elif self.get_type() == "Yearly":
            # Format: YYYY
            return int(end_date) - int(start_date) + 1

    def add_account(self, name, skip=None):
        """
        Add an account to the database, does nothing if it exists
        :type name: str
        :type skip: bool
        :param name: single string that holds the name of the account to add to
        :param skip: optional param that determines if the account should be skipped from the total calculations
        :return:
        """
        assert isinstance(name, str)

        self.read()
        if name not in self.data['Accounts'].keys():
            self.data['Accounts'][name] = {}
            self.data['Latest Dates'][name] = ''
            if skip:
                self.data['Accounts'][name]['Skip'] = 'Just DO ET'
            self.write()

    def add_entry(self, name, record_date, money):
        """
        Add an item to the database, rewrites if an item exists
        :type name: str
        :type record_date: str in '%Y-%m' format
        :type money: str
        :param name: single string that holds the name of the account to add to
        :param record_date: Date the record is for
        :param money: holds a string of numbers separated by commas and periods
        :return:
        """
        assert isinstance(name, str)
        assert isinstance(record_date, str)
        assert isinstance(money, str)

        self.check_date_format(record_date)

        try:
            money = money.replace(',', '')
            if '.' in money:
                if len(money.split('.')[1]) == 0:  # There is nothing after the period
                    money = int(money.replace('.', '')) * 100
                elif len(money.split('.')[1]) == 1:  # There is 1 digit after the period
                    money = int(money.replace('.', '')) * 10
                elif len(money.split('.')[1]) == 2:  # There are 2 digits after the period
                    money = int(money.replace('.', ''))
                else:  # There are more than 2 digits after the period; truncate to 2 digits after the period
                    money = int(money[0:len(money.split('.')[0]) + 3].replace('.', ''))
            else:  # There is no period in the string
                if money == '':
                    money = 0
                money = int(money) * 100
        except ValueError:
            raise ValueError("ValueError: Invalid monetary value. "
                             "Value needs to be a number with only commas and periods")

        self.read()
        if name not in self.data['Accounts'].keys():
            self.data['Accounts'][name] = {}
        self.data['Accounts'][name][record_date] = money
        self.write()

        if self.data['Latest Dates'][name] < record_date or self.data['Latest Dates'][name] == '':
            # Current account latest date is lower than new entry date
            # Set the account latest date to the new entry date
            self.data['Latest Dates'][name] = record_date
            self.write()
        if self.data['End Date'] < record_date:
            # Current account database end date is lower than new entry date
            # Set the account database date to the new entry date
            self.set_end_date(record_date)

    def remove_account(self, name):
        """
        Remove an account to the database, does nothing if it doesn't exists
        :type name: str
        :param name: single string that holds the name of the account to add to
        :return:
        """
        assert isinstance(name, str)

        self.read()
        if name in self.data['Accounts'].keys():
            self.data['Accounts'].pop(name)
            self.data['Latest Dates'].pop(name)
            self.write()

    def remove_entry(self, name, record_date):
        """
        Remove an item from the database
        :type name: str
        :type record_date: str in '%Y-%m' format
        :param name: single string that holds the name of the account to add to
        :param record_date: Date the record is for
        :return:
        """
        assert isinstance(name, str)
        assert isinstance(record_date, str)

        self.check_date_format(record_date)

        self.read()
        if name not in self.data['Accounts'].keys():
            self.data['Accounts'][name] = {}
        self.data['Accounts'][name].pop(record_date)
        self.write()

        if record_date >= self.data['Latest Dates'][name]:
            # Current account latest date is being removed
            # Set the account latest date to the lasted on record
            new_latest_date = sorted(self.data['Accounts'][name])[-1]
            self.data['Latest Dates'][name] = new_latest_date
            self.write()

            latest_dates = sorted(self.data['Latest Dates'].values())
            if self.data['End Date'] > latest_dates[-1]:
                # Current account database end date is greater than latest dates for all accounts
                # Set the account database date to the new entry date
                self.set_end_date(latest_dates[-1])

    def grab_dates(self):
        """
        Grab all the dates this database covers
        :return: a list of all available dates starting from earliest to latest + an extra date beyond the latest
                The extra date is so there is space to add a new entry in the table
        """
        self.read()
        start_date = self.data['Start Date']
        year, month = [int(piece) for piece in start_date.split("-")]
        iterations = self.get_iterations() + 1

        dates = []
        for i in range(1, iterations + 1):
            dates.append(self.date_parser('{0}-{1:02d}'.format(year, month)))
            if self.get_type() == "Monthly":
                month += 1
                if month == 13:
                    month = 1
                    year += 1
            elif self.get_type() == "Quarterly":
                month += 3
                if month >= 13:
                    month = 1
                    year += 1
            elif self.get_type() == "Yearly":
                year += 1
        return dates

    def grab_account_names(self):
        """
        Grab all the account names
        :return: a sorted list of Account names
        """
        self.read()
        return [name for name in sorted(self.data["Accounts"].keys())]

    def grab_account_data(self, name):
        """
        Grab all the account data
        :param name: single string that holds the name of the account to add to
        :return: dictionary with a datetime.date : int format
        """
        self.read()
        if name in self.data["Accounts"].keys():
            data = {}
            for key, value in self.data["Accounts"][name].items():
                if key == 'Skip':
                    data[key] = value
                    continue
                data[self.date_parser(key)] = value
            return data

    def date_parser(self, input_date):
        """
        Takes an ISO formatted date string and returns a date string based on database type
        :type input_date: str
        :param input_date: date formatted in %Y-%m
        :return: a string in the format below based on database type
                MM/YYYY format for 'Monthly' type
                QQ YYYY format for 'Quarterly' type
                YYYY format for 'Yearly' type
        """
        self.check_date_format(input_date)

        year, month = input_date.split("-")
        if self.get_type() == "Monthly":
            return '{0}/{1}'.format(month, year)
        elif self.get_type() == "Quarterly":
            quarter = (int(month) - 1) // 3 + 1
            return 'Q{0} {1}'.format(quarter, year)
        elif self.get_type() == "Yearly":
            return year

    @staticmethod
    def check_date_format(input_date):
        try:
            datetime.datetime.strptime(input_date, '%Y-%m')
        except ValueError:
            raise ValueError('Value Error: Invalid date format. Date must be in YYYY-MM format')
