import os
import datetime

import ZODB
import ZODB.FileStorage
from persistent import Persistent
from BTrees import OOBTree, OIBTree
import transaction

__author__ = 'Gareth Mok'

class Database(Persistent):
    def __init__(self, filepath: str):
        setup_db = not os.path.isfile(filepath)
        self.db = ZODB.DB(filepath)
        if setup_db:
            self.connection = self.db.open()
            self.root = self.connection.root()
            self.root.accounts = OOBTree.BTree()
            transaction.commit()
            self.connection.close()
            
        self.connection = None
        self.root = None

    def __enter__(self):
        self.connection = self.db.open()
        self.root = self.connection.root()

    def __exit__(self, exception_type, exception_value, traceback):
        transaction.commit()
        self.connection.close()
        self.connection = None
        self.root = None

    def get_account(self, account: str):
        """ Gets the account data from the datbase
            If the account doesn't exist, create it first
        """
        if not self.connection and not self.root:
            raise ConnectionError('Database connection not setup yet. Use the database with a context manager.')
        if account not in self.root.accounts:
            self.root.accounts[account] = Account()
        return self.root.accounts[account]
    
    def remove_account(self, account: str):
        if not self.connection and not self.root:
            raise ConnectionError('Database connection not setup yet. Use the database with a context manager.')
        del self.root.accounts[account]

    def grab_accounts(self):
        return self.root.accounts.keys()


class Account(Persistent):
    def __init__(self):
        self.type = ''
        self.start_date = ''
        self.end_date = ''
        self.splits = OOBTree.BTree()        

    def get_start_date(self):
        return self.date_parser(self.start_date)

    def set_start_date(self, input_date: str):
        """
        Setter for Start Date of Account Database
        :type input_date: str in '%Y-%m' format
        :param input_date: New start date for account database
        """
        self.check_date_format(input_date)
        self.start_date = input_date

    def get_end_date(self):
        return self.date_parser(self.end_date[0])
    
    def set_end_date(self, input_date: str):
        """
        Setter for End Date of Account Database
        :type input_date: str in '%Y-%m' format
        :param input_date: New start date for account database
        """
        self.check_date_format(input_date)
        self.end_date = input_date

    def add_split(self, name: str, part_of_total=True):
        """
        Add a split of the account to the database, does nothing if it exists
        :type name: str
        :type part_of_total: bool
        :param name: single string that holds the name of the account to add to
        :param part_of_total: optional param that determines if the account should be skipped from the total calculations
        :return:
        """
        if name not in self.splits:
            self.splits[name] = Split(part_of_total)        

    def add_split_entry(self, split_name: str, record_date: str, money: str):
        """
        Add an item to the database, rewrites if an item exists
        :type split_name: str
        :type record_date: str in '%Y-%m' format
        :type money: str
        :param split_name: single string that holds the name of the split to add to or update
        :param record_date: Date the record is for
        :param money: holds a string of numbers separated by commas and periods
        :return:
        """
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

        if split_name not in self.splits:
            raise KeyError("Split doesn't exist in account")
        self.splits[split_name].add_update_record(record_date, money)

        if self.data['End Date'] < record_date:
            # Current account database end date is lower than new entry date
            # Set the account database date to the new entry date
            self.set_end_date(record_date)

    def remove_split(self, split_name: str):
        """
        Remove an split from the account, does nothing if it doesn't exists
        :type split_name: str
        :param name: single string that holds the name of the account to add to
        :return:
        """
        if split_name in self.splits:
            del self.splits[split_name]

    def remove_split_entry(self, split_name: str, record_date: str):
        """
        Remove a record from the database
        :type name: str
        :type record_date: str in '%Y-%m' format
        :param split_name: single string that holds the name of the split to remove from
        :param record_date: Date the record is for
        :return:
        """
        self.check_date_format(record_date)

        if split_name not in self.splits:
            raise KeyError("Split doesn't exist in account")
        self.splits[split_name].remove_record(record_date)

        latest_dates = sorted([split.latest_date for split in self.splits])
        if self.end_date > latest_dates[-1]:
            # Current account database end date is greater than latest dates for all accounts
            # Set the account database date to the new entry date
            self.set_end_date(latest_dates[-1])

    def grab_split_names(self):
        """
        Grab all the split names in the account
        :return: a sorted list of Split names
        """
        return sorted(self.splits.keys())

    def grab_split_data(self, split_name: str):
        """
        Grab all the split data
        :param name: single string that holds the name of the split to retrieve data from
        :return: tuple with a boolean and a dictionary formated in date parsed date str : money int
            boolean holds whether the split should be counted towards the total
        """
        if split_name in self.splits:
            split = self.splits[split_name]
            return (split.part_of_total, 
                {self.date_parser(key): value for key, value in split.records.items()}, )

    def get_iterations(self):
        """
        Get the number of iterations this account database requires between the starting and ending date
        of the account
        :return: an int for the number of months, quarters, or years that are between the starting and ending dates
        """
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

    def grab_dates(self):
        """
        Grab all the dates this database covers
        :return: a list of all available dates starting from earliest to latest + an extra date beyond the latest
                The extra date is so there is space to add a new entry in the table
        """
        start_date = self.start_date
        year, month = [int(piece) for piece in start_date.split("-")]
        iterations = self.get_iterations() + 1

        dates = []
        for _ in range(1, iterations + 1):
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


class Split(Persistent):
    def __init__(self, part_of_total: bool):
        self.records = OIBTree.BTree()
        self.part_of_total = part_of_total
        self.latest_date = ''

    def add_update_record(self, record_date: str, amount: int):
        self.records[record_date] = amount
        if not self.latest_dates or self.latest_dates < record_date:
            # Record date occurs after latest date, update latest date with new record date
            self.latest_date = record_date

    def remove_record(self, record_date: str):
        del self.reccords[record_date]
        if self.latest_dates == record_date:
            # Record date being removed occurs at the latest date time, update latest date with the previous latest date
            self.latest_date = sorted(self.records.keys())[-1]
