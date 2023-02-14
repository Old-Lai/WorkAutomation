from os import listdir
from os.path import isfile, join
from pdfManager import extractFromFile, extractLabel
from downloadPDFFromList import downloadPDFFile
from styleUpload import formatCust, formatInvoice
import pandas as pd
import time

downloadPath = '/Users/henry/Documents/Others/PyArguments/whatnot/downloaded'
reportPath = '/Users/henry/Documents/Others/PyArguments/whatnot/report.csv'
exportPath = '/Users/henry/Documents/Others/PyArguments/whatnot/'
numberOfOrders = downloadPDFFile(reportPath, downloadPath + '/')
print(numberOfOrders)
time.sleep(4)
files = [f for f in listdir(downloadPath) if isfile(join(downloadPath, f))]
#data = pd.DataFrame(columns=['fullname','firstname', 'lastname', 'address', 'city', 'state', 'zip', 'country', 'tracking', 'brand', 'description', 'orderNum', 'price'], index = range(numberOfOrders))
data = {'username':[],
        'fullname':[],
        'firstname':[],
        'lastname':[],
        'address':[],
        'city':[],
        'state':[],
        'zip':[],
        'country':[],
        'tracking':[],
        'brand':[],
        'description':[],
        'orderNum':[],
        'price':[]}
dataKey = list(data)

extractLabel(downloadPath + '/', files, exportPath)

count = 0
for file in files:
    if(file.find('.pdf') >= 0):
        list = extractFromFile(downloadPath + '/' +file)
        for i in range(len(list[12])):
            for j in range(len(list)):
                if(j < 10):
                    # data.iloc[count + i, j] = list[j]
                    data[dataKey[j]].append(list[j])
                else:
                    # data.iloc[count + i, j] = list[j][i] 
                    data[dataKey[j]].append(list[j][i])
        count += len(list[12])

    dataDF = pd.DataFrame.from_dict(data)
    formatCust(dataDF, exportPath)
    formatInvoice(dataDF, exportPath)

    dataDF.to_excel(exportPath + 'output.xlsx', index = False, header = True)
