import PyPDF2
import re

filePath = '/Users/henry/Documents/Others/PyArguments/InvoicesList/test.pdf'
pdfFileObj = open(filePath, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
pageObj = pdfReader.getPage(6)
pageText = pageObj.extractText()
pageLines = pageText.split('\n')
print(pageText)