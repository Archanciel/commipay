'''

'''

import argparse
import pandas as pd
import os


DEFAULT_EXPENSES_EXPORT_FILE_ANDROID = "/sdcard/export.xlsx"
DEFAULT_MANUAL_INPUT_FILE_ANDROID = "/sdcard/cp_manual_input.csv"

DEFAULT_EXPENSES_EXPORT_FILE_WINDOWS = "C:\\Users\\Jean-Pierre\\Downloads\\export.xlsx"
DEFAULT_MANUAL_INPUT_FILE_WINDOWS = "C:\\Users\\Jean-Pierre\\Downloads\\cp_manual_input.csv"

if os.name == 'posix':
    DEFAULT_EXPENSES_EXPORT_FILE = DEFAULT_EXPENSES_EXPORT_FILE_ANDROID
    DEFAULT_MANUAL_INPUT_FILE = DEFAULT_MANUAL_INPUT_FILE_ANDROID
else:
    DEFAULT_EXPENSES_EXPORT_FILE = DEFAULT_EXPENSES_EXPORT_FILE_WINDOWS
    DEFAULT_MANUAL_INPUT_FILE = DEFAULT_MANUAL_INPUT_FILE_WINDOWS

parser = argparse.ArgumentParser(
        description="Version {}. Adds or inserts all or part of the images contained in the current dir to a Word document. Each image " \
                    "is added in a new paragraph. To facilitate further edition, the image ".format("v0.1"))
parser.add_argument("-e", "--export", nargs="?", default=DEFAULT_EXPENSES_EXPORT_FILE, help="Expense manager xlsx export file path")
parser.add_argument("-i", "--input", nargs="?", default=DEFAULT_MANUAL_INPUT_FILE, help="Manual input csv file path")
parser.add_argument("-d", "--date", default=None, help="Operation date (DD/MM or DD/MM/YY)")
parser.add_argument("-s", "--start", type=float, default=None, help="Initial balance (negative if amount is due !)")
parser.add_argument("-c", "--cash", type=float, default=None, help="Amount drawn from cash machine")
parser.add_argument("-l", "--loan", type=float, default=None, help="Amount lended")
parser.add_argument("-p", "--purchase", type=float, default=None, help="Value of purchase (extra purchase not entered in expense manager)")
parser.add_argument("-w", "--where", default=None, help="Store where purchase was done")
parser.add_argument("-n", "--note", default=None, help="Note")

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
                expenseFilePath = args.export
                manualFilePath = args.input
                opDate = args.date
                startBalance = args.start
                cashWithdrawal = args.cash
                loanAmount = args.loan
                purchaseAmount = args.purchase
                purchaseStore = args.where
                note = args.note

                print("expenseFilePath {}".format(expenseFilePath))
                print("manualFilePath {}".format(manualFilePath))
                print("opDate {}".format(opDate))
                print("startBalance {}".format(startBalance))
                print("cashWithdrawal {}".format(cashWithdrawal))
                print("loanAmount {}".format(loanAmount))
                print("purchaseAmount {}".format(purchaseAmount))
                print("purchaseStore {}".format(purchaseStore))
                print("note {}".format(note))

                colNames = ['DATE', 'CATEGORY', '?', 'AMOUNT', 'NOTE']
                df = pd.read_excel(expenseFilePath, header=None, names=colNames)
                print(df.head())
            except SystemExit:
                # exception thrown by the ArgumentParser.exit method called on error or on help request.
                # ArgumentParser prints its help and then the loop continues.
                continue

if __name__ == '__main__':
    enterLoop()
