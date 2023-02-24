import pdfplumber
import re

class AMEXReader:
    filePath = '/Users/henry/Documents/Reconcile/Amex/pdf/test.pdf'
    pdfFileObj = None

    def __init__(self, filePath):
        self.filePath = filePath
        self.pdfFileObj = pdfplumber.open(filePath)

    def getBalances(self):
        pageObj = self.pdfReader.getPage(0)
        pageText = pageObj.extractText()
        # print('--------Analyzed--------')
        searchResult = re.search(r'Prepared For AccountNumber ClosingDate',pageText)
        startIndx = searchResult.start()
        endIndx = searchResult.end()
        closingDate = pageText[startIndx - 8:startIndx]
        # print('Closing Date:', closingDate)

        searchResult = re.search(r'OtherCredits\$',pageText)
        startIndx = searchResult.end()
        searchResult = re.search(r'Payments \$',pageText)
        endIndx = searchResult.start()
        other_credits = eval(pageText[startIndx+1:endIndx].replace(',',''))
        # print('Other Credits:', other_credits)

        searchResult = re.search(r'OtherDebits\$',pageText)
        startIndx = searchResult.end()
        searchResult = re.search(r'Balance\nDue',pageText)
        endIndx = searchResult.start()
        balances = pageText[startIndx+1:endIndx].replace(',','').split(' ')
        other_debits = eval(balances[0])
        new_charges = eval(balances[1])
        previous_balance = eval(balances[2])
        payments = eval(balances[3])
        # print('Previous Balance:', previous_balance)
        # print('New Charges:', new_charges)
        # print('Other Debits:', other_debits)
        # print('Payments:', payments)


    def __getRawTransactionLines(self, page):
        pageObj = self.pdfFileObj.pages[page]
        pageText = pageObj.extract_text()
        pageLine = pageText.split('\n')
        # print(pageText)
        # print('--------Analyzed--------', page)


        statementStart = next((index for index in range(len(pageLine)) if (re.search(r'[\-0-9\,]*\.[0-9]{2}', pageLine[index]) is not None and (re.search(r'\bForeignSpending\b', pageLine[index-1]) is not None or re.search(r'baserateplus', pageLine[index-1])is not None))),-1)
        statementEnd = next((index for index in range(len(pageLine)) if re.search(r'\bContinued\b', pageLine[index]) or re.search(r'Totalfor', pageLine[index])), -1)

        if(statementStart != -1):
            statementLines = pageLine[statementStart:statementEnd]

            transactionLines = []
            combiner = []
            count = 0
            for line in statementLines:
                # print(line)
                #if it's the first transaction line of the page
                if len(transactionLines) == 0:
                    combiner.append(line)
                    #when found second transaction, save first
                    if count:
                        # print(combiner)
                        if(re.search(r'[0-9]*\.[0-9]{2}',line)):
                            transactionLines.append(' '.join(combiner[:-1]))
                            combiner = []
                            #save and add current line
                            combiner.append(line)
                    count += 1
                else:
                    if(re.search(r'[0-9]*\.[0-9]{2}',line)):
                        transactionLines.append(' '.join(combiner))
                        combiner = []
                        combiner.append(line)
                    else:
                        combiner.append(line)
            transactionLines.append(' '.join(combiner))

            return transactionLines
        else:
            return None

    def getTransactionLines(self, pageNum):
        rawTransactions = self.__getRawTransactionLines(pageNum)
        if rawTransactions:
            fedexTransactions = []
            for transaction in rawTransactions:
                amtRes = re.search(r'[\-0-9\,]*\.[0-9]{2}', transaction)
                amount = transaction[amtRes.start(): amtRes.end()]
                if 'FEDEX' in transaction:
                    fedexTransactions.append({
                        transaction,
                        amount
                    })
                    print(transaction)

amex = AMEXReader('/Users/henry/Documents/Reconcile/Amex/pdf/2022-12-28.pdf')
amex.getTransactionLines(6)