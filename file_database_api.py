import json
import os

__author__ = 'Gareth Mok'


class Files:
    def __init__(self, filepath):
        """
        Keys are Account Names and Values are the file path
        :type filepath: str
        :param filepath: filepath path location
        :return:
        """
        assert isinstance(filepath, str)

        self.filepath = filepath
        self.data = {'Directory': ''}

        if os.path.isfile(filepath):
            self.read()
        else:
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

    def add_update(self, name, file_location):
        """
        Add an item to the database, rewrites if an item exists
        :type name: str
        :type file_location: str
        :param name: name of the file when opened as a tab
        :param file_location: the full file location
        :return:
        """
        assert isinstance(name, str)
        assert isinstance(file_location, str)

        if name != "Directory" and not os.path.isfile(file_location):
            raise FileNotFoundError("Given file location not a valid file")

        self.read()
        self.data[name] = file_location
        self.write()

    def remove(self, name):
        """
        Remove the file from the database
        :type name: str
        :param name: name of the file in the database
        :return:
        """
        assert isinstance(name, str)

        self.read()
        if name in self.data.keys():
            self.data.pop(name)
        self.write()

    def get_directory(self):
        """
        Grab the directory for the account databases
        :return: string that holds the directory path
        """
        self.read()
        return self.data['Directory']

    def grab(self):
        """
        Grab the data
        :return: dictionary with a str: str format with the name as key and file location as value
        """
        self.read()
        return {key: value for key, value in self.data.items() if key != 'Directory'}

    def empty(self):
        """
        Check if the database is empty
        :return: True if empty, False if not
        """
        return len(self.data) == 1
