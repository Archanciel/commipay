'''

'''

import argparse
import pandas as pd
import os


DEFAULT_EXPENSES_EXPORT_FILE_ANDROID = "/sdcard/export.xlsx"
DEFAULT_EXPENSES_EXPORT_FILE_WINDOWS = "C:\\Users\\Jean-Pierre\\Downloads\\export.xlsx"

if os.name == 'posix':
    DEFAULT_EXPENSES_EXPORT_FILE = DEFAULT_EXPENSES_EXPORT_FILE_ANDROID
else:
    DEFAULT_EXPENSES_EXPORT_FILE = DEFAULT_EXPENSES_EXPORT_FILE_WINDOWS

parser = argparse.ArgumentParser(
        description="Version {}. Adds or inserts all or part of the images contained in the current dir to a Word document. Each image " \
                    "is added in a new paragraph. To facilitate further edition, the image ".format("v0.1"))
#parser.add_argument("val", type=int, help="display a square of a given number")
#parser.add_argument("power", type=int, nargs="?", default=2, help="power to apply to val. 2 if not specified.")
parser.add_argument("-d", "--data", nargs="?", default=DEFAULT_EXPENSES_EXPORT_FILE, help="increase output verbosity")
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], help="increase output verbosity")

def enterLoop():
    stop = False

    while not stop:
        inputStr = input("Waiting for command (q to quit): ")
        if inputStr.upper() == 'Q':
            stop = True
        else:
            try:
                inputList = inputStr.split() # ArgumentParser accepts a list of arguments
                args = parser.parse_args(inputList)
                expenseFilePath = args.data
                df = pd.read_excel(expenseFilePath, header=None)
                print(df.head())

                if args.verbosity == 2:
                    pass
                elif args.verbosity == 1:
                    pass
                else:
                    pass
            except SystemExit:
                # exception thrown by the ArgumentParser.exit method called on error or on help request.
                # ArgumentParser prints its help and then the loop continues.
                continue

if __name__ == '__main__':
    enterLoop()
