import PyPDF2
import datetime
import re

def extractLabel(filePath, fileNames, outputDir):
    pdfWriter = PyPDF2.PdfFileWriter()

    for fileName in fileNames:
        if(fileName.find('.pdf') >= 0):
            pdfFileObj = open(filePath + fileName, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
            lastPage = pdfReader.numPages-1
            pageObj = pdfReader.getPage(lastPage)
            pdfWriter.addPage(pageObj)
            pdfFileObj.close

    today = datetime.date.today()
    today = today.strftime('%m-%d-%Y')
    pdfLabelOutput = open(outputDir + today + ' WN Label.pdf', 'wb')
    pdfWriter.write(pdfLabelOutput)

    pdfLabelOutput.close

def extractFromFile(filePath):
    pdfFileObj = open(filePath, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
    totalPages = pdfReader.numPages

    pageObj = pdfReader.getPage(0)
    pageText = pageObj.extractText()
    textArr = pageText.split('\n')
    shipsToIndex = 0

    for index in range(len(textArr)):
        if(textArr[index] == 'Ships to:' or textArr[index] == '( NEW BUYER! )'):
            shipsToIndex = index

    name = textArr[shipsToIndex + 1]
    userName = name[name.find('('):]
    name = name[:name.find('(') - 1]
    firstname = name[:name.find(' ')]
    lastname = name[name.find(' ') + 1:]

    addressArr = ''
    for line in textArr[shipsToIndex+2:]:
        if(line.find('Tracking code:') >= 0):
            break
        addressArr += line

    addressArr = addressArr.split(',')
    address = ''
    for addressLine in ''.join(addressArr[:-1]).split('.')[:-1]:
        address += addressLine.strip() + ' '

    address = address.strip()
    city = ''.join(addressArr[:-1]).split('.')[-1]
    state = addressArr[-1].split('.')[0]
    zip = addressArr[-1].split('.')[1]
    country = addressArr[-1].split('.')[-1]

    tracking = ''
    for line in textArr:
        if(line.find('Tracking code:')>=0):
            tracking = line[line.find(':')+2:]
            break

    brand = []
    descriptionLine = ''
    descriptionLine2 = ''
    description = []
    description2 = []
    orderNum = []
    price = []
    partOfName = False
    partOfDes = False
    for line in textArr[shipsToIndex:]:
        if(line.find('Name:')>=0):
            editedLine = line[line.find('Name:'):]
            brand.append(editedLine.split(' ')[1].title())
            partOfName = True
        elif(line.find('Order:')>=0):
            partOfDes = False
            description2.append(descriptionLine2[descriptionLine2.find(':')+2:])
            descriptionLine2 = ''
            orderNum.append(line[line.find(':')+2:])
        elif(line.find('Quantity:')>=0):
            partOfName = False
            description.append(descriptionLine[descriptionLine.find(':')+2:])
            descriptionLine = ''
        elif(line.find('Description:')>=0):
            editedLine = line[line.find('Description:'):]
            partOfDes = True
        elif(line.find('Price:')>=0):
            price.append(line[line.find(':')+3:])

        if(partOfName):
            descriptionLine += line + ' '
        elif(partOfDes):
            descriptionLine2 += line + ' '        

    #anypages other than first page

    for pageNum in range(1,totalPages - 1):
        pageObj = pdfReader.getPage(pageNum)
        pageText = pageObj.extractText()
        textArr = pageText.split('\n')
        
        for line in textArr:
            if(line.find('Name:')>=0):
                editedLine = line[line.find('Name:'):]
                brand.append(editedLine.split(' ')[1].title())
                partOfName = True
            elif(line.find('Order:')>=0):
                partOfDes = False
                description2.append(descriptionLine2[descriptionLine2.find(':')+2:])
                descriptionLine2 = ''
                orderNum.append(line[line.find(':')+2:])
            elif(line.find('Quantity:')>=0):
                partOfName = False
                description.append(descriptionLine[descriptionLine.find(':')+2:])
                descriptionLine = ''
            elif(line.find('Description:')>=0):
                editedLine = line[line.find('Description:'):]
                partOfDes = True
            elif(line.find('Price:')>=0):
                price.append(line[line.find(':')+3:])

            if(partOfName):
                descriptionLine += line + ' '
            elif(partOfDes):
                descriptionLine2 += line + ' '  

    for i in range(len(brand)):
        brand[i] = brand[i].strip()
        if(brand[i] == 'Emporio' or brand[i] == 'Armani'):
            brand[i] = 'Emporio Armani'
        elif(brand[i] == 'Michael'):
            brand[i] = 'Michael Kors'

    for i in range(len(description)):
        description[i] = description[i].strip()
        if(description[i].lower().find('set') != -1 or description[i].lower().find('organizer') != -1 or description[i].lower().find('giveaway') != -1):
            brand[i] = ''

        if(description[i].lower().find('set') != -1):
            des2Arr = description2[i].split('+')
            count = 0
            for des in des2Arr:
                if des.lower().find('leather') == -1:
                    count += 1
            unitPrice = float(price[i])/count
            setName = description[i]
            description[i] = setName + ' (' + des2Arr[0].strip() + ')'
            if des2Arr[0].lower().find('leather') == -1:
                price[i] = unitPrice
            else:
                price[i] = '0.00'

            if len(des2Arr) > 1:
                for j in range(1,len(des2Arr)):
                    description.insert(i+j,setName + ' (' + des2Arr[j].strip() + ')')
                    brand.insert(i+j, '')
                    orderNum.insert(i+1, orderNum[i])
                    if des2Arr[j].lower().find('leather') == -1:
                        price.insert(i+j, unitPrice)
                    else:
                        price.insert(i+j, '0.00')


    for i in range(len(orderNum)):
        orderNum[i] = orderNum[i].strip()
        price[i] = str(price[i]).strip()
        
    userName = userName.strip()
    firstname = firstname.strip()
    lastname = lastname.strip()
    address = address.strip()
    city = city.strip()
    state = state.strip()
    zip = zip.strip()
    country = country.strip()
    tracking = tracking.strip()

    for i in range(len(brand)):
        brand[i] = re.sub(r'[^\w\s]', '',brand[i])

    fullname = firstname + ' ' + lastname
    list = [userName, fullname, firstname, lastname, address, city, state, zip, country, tracking, brand, description, orderNum, price]
    pdfFileObj.close()
    return list
