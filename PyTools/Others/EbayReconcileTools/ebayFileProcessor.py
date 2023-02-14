import pandas as pd
import sys, os
from datetime import datetime

class ebayReport:
    title = ''
    journalEntryNumber = 0
    data = pd.DataFrame()
    claimData = pd.DataFrame()
    refundData = pd.DataFrame()
    holdData = pd.DataFrame()
    orderData = pd.DataFrame()
    otherFeeData = pd.DataFrame()
    shippingData = pd.DataFrame()
    transferData = pd.DataFrame()
    unknownData = pd.DataFrame()

    journalEntryColumns = ['Journal No','Journal Date','Memo',' Account ',' Amount',' Description','Name','Location','Class ','Currency Code','Exchange Rate','Is Adjustment']
    expenseColumns = ['Ref No','Account','Payee','Memo','Payment Date','Payment Method','Expense Account ','Expense Description',' Expense Line Amount ','Expense Billable Status','Expense Markup Percent','Expense Customer ','Expense Class ','Expense Taxable','Product/Service','Product/Service Description','Product/Service Quantity','Product/Service Rate','Product/Service Amount','Product/Service Billable Status','Product/Service Taxable','Product/Service Markup Percent','Billable Customer:Product/Service ','Product/Service Class ','Location','Currency Code','Exchange Rate']
    paymentRecievedColumns = ['Ref No','Payment Date','Customer ','Payment method','Deposit To Account Name','Invoice No','Journal No','Journal No','Amount','Reference No','Memo','Currency Code','Exchange Rate']
    
    def readFile(self):
        print(self.title)
        canReadFile = False
        while not canReadFile:
            print("Feed me report (drag and drop excel file here, then press enter):")
            filePath = input()
            try:
                data = pd.read_csv(filePath.strip().replace('\'',''))
                if not 'eBay collected tax' in data:
                    raise ImportError()
                canReadFile = True
            except ImportError:
                os.system('clear')
                print(self.title)
                print("Could not find eBay collected tax column in excel file!! (reminder, this is for eBay report)\n\n")
            except:
                os.system('clear')
                print(self.title)
                print("file cannot be read or is not an excel file\n\n")

        numericalCols = ['Net amount','Quantity','Item subtotal','Shipping and handling','Seller collected tax','eBay collected tax','Final Value Fee - fixed','Final Value Fee - variable','Very high "item not as described" fee','Below standard performance fee','International fee','Gross transaction amount']
        data[numericalCols] = data[numericalCols].apply(lambda x: pd.to_numeric(x.astype(str).str.replace(',',''), errors='coerce'))

        self.data = data
        return data

    def separateType(self):
        self.claimData = self.data.query('Type == "Claim"')
        self.refundData = self.data.query('Type == "Refund"')
        self.holdData = self.data.query('Type == "Hold"')
        self.orderData = self.data.query('Type == "Order"')
        self.otherFeeData = self.data.query('Type == "Other fee"')
        self.shippingData = self.data.query('Type == "Shipping label"')
        self.transferData = self.data.query('Type == "Transfer"')
        self.unknownData = self.data.query('Type != "Claim" & Type != "Refund" & Type != "Hold" & Type != "Order" & Type != "Other fee" & Type != "Shipping label" & Type != "Transfer"')

        print('----- Count report -----')
        print('num of claim: ' + str(len(self.claimData.index)))
        print('num of refund: ' + str(len(self.refundData.index)))
        print('num of hold: ' + str(len(self.holdData.index)))
        print('num of order: ' + str(len(self.orderData.index)))
        print('num of other fee: ' + str(len(self.otherFeeData.index)))
        print('num of shipping: ' + str(len(self.shippingData.index)))
        print('num of transfer: ' + str(len(self.transferData.index)))
        print('num of unknown: ' + str(len(self.unknownData.index)))
        print('Total num of data: ' + str(len(self.data.index)))
        print('Sumed Total      : ' + str(len(self.claimData.index)+len(self.refundData.index)+len(self.holdData.index)+len(self.orderData.index)+len(self.otherFeeData.index)+len(self.shippingData.index)+len(self.transferData.index)+len(self.unknownData.index)))

    def processExpenseFees(self): #Other Fee + shipping label
        print('Expense Fees-------------------')
        print('Processing Expense Fees.....', end=' ')
        otherFeeList = self.otherFeeData['Net amount'].tolist()
        shippingList = self.shippingData['Net amount'].tolist()
        numList = []
        for i in otherFeeList:
            if pd.notna(i):
                numList.append(i)
        
        for i in shippingList:
            if pd.notna(i):
                numList.append(i)

        expenseFees = pd.DataFrame(columns=self.expenseColumns)
        account = 'HSBC'
        memo = 'HSBC'
        paymentDate = datetime.strptime(self.data['Payout date'].iloc[-1],'%d-%b-%y').date().strftime('%m/%d/%Y')
        expenseAcc = 'Merchant Account Fees'
        expenseDes = 'eBay other fee'
        expenseAmt = round(sum(numList),2)
        expenseClass = 'eBay - Direct Sales'

        expenseFees.loc[-1] = ['',account,'',memo,paymentDate,'',expenseAcc,expenseDes,expenseAmt,'','','',expenseClass,'','','','','','','','','','','','','','']
        expenseFees.index += 1
        self.__exportToExcel(expenseFees,'Fees(expense) upload')
        print('Complete')

    def processSalesTax(self):
        print('Sales Tax -----------------')
        print('Processing Sales Tax.....', end=' ')
        combinedData = pd.concat([self.orderData, self.refundData])
        payoutDayList = combinedData['Payout date'].drop_duplicates(keep='first').tolist()
        payoutDayList.sort(key=lambda date: datetime.strptime(date,"%d-%b-%y"))

        salesTax = pd.DataFrame(columns=self.journalEntryColumns)
        individualSales = pd.DataFrame(columns=self.journalEntryColumns)

        for payoutDay in payoutDayList:
            filteredData = combinedData[combinedData['Payout date'] == payoutDay]

            rowSum = 0
            for index, rowData in filteredData.iterrows():
                amt = rowData['eBay collected tax']
                if(pd.notna(amt)):
                    jDate = payoutDay
                    memoNDes = 'eBay Remitted Sales Tax ' + rowData['Order number']
                    acc = 'eBay Sales Tax'
                    rowSum += amt

                    individualSales.loc[-1] = [self.journalEntryNumber, jDate, memoNDes, acc, amt, memoNDes, '', '', '', '', '', '']
                    individualSales.index += 1
            
            individualSales.sort_values(by=' Amount', ascending=False, inplace=True)
            rowSum *= -1
            sumLine = [self.journalEntryNumber, jDate, 'eBay Remitted Sales Tax', 'HSBC', rowSum, 'eBay Remitted Sales Tax', '', '', '', '', '', '']
            individualSales.loc[-1] = sumLine
            individualSales.index += 1
            salesTax = pd.concat([salesTax, individualSales])
            individualSales = individualSales.iloc[0:0]
            self.journalEntryNumber += 1
            self.__exportToExcel(salesTax,'SalesTax(JE) Upload')
        print('Complete')

    def processOrderRefundFees(self):
        print('OrderFees -----------------')
        print('processing OrderFees......', end=' ')
        combinedData = pd.concat([self.orderData, self.refundData, self.claimData])
        combinedData.dropna(subset=['Net amount'], inplace=True)
        payoutList = combinedData['Payout date'].drop_duplicates(keep='first').tolist()
        payoutList.sort(key=lambda date: datetime.strptime(date,"%d-%b-%y"))

        orderFeesData = pd.DataFrame(columns=self.journalEntryColumns)
        individualDayData = pd.DataFrame(columns=self.journalEntryColumns)

        for payoutDay in payoutList:
            filteredData = combinedData[combinedData['Payout date'] == payoutDay]
            rowSum = 0
            for index, row in filteredData.iterrows():
                netAmt = row['Net amount']
                grossAmt = row['Gross transaction amount']
                feeAmt = grossAmt - netAmt
                if(not feeAmt == 0):
                    jNum = self.journalEntryNumber
                    jDate = payoutDay
                    memo = ''
                    acc = 'Merchant Account Fees'
                    amt = feeAmt
                    des = f'eBay {round(feeAmt/grossAmt*100,2)}% {row["Order number"]}' if row['Type'] == 'Order' else f'{row["Order number"]} merchant fee'
                    individualDayData.loc[-1] = [jNum, jDate, memo, acc, amt, des, '','','','','','']
                    individualDayData.index += 1
                    rowSum += amt
            individualDayData.sort_values(by=' Amount', ascending=False, inplace=True)
            rowSum *= -1
            individualDayData.loc[-1] = [jNum, jDate, memo, 'HSBC', rowSum, 'eBay Final Value Fee','','','','','','']
            individualDayData.index += 1
            orderFeesData = pd.concat([orderFeesData,individualDayData])
            individualDayData = individualDayData.iloc[0:0]
            self.journalEntryNumber += 1
        self.__exportToExcel(orderFeesData, 'MerchantFees(JE) upload')
        print('Complete')

    def processHold(self):
        print('Hold ------------------')
        print('Processing Hold.......', end=' ')
        data = self.holdData
        caseIDs = data['Reference ID'].drop_duplicates(keep='first').tolist()
        outputData = pd.DataFrame(columns=self.journalEntryColumns)
        for caseID in caseIDs:
            filteredData = data[data['Reference ID'] == caseID]
            if not filteredData.sum(numeric_only=True)['Net amount'] == 0:
                jNum = self.journalEntryNumber
                jDate = filteredData['Payout date'].tolist()[0]
                memo = ''
                acc = 'Sales of Product Income - Returns:Chargeback'
                acc2 = 'HSBC'
                amt = filteredData['Net amount'].tolist()[0]
                amt2 = amt * -1
                des = 'EB_' + filteredData['Type'].str.cat(sep='\n') + ' ' + ('hold placed' if amt > 0 else 'hold released')

                outputData.loc[-1] = [jNum, jDate, memo, acc, amt, des, '','','','','','']
                outputData.index += 1
                outputData.loc[-1] = [jNum, jDate, memo, acc2, amt2, des, '','','','','','']
                outputData.index += 1
                self.journalEntryNumber += 1

        self.__exportToExcel(outputData, 'Hold Needed Processing')
        print('Complete')

    def processRefund(self):

        pass

    def processReports(self):
        print('\nRunning.....')
        while True:
            try:
                jNum = int(input('\nPlease Enter number for the first journal entry: '))
                break
            except ValueError:
                print('\nOnly numbers allowed')
        self.journalEntryNumber = jNum
        self.processExpenseFees()
        self.processSalesTax()
        self.processOrderRefundFees()
        self.processHold()

    def __exportToExcel(self, data, fileName):
        # currentPath = os.path.dirname(sys.executable) + '/'
        currentPath = __file__[:__file__.rfind('/')] + '/'
        data.to_excel(currentPath + fileName + '.xlsx', index = False, header = True)
