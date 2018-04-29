import json
import os

__author__ = 'Gareth Mok'


class Config:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = {'Previous Open Database': ''}

        if os.path.isfile(filepath):
            self.read()
        else:
            self.write()

    def read(self):
        with open(self.filepath, 'r') as readfile:
            self.data = json.load(readfile)

    def write(self):
        with open(self.filepath, 'w') as outfile:
            json.dump(self.data, outfile, indent=4)
        self.read()

    def set_prev_database(self, file_location: str):
        self.read()
        if not os.path.isfile(file_location):
            raise FileNotFoundError("Given file location not a valid file")
        self.data['Previous Open Database'] = file_location
        self.write()

    def get_prev_database(self):
        self.read()
        return self.data['Previous Open Database']
