'''

'''

import argparse
import pandas as pd
import numpy as np
import os

LIBELLE_INDEX = 1

DATE_INDEX = 0

DEFAULT_EXPENSES_EXPORT_FILE_ANDROID = "/sdcard/export.xlsx"
DEFAULT_MANUAL_INPUT_FILE_ANDROID = "/sdcard/cp_manual_input.csv"

DEFAULT_EXPENSES_EXPORT_FILE_WINDOWS = "D:\\Users\\Jean-Pierre\\Downloads\\export.xlsx"
DEFAULT_MANUAL_INPUT_FILE_WINDOWS = "D:\\Users\\Jean-Pierre\\Downloads\\cp_manual_input.csv"

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
                df.fillna('', inplace=True)
                print(df.head())
            except SystemExit:
                # exception thrown by the ArgumentParser.exit method called on error or on help request.
                # ArgumentParser prints its help and then the loop continues.
                continue

def expResult():
    print('Expected results')
    eData = [['2018-01-01', 'Solde', np.nan, 100, -100],
['2018-01-05', 'Migros', np.nan, 55.25, np.nan],
['2018-01-05', 'Lidl', np.nan, 20, -175.25],
['2018-01-31', 'Virement', 400, np.nan, 224.75],
]
    e = pd.DataFrame(columns=['Date', 'Lib', 'DEBIT', 'CREDIT', 'SOLDE'],
                    data=eData, index=[x for x in range(1, len(eData) + 1)])

    pd.options.display.float_format = '{:,.2f}'.format
                    
    e.fillna('', inplace=True)
    ei = e.set_index(['Date', 'Lib'])
    print(ei)


def addedData(doPrint):
    if doPrint:
        print('Added data (from command line in the end)')
    eData = [['2016-06-01', 'Solde', np.nan, 100, np.nan],
             ['2016-07-05', 'Interio', np.nan, 20, np.nan],
             ['2016-07-05', 'Bancomat', np.nan, 200, np.nan],
             ['2016-07-31', 'Virement', 400, np.nan, np.nan],
             ]
    e = pd.DataFrame(columns=['Date', 'Lib', 'DEBIT', 'CREDIT', 'SOLDE'],
                     data=eData, index=[x for x in range(1, len(eData) + 1)])

    pd.options.display.float_format = '{:,.2f}'.format

    e.fillna('', inplace=True)

    #Setting string date to Date object. WARNING: internal date format must be
    #yyyy-mm-dd in order for the Date index to be sorted correctly !
    ei = e.set_index(['Date', 'Lib'])
    e['Date'] = pd.to_datetime(e['Date'], format='%Y-%m-%d', utc=True)
    e['Date'] = e['Date'].dt.date #removing 00:00:00 time component
    ei.sort_index(inplace=True)
    if doPrint:
        print(ei)
        print()

    return ei


def expenseData():
    #Setting col names so it matches exp results structure
    colNames = ['Date', 'Lib', 'DEBIT', 'CREDIT', 'Note']

    df = pd.read_excel(DEFAULT_EXPENSES_EXPORT_FILE, header=None, names=colNames)

    print('Raw imported expense data')
    print(df.head())
    print('..')
    print(df.tail())
    print()

    #Replacing empty shop value
    df['Lib'] = df['Lib'].fillna('Divers')

    #Dropping Note column
    dfi = df.drop(columns=['Note'])

    #Altering date format
#    dfi['Date'] = dfi['Date'].dt.date #removing 00:00:00 time component
    dfi['Date'] = dfi['Date'].dt.strftime('%Y-%m-%d')

    #Set index to Date/Lib couple
    dfi.set_index(['Date', 'Lib'], inplace=True)
    dfi.sort_index(inplace=True) #improves multi index select performance

    #Adding SOLDE column
    dfi['SOLDE'] = pd.Series(index=dfi.index)

    #Getting rid of remaining NaN values
    dfi.fillna('', inplace=True)

    print('Structured imported expense data')
    print(dfi.head())
    print('..')
    print(dfi.tail())
    print()

    selectionDate = '2016-07-01'
    print('Accessing rows ' + selectionDate + ' Date only index')
    print(dfi.loc[selectionDate])
    print()

    print()
    print('Accessing row with ' + selectionDate + ' Crêperie Date/Lib index')
    print(dfi.loc[selectionDate, 'Crêperie'])
    print()

    print('Imported expense data after adding added data')

    #Adding command line entered data             ['2016-07-05', 'Hornbach', np.nan, 50, np.nan],

    dfa = pd.concat([dfi, addedData(False)], ignore_index=False)
    dfa.sort_index(inplace=True) #required othervise added data remains at end of DataFrame !

    print(dfa.head(31))

    print()

