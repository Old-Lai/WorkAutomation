import pandas as pd
import wget

def downloadPDFFile(reportPath, downloadPath):
    csv_data = pd.read_csv(reportPath, dtype=str)
    data = pd.DataFrame(csv_data)
    data = data[data['cancelled'] != 'Yes']
    numOfData = data.shape[0]
    data = data.drop_duplicates(subset=['tracking'], keep = 'last')
    links = data['shipment manifest']

    count = 0
    for link in links:
        print('\ndownloading ' + str(count + 1) + ' out of ' + str(len(links)))
        fileName = downloadPath + str(count) + '.pdf'
        wget.download(link, fileName)
        count = count + 1

    print('\n---------- download complete!!!! ----------\n')
    return numOfData
