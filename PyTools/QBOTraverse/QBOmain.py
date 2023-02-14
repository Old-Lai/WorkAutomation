from QBOWebScraping import QBOWebScrap
from QBODataManager import DataManager

qboWeb = QBOWebScrap()
qboWeb.loginToQBO()
qboData = DataManager()
idList = qboData.importIDFromExcel('/Users/henry/Documents/Others/PyArguments/QBO/idToProcess.xlsx')
print(len(idList))
# qboWeb.searchOrder('PO# 1870517753346')
# print(qboWeb.checkShipping('Jerin Prasad 2325 W Buckingham Rd Apt 1069 Garland TX 75042 United States'))
count = 0
for id in idList:
    count += 1
    print(str(count) + '/' + str(len(idList)))
    qboWeb.openSearch()
    qboWeb.searchOrder(id)
    qboWeb.addClassToProducts()
    qboWeb.saveAndClose()
    # if not qboWeb.findPaymentRecieved():
    #     estDate = qboWeb.getEstDate()
    #     qboWeb.addPaymentRecieved(estDate)

#qboWeb.close()
