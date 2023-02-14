import pandas as pd

class DataManager():
    def importIDFromExcel(self, fileDir):
        rawExcelData = pd.read_excel(fileDir, dtype=str)
        data = pd.DataFrame(rawExcelData)
        return data['ID'].tolist()
