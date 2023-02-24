# import PyPDF2
# import re

# filePath = '/Users/henry/Documents/Reconcile/Amex/pdf/test.pdf'
# pdfFileObj = open(filePath, 'rb')
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
# pageObj = pdfReader.getPage(0)
# pageText = pageObj.extractText()
# pageLines = pageText.split('\n')
# print(pageText)

import pdfplumber

with pdfplumber.open(r'/Users/henry/Documents/Reconcile/Amex/pdf/2022-12-28.pdf') as pdf:
    first_page = pdf.pages[0]
    print(first_page.extract_text())