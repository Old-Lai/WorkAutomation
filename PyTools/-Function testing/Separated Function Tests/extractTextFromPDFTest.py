import PyPDF2
import pandas as pd

data = pd.DataFrame(columns=['firstname', 'lastname', 'address', 'city', 'state', 'zip', 'country', 'tracking', 'brand', 'description', 'orderNum', 'price'], index = range(1,10))

pdfFileObj = open('/Users/henry/Documents/Others/PyTools/whatnot/downloaded/2.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#print(pdfReader.numPages)

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

addressArr = textArr[shipsToIndex + 2]
addressArr = addressArr.split('.')
address = addressArr[0].strip()
city = addressArr[1][:addressArr[1].find(',')].strip()
state = addressArr[1][addressArr[1].find(',')+1:].strip()
zip = addressArr[2].strip()
country = addressArr[3].strip()

tracking = textArr[shipsToIndex + 3]
tracking = tracking[tracking.find(':')+2:]

brand = textArr[shipsToIndex + 5]
brand = brand.split(' ')
brand = brand[2].title()
if(brand == 'Emporio' or brand == 'Armani'):
    brand = 'Emporio Armani'

pageObj = pdfReader.getPage(1)
pageText = pageObj.extractText()
textArr = pageText.split('\n')

description = ""
orderNum = ""
price = ""

for text in textArr:
    if(text.find('Order:') >= 0):
        orderNum += text
    elif(text.find('Price:') >= 0):
        price += text
    elif(text.find('Total:') >= 0):
        donth = ""
    else:
        description += text

description = description[description.find(':')+2:]
orderNum = orderNum[orderNum.find(':')+2:]
price = price[price.find(':')+3:]

list = [firstname, lastname, address, city, state, zip, country, tracking, brand, description, orderNum, price]

data.iloc[0,:] = list

data.to_excel(r'/Users/henry/Documents/Testing.xlsx', index = False, header = True)

pdfFileObj.close()
