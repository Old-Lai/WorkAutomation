from os import listdir
from os.path import isfile, join
from extractTextFromPDF import extractFromFile
from downloadPDFFromList import downloadPDFFile
from styleUpload import formatCust, formatInvoice
import pandas as pd
import time

downloadPath = '/Users/henry/Documents/Others/PyArguments/whatnot/downloaded'
reportPath = '/Users/henry/Documents/Others/PyArguments/whatnot/report.csv'
exportPath = '/Users/henry/Documents/Others/PyArguments/whatnot/'
numberOfOrders = downloadPDFFile(reportPath, downloadPath + '/')
time.sleep(4)
files = [f for f in listdir(downloadPath) if isfile(join(downloadPath, f))]
data = pd.DataFrame(columns=['fullname','firstname', 'lastname', 'address', 'city', 'state', 'zip', 'country', 'tracking', 'brand', 'description', 'orderNum', 'price'], index = range(numberOfOrders))

count = 0
for file in files:
    if(file.find('.pdf') >= 0):
        list = extractFromFile(downloadPath + '/' +file)
        for i in range(len(list[11])):
            for j in range(len(list)):
                if(j < 9):
                    data.iloc[count + i, j] = list[j]
                else:
                    data.iloc[count + i, j] = list[j][i]
        count += len(list[11])

    formatCust(data, exportPath)
    formatInvoice(data, exportPath)

    data.to_excel(exportPath + 'output.xlsx', index = False, header = True)