def explGroupBy():
    eData = [['2016-06-01', 'Solde', np.nan, 100, np.nan],
             ['2016-07-05', 'Interio', np.nan, 20, np.nan],
             ['2016-07-05', 'Hornbach', np.nan, 50, np.nan],
             ['2016-07-05', 'Bancomat', np.nan, 200, np.nan],
             ['2016-07-31', 'Interio', np.nan, 35, np.nan],
             ['2016-07-31', 'Virement', 400, np.nan, np.nan],
             ]
    exp = pd.DataFrame(columns=['Date', 'Lib', 'DEBIT', 'CREDIT', 'SOLDE'], data=eData,
                       index=[x for x in range(1, len(eData) + 1)])
    #exp.fillna('', inplace=True) breaks the groupby !
    print('\nExp data raw')
    print(exp)

    expG = exp.groupby('Date').sum()
    expG['SOLDE'] = expG.apply(lambda row: row.DEBIT - row.CREDIT, axis=1)
    expG['SOLDE'] = expG['SOLDE'].cumsum()

    #merging groupby result with initial DataFrame
    merged = pd.merge(exp, expG, on=['Date'])
    merged.drop(merged.columns[[2, 3, 4]], axis=1, inplace=True)
    merged.columns = ['Date', 'Lib', 'DEBIT', 'CREDIT', 'SOLDE']

    #Set index to Date/Lib couple
    merged.set_index(['Date', 'Lib'], inplace=True)
    merged.sort_index(inplace=True) #improves multi index select performance

    print('\nExp data Group by')
    print(merged)

    previousRow = merged.iloc[0]

    # required for exp.loc used in the loop below to succeed !
    exp.set_index(['Date', 'Lib'], inplace=True)
    exp.sort_index(inplace=True) #improves multi index select performance

    for i in range(1, len(merged)):
        row = merged.iloc[i]
        rowDate = row.name[DATE_INDEX]
        rowLib = row.name[LIBELLE_INDEX]
        expRow = exp.loc[rowDate, rowLib]
        rowDebit = expRow.DEBIT
        rowCredit = expRow.CREDIT
        merged.DEBIT.iloc[i] = rowDebit
        merged.CREDIT.iloc[i] = rowCredit
        if rowDate == previousRow.name[DATE_INDEX] and row.SOLDE == previousRow.SOLDE:
            # merged.iloc[i - 1].SOLDE = np.nan does not work !
            # merged.loc[i - 1, 'SOLDE'] = np.nan #no longer works with set_index moved before loop !
            merged.SOLDE.iloc[i - 1] = np.nan
        previousRow = row

    merged.fillna('', inplace=True)

    print('\nAfter improving Solde col')
    print(merged)

class CommiPay():
    def loadExpenseData(self, filePathName):
        '''
        Reads a the csv data file containing expense data exported from the Android  expense manager
        into a Pandas dataframe.
        :param filePathName: file to read data from

        :return: Pandas dataframe filled with filePathName expense data
        '''
        # Setting col names so it matches exp results structure
        colNames = ['Date', 'Lib', 'DEBIT', 'CREDIT', 'Note']

        df = pd.read_excel(filePathName, header=None, names=colNames)

        #Replacing empty shop value
        df['Lib'] = df['Lib'].fillna('Divers')

        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

        return df

if __name__ == '__main__':
#    enterLoop()
    addedData(True)
    expenseData()
    expResult()
    explGroupBy()
