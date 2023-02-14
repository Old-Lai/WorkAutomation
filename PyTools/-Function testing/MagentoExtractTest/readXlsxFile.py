import pandas as pd

class MyIDList:
    data = pd.DataFrame()
    def readData(self,filePath):
        excel_data = pd.read_excel(filePath, dtype={'ID': str})
        self.data = pd.DataFrame(excel_data)

    def editData(self, row, inputList):
        for key in inputList:
            self.data.loc[row, key] = inputList[key]
            print("----Key: " + key + '----\n' + "Value: " + inputList[key] + '\n')

    def printData(self):
        print(self.data)

    def saveData(self):
        self.data.to_excel(r'/Users/henry/Documents/Daily LUX count track/Tools/Data.xlsx', index = False, header = True)

    def getID(self, row):
        return self.data.loc[row,'ID']

    def getNumOfData(self):
        return (self.data.shape[0])
