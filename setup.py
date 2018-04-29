import sys
from cx_Freeze import setup, Executable

__author__ = 'Gareth Mok'

# -*- coding: utf-8 -*-

# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt4app.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application


base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': ['atexit', 'PyQt4'],
        'include_files': ['credit.txt', 'add_remove_account.ui', 'add_remove_entry.ui',
                          'frame.ui', 'get_database_type.ui', 'get_start_date.ui', 'main.ui',
                          'White_Background_Annuity.png'],
    }
}

executables = [
    Executable('gui_main.py', base=base,
               targetName='Account_Recorder.exe')
]

includes = ['PyQt5', 'datetime', 'json', 'os', 'pyqtgraph', 'sys', 'ZODB', 'persistent', 'BTrees', 'transaction']

setup(name='Account Recoder',
      version='0.1',
      description='Keeps a simple record of money accounts',
      options=options,
      install_requires=['PyQt5', 'pyqtgraph'],
      executables=executables
      )
