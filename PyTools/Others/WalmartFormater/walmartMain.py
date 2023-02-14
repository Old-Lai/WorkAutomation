import pandas as pd
import re
import sys, os
import datetime
os.system('clear')

title  = "#########################\n"
title += "# Walmart File Formater #\n"
title += "#########################\n"

def readFile():
    print(title)
    canReadFile = False
    while not canReadFile:
        print("Feed me report (drag and drop excel file here, then press enter):")
        filePath = input()
        try:
            data = pd.read_excel(filePath.strip().replace('\'',''))
            if not 'PO#' in data:
                raise ImportError()
            canReadFile = True
        except ImportError:
            os.system('clear')
            print(title)
            print("Could not find PO# column in excel file!! (reminder, this is for Walmart report)\n\n")
        except:
            os.system('clear')
            print(title)
            print("file cannot be read or is not an excel file\n\n")
    return data

def processReport(data = pd.DataFrame()):
    outputData = pd.DataFrame(columns=['PO#','Order Date','Customer Name','First Name','Last Name','Customer Phone Number','Ship to Address 1','Ship to Address 2','City','State','Zip','Item Description','Qty','SKU','Item Cost','Tax','Total Cost','Brand Name'])
    for index, row in data.iterrows():
        orderNum = 'PO# ' + str(row['PO#'])
        orderDate = row['Order Date']
        cusName = row['Customer Name']
        firstName = cusName[:cusName.find(' ')]
        lastName = cusName[cusName.find(' '):]
        cusPhone = row['Customer Phone Number']
        address1 = row['Ship to Address 1']
        address2 = row['Ship to Address 2']
        city = row['City']
        state = row['State']
        zip = row['Zip']

        sku = re.search(r"(\w+[\d.]+[\w\d.]+)", row['Item Description'])
        skuLessDes = row['Item Description'].replace(sku.group() if sku else '', '')

        des = " ".join((skuLessDes + ' ' + row['SKU']).split())
        quantity = row['Qty']
        sku = row['SKU']
        itemCost = row['Item Cost']
        tax = row['Tax']
        totCost = itemCost * quantity + row['Shipping Cost']
        #brand = row['Brand']
        grabbedBrand = row['Item Description'][:row['Item Description'].strip().find(' ')].title()
        if grabbedBrand.title().find("Michael") != -1:
            grabbedBrand = "Michael Kors"
        elif grabbedBrand.title().find("Armani") != -1 or grabbedBrand.title().find("Emporio") != -1:
            grabbedBrand = "Emporio Armani"
        brand = grabbedBrand

        outputData.loc[-1] = [orderNum,orderDate,cusName,firstName,lastName,cusPhone,address1,address2,city,state,zip,des,quantity,sku,itemCost,tax,totCost,brand]
        outputData.index += 1
    return outputData

def getBrandFromUser(data = pd.DataFrame()):
    done = False
    brand = []
    index = 0
    while not done:
        os.system('clear')
        print(title)

        sku = re.search(r"(\w+[\d.]+[\w\d.]+)", data['Item Description'][index])
        skuLessDes = data['Item Description'][index].replace(sku.group() if sku else '', '')
        des = " ".join((skuLessDes + ' ' + data['SKU'][index]).split())

        print("Description: " + des)
        print("SKU: " + data['SKU'][index])
        grabbedBrand = data['Item Description'][index][:data['Item Description'][index].strip().find(' ')].title()
        if grabbedBrand.title().find("Michael") != -1:
            grabbedBrand = "Michael Kors"
        elif grabbedBrand.title().find("Armani") != -1 or grabbedBrand.title().find("Emporio") != -1:
            grabbedBrand = "Emporio Armani"
        print("Brand: " + grabbedBrand)
        print("\n Is the brand correct?(y/n)")
        answer = input()
        if(answer.lower().find('y') != -1):
            brand.append(grabbedBrand)
        else:
            print("Enter correct brand name: ")
            answer = input()
            brand.append(answer)
        
        if index + 1 < len(data['Item Description']):
            index += 1
        else:
            os.system('clear')
            print(title)
            tempData = pd.DataFrame(data["SKU"]).assign(Brand = brand)
            print(tempData)
            print("Everything looks good?(y/n)")
            answer = input()
            if(answer.lower().find('y') != -1):
                done = True
            else:
                brand = []
                index = 0
    data = data.assign(Brand = brand)
    return data

