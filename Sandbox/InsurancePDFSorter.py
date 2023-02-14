import PyPDF2
import re
import sys, os

filePath = '/Users/henry/Documents/Others/PyArguments/InvoicesList/invoice.pdf'
pdfFileObj = open(filePath, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)

insPdfWriter = PyPDF2.PdfFileWriter()
regPdfWriter = PyPDF2.PdfFileWriter()

numOfPage = pdfReader.numPages
print(numOfPage)

for i in range(numOfPage):
    pageObj = pdfReader.getPage(i)
    pageText = pageObj.extractText()

    invoiceNum = pageText[pageText.find('INVOICE #')+10:pageText.find('DATE')-1]
    totalAmt = eval(pageText[re.search(r'\bBALANCE DUE\b', pageText).start()+16:].replace(',',''))

    if totalAmt >= 500:
        insPdfWriter.addPage(pageObj)
    else:
        print(invoiceNum)
        regPdfWriter.addPage(pageObj)

insPdfOutput = open('/Users/henry/Documents/Others/PyArguments/InvoicesList/' + 'insInvoice.pdf', 'wb')
regPdfOutput = open('/Users/henry/Documents/Others/PyArguments/InvoicesList/' + 'regInvoice.pdf', 'wb')

print(insPdfWriter.getNumPages())
print(regPdfWriter.getNumPages())

insPdfWriter.write(insPdfOutput)
regPdfWriter.write(regPdfOutput)