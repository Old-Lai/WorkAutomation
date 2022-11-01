from MagentoWebScraping import MagentoWebScrap
from MagentoDataManager import DataManager
import time
import traceback

rawFileDir = '/Users/henry/Documents/Others/PyArguments/WS/raw.csv'
sortOutput = '/Users/henry/Documents/Others/PyArguments/WS/Sorted File'
outputDir = '/Users/henry/Documents/Others/PyArguments/WS'
dataManager = DataManager()
dataManager.processRawData(rawFileDir, sortOutput)
time.sleep(3)
idNums = dataManager.getProcessingData()['"ID"'].tolist()
print(idNums)
MagentoWeb = MagentoWebScrap()
MagentoWeb.loginToMagento()
numOfData = len(idNums)
count = 0

for idNum in idNums:
    data = {}
    try:
        MagentoWeb.goToOrders()
        MagentoWeb.sesarchOrder(idNum)
        data[idNum] = {}
        print('getting billing')
        data[idNum]['billing'] = MagentoWeb.getBilling()
        print('getting shipping')
        data[idNum]['shipping'] = MagentoWeb.getShipping()
        print('getting Payment')
        data[idNum]['payment'] = MagentoWeb.getPaymentMethod()
        print('getting Details')
        data[idNum]['product'] = MagentoWeb.getProductDeatils()
        print('getting Total')
        data[idNum]['orderTotal'] = MagentoWeb.getOrderTotals()
        print('getting Capture Date')
        if 'Wire' in data[idNum]['payment']:
            data[idNum]['captureDate'] = ''
        else:
            data[idNum]['captureDate'] = MagentoWeb.getCapturedDate()
        print('getting Ordered Date')
        data[idNum]['orderedDate'] = MagentoWeb.getOrderedDate()
        print('getting Contact')
        data[idNum]['contact'] = MagentoWeb.getCustomerContact()
        print(data)
        dataManager.addToOutput(data)
        dataManager.formatAndExportEst(data)
        dataManager.formatAndExportCust()
        dataManager.exportOutput(outputDir)
        count += 1
        print(str(count) + ' of ' + str(numOfData))
    except:
        dataManager.saveToFailed(idNum, outputDir)
        print('Error occured!!!')
        print(traceback.print_exc())

MagentoWeb.close()
