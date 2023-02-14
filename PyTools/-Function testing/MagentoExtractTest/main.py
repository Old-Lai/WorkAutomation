from readXlsxFile import MyIDList
from webScratch import WSWebScratch

idList = MyIDList()
idList.readData('/Users/henry/Documents/Daily LUX count track/Tools/ExtractAdressIDList.xlsx')
numOfData = idList.getNumOfData()
web = WSWebScratch()
web.logIntoMagentoAndGoToOrders()
for index in range(numOfData):
    if(web.searchIDInOrders(idList.getID(index))):
        print(str(index) + '.) Billing:')
        idList.editData(index, web.goToBillingEdit())
        web.goBackAPage()
        print(str(index) + '.) Shipping:')
        idList.editData(index, web.goToShippingEdit())
    web.goToOrders()
idList.saveData()
web.completedTask()
print("Complete!!!!!")
