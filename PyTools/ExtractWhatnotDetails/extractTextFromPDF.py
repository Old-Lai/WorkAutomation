import PyPDF2

def extractFromFile(filePath):
    pdfFileObj = open(filePath, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
    totalPages = pdfReader.numPages

    pageObj = pdfReader.getPage(0)
    pageText = pageObj.extractText()
    textArr = pageText.split('\n')
    shipsToIndex = 0

    for index in range(len(textArr)):
        if(textArr[index] == 'Ships to:'):
            shipsToIndex = index

    name = textArr[shipsToIndex + 1]
    name = name[:name.find('(') - 1]
    firstname = name[:name.find(' ')]
    lastname = name[name.find(' ') + 1:]

    addressArr = ''
    for line in textArr[shipsToIndex+2:]:
        if(line.find('Tracking code:') >= 0):
            break
        addressArr += line

    addressArr = addressArr.split('.')
    address = addressArr[0].strip()
    city = addressArr[1][:addressArr[1].find(',')].strip()
    state = addressArr[1][addressArr[1].find(',')+1:].strip()
    zip = addressArr[2].strip()
    country = addressArr[3].strip()

    tracking = ''
    for line in textArr:
        if(line.find('Tracking code:')>=0):
            tracking = line[line.find(':')+2:]
            break

    brand = []
    descriptionLine = ''
    description = []
    orderNum = []
    price = []
    partOfName = False
    for line in textArr[shipsToIndex:]:
        if(line.find('Name:')>=0):
            editedLine = line[line.find('Name:'):]
            brand.append(editedLine.split(' ')[1].title())
            partOfName = True
        elif(line.find('Order:')>=0):
            orderNum.append(line[line.find(':')+2:])
        elif(line.find('Quantity:')>=0):
            partOfName = False
            description.append(descriptionLine[descriptionLine.find(':')+2:])
            descriptionLine = ''
        elif(line.find('Price:')>=0):
            price.append(line[line.find(':')+3:])

        if(partOfName):
            descriptionLine += line + ' '
        

    #anypages other than first page

    for pageNum in range(1,totalPages - 1):
        pageObj = pdfReader.getPage(pageNum)
        pageText = pageObj.extractText()
        textArr = pageText.split('\n')
        descriptionLine = ''
        
        for line in textArr:
            if(line.find('Name:')>=0):
                editedLine = line[line.find('Name:'):]
                brand.append(editedLine.split(' ')[1].title())
                partOfName = True
            elif(line.find('Order:')>=0):
                orderNum.append(line[line.find(':')+2:])
            elif(line.find('Quantity:')>=0):
                partOfName = False
                description.append(descriptionLine[descriptionLine.find(':')+2:])
                descriptionLine = ''
            elif(line.find('Price:')>=0):
                price.append(line[line.find(':')+3:])

            if(partOfName):
                descriptionLine += line + ' '

    for i in range(len(brand)):
        if(brand[i] == 'Emporio' or brand[i] == 'Armani'):
            brand[i] = 'Emporio Armani'

    fullname = firstname + ' ' + lastname
    list = [fullname, firstname, lastname, address, city, state, zip, country, tracking, brand, description, orderNum, price]
    print(list)
    pdfFileObj.close()
    return list
