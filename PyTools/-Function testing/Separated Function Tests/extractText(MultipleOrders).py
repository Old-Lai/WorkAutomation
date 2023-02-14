import pandas as pd

data = pd.DataFrame(columns=['firstname', 'lastname', 'address', 'city', 'state', 'zip', 'country', 'tracking', 'brand', 'description', 'orderNum', 'price'], index = range(1,10))

nestedList = [['a','b'],['1','2'],['3','4'],['5','6']]
firstname = 'first'
lastname = 'last'
address = 'addr'
city = 'cit'
state = 'sta'
zip = 'zip'
country = 'coun'
tracking = 'track'
brand = nestedList[0]
description = nestedList[1]
orderNum = nestedList[2]
price = nestedList[3]

list = [firstname, lastname, address, city, state, zip, country, tracking, brand, description, orderNum, price]

count = 3
for i in range(len(orderNum)):
    for j in range(len(list)):
        if(j < 8):
            data.iloc[count + i, j] = list[j]
        else:
            data.iloc[count + i, j] = list[j][i]

print(data)
