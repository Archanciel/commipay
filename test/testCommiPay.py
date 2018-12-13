import unittest
import os,sys,inspect
import csv
from cp import CommiPay

DUMMY_HEADER = ["DUMMY HEADER 1", "DUMMY HEADER 2"]

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

class TestCommiPay(unittest.TestCase):
    def setUp(self):
        if os.name == 'posix':
            self.configFilePath = '/sdcard/gridview_test.ini'
        else:
            self.configFilePath = 'D:\\Users\\Jean-Pierre\\Downloads\\export.xlsx'

    def testLoadExpenseData(self):
        '''
        This test case ensures that the grid data are written into the csv file with a column title
        line as well as with a 0 index column storing the 0 based line index.
        '''
        xlrxFileName = "testLoadExpenseData.xlsx"
        cp = CommiPay()
        df = cp.loadExpenseData(xlrxFileName)

        self.assertEquals(681, len(df.index))

        # with open(xlrxFileName, 'r') as file:
        #     reader = csv.reader(file, delimiter='\t')
        #
        #     # reading the header line and use it to determine the x dimension of the input data
        #
        #     header = next(reader)
        #     self.assertEqual(['','0','1','2','3'], header)
        #
        #     self.assertEqual(['0','1','1','0','0'], next(reader), 'csv matrix data line 0')
        #     self.assertEqual(['1','1','0','1','1'], next(reader), 'csv matrix data line 1')
        #     self.assertEqual(['2','0','0','1','1'], next(reader), 'csv matrix data line 2')
        #     self.assertEqual(['3','1','1','1','1'], next(reader), 'csv matrix data line 3')


#        os.remove(csvFileName)

if __name__ == '__main__':
    unittest.main()