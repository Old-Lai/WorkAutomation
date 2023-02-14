import pandas as pd
import wget

csv_data = pd.read_csv('/Users/henry/Documents/Others/PyTools/whatnot/report.csv', dtype=str)
data = pd.DataFrame(csv_data)

print(data)

data = data[data['cancelled'] != 'Yes']

links = data['shipment manifest'].tolist()

count = 0
for link in links:
    fileName = '/Users/henry/Documents/Others/PyTools/whatnot/downloaded/' + str(count) + '.pdf'
    wget.download(link, fileName)
    count = count + 1
