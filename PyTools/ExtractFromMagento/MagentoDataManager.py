import pandas as pd

class DataManager():
    processingData = pd.DataFrame()
    holdedData = pd.DataFrame()
    completedData = pd.DataFrame()
    closed_CancledData = pd.DataFrame()
    unknownData = pd.DataFrame()
    header = ['ID','Purchase Date','Capture Date','PaymentMethod','Email','Bill Name','Bill First','Bill Last','Bill Address1','Bill Address2','Bill Address3','Bill City','Bill Country','Bill State','Bill Zip','Bill Phone','Ship Name','Ship First','Ship Last','Ship Address1','Ship Address2','Ship Address3','Ship City','Ship Country','Ship State','Ship Zip','Ship Phone','Product SKU','Product Description','Product Price','Product Quantity','Order Subtotal','Order Shipping Fee','Order Discount Total','Order Tax','Order Total', 'Refunded amount']
    outputData = pd.DataFrame(columns=header)

    formatedEstimateData = pd.DataFrame(columns=['Estimate No','Customer','Estimate Date','Expiration Date','Estimate Status','Accepted By','Accepted Date','Ship Via','Ship Date','Tracking No','Billing Address Line 1','Billing Address Line 2','Billing Address Line 3','Billing Address City','Billing Address Postal Code','Billing Address Country','Billing Address State','Shipping Address Line 1','Shipping Address Line 2','Shipping Address Line 3','Shipping Address City','Shipping Address Postal Code','Shipping Address Country','Shipping Address State','Memo','Message displayed on estimate','Email','Shipping','Sales Tax Code','Sales Tax Amount','Discount Amount','Discount Percent','Discount Account','Service Date','Product/Service','Product/Service Description','Product/Service Quantity','Product/Service Rate','Product/Service Amount','Product/Service Taxable','Product/Service Class','Show Sub Total','Apply Tax After Discount','Location','Custom Field Value (1)','Custom Field Value (2)','Custom Field Value (3)','Currency Code','Exchange Rate','Print Status','Email Status'])
    formatedCustomerData = pd.DataFrame(columns=['Title','Company','First Name','Middle Name','Last Name','Suffix','Display Name As','Print On Check As','Billing Address Line 1','Billing Address Line 2','Billing Address Line 3','Billing Address City','Billing Address Postal Code','Billing Address Country','Billing Address State','Shipping Address Line 1','Shipping Address Line 2','Shipping Address Line 3','Shipping Address City','Shipping Address Postal Code','Shipping Address Country','Shipping Address State','Phone','Mobile','Fax','Other','Website','Email','Terms','Preferred Payment Method','Tax Resale No','Preferred Delivery Method','Bill With Parent','Parent Customer','Opening Balance','Open Balance Date','Notes','Customer Taxable','Currency Code'])

    failedOutput = pd.DataFrame(columns=['ID'])

    def processRawData(self, reportDir, exportDir):
        rawCsvData = pd.read_csv(reportDir, dtype=str)
        data = pd.DataFrame(rawCsvData)
        self.processingData = pd.concat([self.processingData, data.query('Status == "processing" | Status == "pending" | Status == "complete"')])
        self.holdedData = pd.concat([self.holdedData, data[data['Status'] == 'holded']]) 
        self.completedData = pd.concat([self.completedData, data[data['Status'] == 'complete']]) 
        self.closed_CancledData = pd.concat([self.closed_CancledData, data.query('Status == "closed" | Status == "canceled"')]) 
        self.unknownData = pd.concat([self.unknownData, data.query('Status != "processing" & Status != "pending" & Status != "holded" & Status != "complete" & Status != "closed" & Status != "canceled"')]) 
        self.exportAllExcel(exportDir)

    def getProcessingData(self):
        return self.processingData

    def addToOutput(self, data):
        idNum = str(list(data.keys())[0])

        captureDate = data[idNum]['captureDate']
        orderDate = data[idNum]['orderedDate']
        paymentMethod = data[idNum]['payment']
        email = data[idNum]['contact']['email']

        billFirst = data[idNum]['billing']['firstName']
        billLast = data[idNum]['billing']['lastName']
        billFull = billFirst + ' ' + billLast
        billAdd1 = data[idNum]['billing']['address1']
        billAdd2 = data[idNum]['billing']['address2']
        billAdd3 = data[idNum]['billing']['address3']
        billCity = data[idNum]['billing']['city']
        billCountry = data[idNum]['billing']['country']
        billState = data[idNum]['billing']['state']
        billZip = data[idNum]['billing']['zip']
        billPhone = data[idNum]['billing']['phone']

        shipFirst = data[idNum]['shipping']['firstName']
        shipLast = data[idNum]['shipping']['lastName']
        shipFull = shipFirst + ' ' + shipLast
        shipAdd1 = data[idNum]['shipping']['address1']
        shipAdd2 = data[idNum]['shipping']['address2']
        shipAdd3 = data[idNum]['shipping']['address3']
        shipCity = data[idNum]['shipping']['city']
        shipCountry = data[idNum]['shipping']['country']
        shipState = data[idNum]['shipping']['state']
        shipZip = data[idNum]['shipping']['zip']
        shipPhone = data[idNum]['shipping']['phone']

        orderDiscount = 0
        for key, val in data[idNum]['orderTotal'].items():
            if 'Subtotal' in key:
                orderSubtotal = val
            elif 'Shipping' in key:
                orderShipping = val
            elif 'Discount' in key:
                orderDiscount += float(val.replace(',',''))
            elif 'Grand Total (Incl.Tax)' in key:
                orderGrandTotal = val
            elif 'Total Refunded' in key:
                orderRefund = val
        orderTax = data[idNum]['orderTotal']['Tax']

        for i in range(len(data[idNum]['product']['SKU'])):
            pdData = pd.DataFrame(columns=self.header)
            #print(i)
            productSKU = data[idNum]['product']['SKU'][i]
            productDes = data[idNum]['product']['productDescription'][i]
            productUnitPrice = data[idNum]['product']['unitPrice'][i]
            productQuantity = data[idNum]['product']['quantity'][i]
            #'ID','Purchase Date','Capture Date','PaymentMethod','Email','Bill Name','Bill First','Bill Last','Bill Address1','Bill Address2','Bill Address3','Bill City','Bill Country','Bill State','Bill Zip','Bill Phone','Ship Name','Ship First','Ship Last','Ship Address1','Ship Address2','Ship Address3','Ship City','Ship Country','Ship State','Ship Zip','Ship Phone','Product SKU','Product Description','Product Price','Product Quantity','Order Subtotal','Order Shipping Fee','Order Discount Total','Order Tax','Order Total', 'Refunded amount'
            pdData.loc[-1] = [idNum, orderDate, captureDate, paymentMethod, email, billFull, billFirst, billLast, billAdd1, billAdd2, billAdd3, billCity, billCountry, billState, billZip, billPhone, shipFull, shipFull, shipLast, shipAdd1, shipAdd2, shipAdd3, shipCity, shipCountry, shipState, shipZip, shipPhone, productSKU, productDes, productUnitPrice, productQuantity, orderSubtotal, orderShipping, orderDiscount, orderTax, orderGrandTotal, orderRefund]
            pdData.index = pdData.index + 1
            self.outputData = pd.concat([self.outputData, pdData])
            #print(self.outputData)

    #'Title','Company','First Name','Middle Name','Last Name','Suffix','Display Name As','Print On Check As','Billing Address Line 1','Billing Address Line 2','Billing Address Line 3','Billing Address City','Billing Address Postal Code','Billing Address Country','Billing Address State','Shipping Address Line 1','Shipping Address Line 2','Shipping Address Line 3','Shipping Address City','Shipping Address Postal Code','Shipping Address Country','Shipping Address State','Phone','Mobile','Fax','Other','Website','Email','Terms','Preferred Payment Method','Tax Resale No','Preferred Delivery Method','Bill With Parent','Parent Customer','Opening Balance','Open Balance Date','Notes','Customer Taxable','Currency Code'
    def formatAndExportCust(self):
        cusData = pd.DataFrame(columns=self.formatedCustomerData.columns)
        uniqueNamesData = self.outputData.drop_duplicates(subset=['Bill Name'], keep='last')

        for index, row in uniqueNamesData.iterrows():
            firstName = row['Bill First']
            lastName = row['Bill Last']
            fullName = row['Bill Name']
            billAddr1 = row['Bill Address1']
            billAddr2 = row['Bill Address2']
            billAddr3 = row['Bill Address3']
            billCity = row['Bill City']
            billZip = row['Bill Zip']
            billCountry = row['Bill Country']
            billState = row['Bill State']

            shipAddr1 = row['Ship Address1']
            shipAddr2 = row['Ship Address2']
            shipAddr3 = row['Ship Address3']
            shipCity = row['Ship City']
            shipZip = row['Ship Zip']
            shipCountry = row['Ship Country']
            shipState = row['Ship State']
            
            if row['Bill Phone']:
                phone = row['Bill Phone']
            else:
                phone = row['Ship Phone']

            email = row['Email']

            cusData.loc[-1] = ['','',firstName,'',lastName,'',fullName,'',billAddr1,billAddr2,billAddr3,billCity,billZip,billCountry,billState,shipAddr1,shipAddr2,shipAddr3,shipCity,shipZip,shipCountry,shipState,phone,'','','','',email,'','','','','','','','','','','']
            cusData.index = cusData.index + 1
        self.formatedCustomerData = pd.concat([self.formatedCustomerData,cusData]).drop_duplicates(subset=['Display Name As'])

    #'Estimate No','Customer','Estimate Date','Expiration Date','Estimate Status','Accepted By','Accepted Date','Ship Via','Ship Date','Tracking No','Billing Address Line 1','Billing Address Line 2','Billing Address Line 3','Billing Address City','Billing Address Postal Code','Billing Address Country','Billing Address State','Shipping Address Line 1','Shipping Address Line 2','Shipping Address Line 3','Shipping Address City','Shipping Address Postal Code','Shipping Address Country','Shipping Address State','Memo','Message displayed on estimate','Email','Shipping','Sales Tax Code','Sales Tax Amount','Discount Amount','Discount Percent','Discount Account','Service Date','Product/Service','Product/Service Description','Product/Service Quantity','Product/Service Rate','Product/Service Amount','Product/Service Taxable','Product/Service Class','Show Sub Total','Apply Tax After Discount','Location','Custom Field Value (1)','Custom Field Value (2)','Custom Field Value (3)','Currency Code','Exchange Rate','Print Status','Email Status'
    #'ID','Purchase Date','Capture Date','PaymentMethod','Email','Bill Name','Bill First','Bill Last','Bill Address1','Bill Address2','Bill Address3','Bill City','Bill Country','Bill State','Bill Zip','Bill Phone','Ship Name','Ship First','Ship Last','Ship Address1','Ship Address2','Ship Address3','Ship City','Ship Country','Ship State','Ship Zip','Ship Phone','Product SKU','Product Description','Product Price','Product Quantity','Order Subtotal','Order Shipping Fee','Order Discount Total','Order Tax','Order Total', 'Refunded amount'
    def formatAndExportEst(self, data):
        estData = pd.DataFrame(columns=self.formatedEstimateData.columns)

        idNum = str(list(data.keys())[0])

        captureDate = data[idNum]['captureDate']
        orderDate = data[idNum]['orderedDate']
        paymentMethod = data[idNum]['payment']
        if 'PayPal' in paymentMethod:
            paymentMethod = 'PayPal'
        elif 'Credit' in paymentMethod:
            paymentMethod = 'Credit Card'
        elif 'Amazon' in paymentMethod:
            paymentMethod = 'Amazon Pay'
        elif 'Apple' in paymentMethod :
            paymentMethod = 'Apple Pay'
        elif 'Google' in paymentMethod :
            paymentMethod = 'Google Pay'
        elif 'Affirm' in paymentMethod :
            paymentMethod = 'Affirm'
        elif 'Wire' in paymentMethod :
            paymentMethod = 'Wire Transfer'
        else:
            paymentMethod = 'Others'

        email = data[idNum]['contact']['email']

        billFirst = data[idNum]['billing']['firstName']
        billLast = data[idNum]['billing']['lastName']
        billFull = billFirst + ' ' + billLast
        billAdd1 = data[idNum]['billing']['address1']
        billAdd2 = data[idNum]['billing']['address2']
        billAdd3 = data[idNum]['billing']['address3']
        billCity = data[idNum]['billing']['city']
        billCountry = data[idNum]['billing']['country']
        billState = data[idNum]['billing']['state']
        billZip = data[idNum]['billing']['zip']
        billPhone = data[idNum]['billing']['phone']

        shipFirst = data[idNum]['shipping']['firstName']
        shipLast = data[idNum]['shipping']['lastName']
        shipFull = shipFirst + ' ' + shipLast
        shipAdd1 = data[idNum]['shipping']['address1']
        shipAdd2 = data[idNum]['shipping']['address2']
        shipAdd3 = data[idNum]['shipping']['address3']
        shipCity = data[idNum]['shipping']['city']
        shipCountry = data[idNum]['shipping']['country']
        shipState = data[idNum]['shipping']['state']
        shipZip = data[idNum]['shipping']['zip']
        shipPhone = data[idNum]['shipping']['phone']

        orderDate = data[idNum]['orderedDate']

        discountDes = []
        discountAmt = []
        shipping = ''
        for key, val in data[idNum]['orderTotal'].items():
            if 'Discount' in key:
                discountDes.append(key)
                discountAmt.append(val)
            elif 'Shipping' in key:
                shipping = float(val.replace(',',''))
        
        orderDiscount = {}
        orderDiscount['discountDes'] = discountDes
        orderDiscount['discountAmt'] = discountAmt
        #print(orderDiscount)

        for i in range(len(data[idNum]['product']['SKU'])):
            productDes = data[idNum]['product']['productDescription'][i]
            productQuantity = data[idNum]['product']['quantity'][i]
            productSKU = data[idNum]['product']['SKU'][i]
            productPrice = data[idNum]['product']['unitPrice'][i].replace('$','').replace(',','')
            if i == 0:
                estData.loc[-1] = ['WS'+idNum, billFull, orderDate,'','Accepted','','','','','',billFull,billAdd1,(billAdd2 + ' ' + billAdd3) if billAdd3 else billAdd2,billCity,billZip,billCountry,billState,shipFull,shipAdd1,(shipAdd2 + ' ' + shipAdd3) if shipAdd3 else shipAdd2,shipCity,shipZip,shipCountry,shipState,paymentMethod,'','','','','','','','','','',productDes + '\n' + productSKU,productQuantity,productPrice,str(float(productQuantity)*float(productPrice)),'TRUE','WS - Direct Sales','','','','','','','','','FALSE','FALSE']
            else:
                estData.loc[-1] = ['WS'+idNum, '', '','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',productDes + '\n' + productSKU,productQuantity,productPrice,str(float(productQuantity)*float(productPrice)),'TRUE','WS - Direct Sales','','','','','','','','','FALSE','FALSE']

            estData.index = estData.index + 1

        for i in range(len(orderDiscount['discountDes'])):
            estData.loc[-1] = ['WS'+idNum, '', '','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Discounts or Refunds',orderDiscount['discountDes'][i],'1',orderDiscount['discountAmt'][i],orderDiscount['discountAmt'][i],'TRUE','WS - Direct Sales','','','','','','','','','FALSE','FALSE']
            estData.index = estData.index + 1

        if shipping > 0:
            estData.loc[-1] = ['WS'+idNum, '', '','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shipping','Shipping & Handling','1',shipping,shipping,'TRUE','WS - Direct Sales','','','','','','','','','FALSE','FALSE']
            estData.index = estData.index + 1

        if captureDate :
            estData.loc[-1] = ['WS'+idNum, '', '','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Payment received: ' + captureDate,'','','','','','','','','','','','','','FALSE','FALSE']
            estData.index = estData.index + 1

        self.formatedEstimateData = pd.concat([self.formatedEstimateData, estData])
        

    def saveToFailed(self,idNum, exportDir):
        self.failedOutput.loc[-1] = [idNum]
        self.failedOutput.index = self.failedOutput.index + 1

        self.exportToExcel(self.failedOutput, 'Failed', exportDir)

    def exportOutput(self, exportDir):
        self.exportToExcel(self.formatedEstimateData, 'WSEstimateUpload' ,exportDir)
        self.exportToExcel(self.formatedCustomerData, 'WSCustomerUpload', exportDir)
        self.exportToExcel(self.outputData, 'output', exportDir)

    def exportToExcel(self, data, exportName, exportDir):
        data.to_excel(exportDir + '/' + exportName + '.xlsx', index = False, header = True)

    def exportAllExcel(self, exportDir):
        self.processingData.to_excel(exportDir + '/' + 'processing.xlsx', index = False, header = True)
        if not self.holdedData.empty:
            self.holdedData.to_excel(exportDir + '/' + 'holded.xlsx', index = False, header = True)
        if not self.completedData.empty:
            self.completedData.to_excel(exportDir + '/' + 'complete.xlsx', index = False, header = True)
        if not self.closed_CancledData.empty:
            self.closed_CancledData.to_excel(exportDir + '/' + 'closed_Cancled.xlsx', index = False, header = True)
        if not self.unknownData.empty:
            self.unknownData.to_excel(exportDir + '/' + 'unknown.xlsx', index = False, header = True)