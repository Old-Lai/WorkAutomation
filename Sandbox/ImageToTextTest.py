from PIL import Image
import pytesseract
from pdf2image import convert_from_path

# imagePath = '/Users/henry/Documents/Others/PyArguments/InvoicesList/img.pdf'
# pdfPages = convert_from_path(imagePath, 500)
# for page_enum, page in enumerate(pdfPages, start=1):
#     page.save('/Users/henry/Documents/Others/PyArguments/InvoicesList/img.jpg', 'JPEG')

img = Image.open('/Users/henry/Documents/Others/PyArguments/InvoicesList/img.jpg')

text = pytesseract.image_to_string(img)

print(text[:-1])