def formatOthers(pData = pd.DataFrame()):
    today = datetime.date.today()
    today = today.strftime('%m-%d-%Y')

    seUpload = pd.DataFrame(columns=['Order Number','Order Date','Status','Order Total','Requested Service','Shipping Cost','Custom 1','Custom 2','Custom 3','Item Name','Item SKU','Item Unit Price','Item Quantity','Item Unit Weight (oz)','Warehouse Bin','Full Name','First Name','Last Name','Address Line 1','Address Line 2','City','State/Province','Zip/Postal Code','Country','Company','Email','Phone','Notes'])
    cusData = pd.DataFrame(columns=['Title','Company','First Name','Middle Name','Last Name','Suffix','Display Name As','Print On Check As','Billing Address Line 1','Billing Address Line 2','Billing Address Line 3','Billing Address City','Billing Address Postal Code','Billing Address Country','Billing Address State','Shipping Address Line 1','Shipping Address Line 2','Shipping Address Line 3','Shipping Address City','Shipping Address Postal Code','Shipping Address Country','Shipping Address State','Phone','Mobile','Fax','Other','Website','Email','Terms','Preferred Payment Method','Tax Resale No','Preferred Delivery Method','Bill With Parent','Parent Customer ','Opening Balance','Open Balance Date','Notes','Customer Taxable','Currency Code'])
    estData = pd.DataFrame(columns=['Estimate No','Customer','Estimate Date','Expiration Date','Estimate Status','Accepted By','Accepted Date','Ship Via','Ship Date','Tracking No','Billing Address Line 1','Billing Address Line 2','Billing Address Line 3','Billing Address City','Billing Address Postal Code','Billing Address Country','Billing Address State','Shipping Address Line 1','Shipping Address Line 2','Shipping Address Line 3','Shipping Address City','Shipping Address Postal Code','Shipping Address Country','Shipping Address State','Memo','Message displayed on estimate','Email','Shipping','Sales Tax Code','Sales Tax Amount','Discount Amount','Discount Percent','Discount Account','Service Date','Product/Service','Product/Service Description','Product/Service Quantity','Product/Service Rate','Product/Service Amount','Product/Service Taxable','Product/Service Class ','Show Sub Total','Apply Tax After Discount','Location','Custom Field Value (1)','Custom Field Value (2)','Custom Field Value (3)','Currency Code','Exchange Rate','Print Status','Email Status'])
    estTaxData = pd.DataFrame(columns=estData.columns)
    for index, row in pData.iterrows():
        orderNum = row['PO#']
        orderDate = row['Order Date']
        cusName = row['Customer Name']
        firstName = row['First Name']
        lastName = row['Last Name']
        cusPhone = row['Customer Phone Number']
        address1 = row['Ship to Address 1']
        address2 = row['Ship to Address 2']
        city = row['City']
        state = row['State']
        zip = row['Zip']
        des = row['Item Description']
        quantity = row['Qty']
        sku = row['SKU']
        itemCost = row['Item Cost']
        tax = row['Tax']
        totCost = row['Total Cost']
        brand = row['Brand Name']
        seUpload.loc[-1] = [orderNum,orderDate,'',totCost,'','','','','',sku,sku,'',quantity,'','',cusName,'','',address1,address2,city,state,zip,'USA','','',cusPhone,'']
        seUpload.index += 1
        cusData.loc[-1] = ['','',firstName,'',lastName,'',cusName,'',address1,address2,'',city,zip,'USA',state,address1,address2,'',city,zip,'USA',state,cusPhone,'','','','','','','','','','FALSE','','','','','','']
        cusData.index += 1
        estTaxData.loc[-1] = [orderNum,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Walmart Sales Tax','Sales tax remitted by Walmart','1',tax,tax,'FALSE','','','','','','','','','','FALSE','FALSE']
        estTaxData.index += 1
        estData.loc[-1] = [orderNum,cusName,today,'','Accepted','','','','','',cusName,address1,address2,city,zip,'USA',state,cusName,address1,address2,city,zip,'USA',state,'','','','','','','','','','',brand,des,quantity,itemCost,totCost,'FALSE','Walmart - Direct Sales','','','','','','','','','FALSE','FALSE']
        estData.index += 1

    estData = pd.concat([estData,estTaxData])
    exportToExcel(seUpload, today + " WM_SEUpload")
    exportToExcel(cusData, today + " WM_CusUpload")
    exportToExcel(estData, today + " WM_EstUpload")
        





def exportToExcel(data, fileName):
    currentPath = os.path.dirname(sys.executable) + '/'
    data.to_excel(currentPath + fileName + '.xlsx', index = False, header = True)
    

os.system('clear')
data = readFile()
#data = getBrandFromUser(data)
pData = processReport(data)
exportToExcel(pData, "processedReport")
formatOthers(pData)