from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

import sys
sys.path.append('Credentials')
sys.path.append('PyTools/myToolHelpers')
import loginDetails
from webScratchHelper import *

class MagentoWebScrap:
    driver = webdriver.Chrome()
    username = loginDetails.magento_username
    password = loginDetails.magento_password
    
    def loginToMagento(self):
        self.driver.get('https://www.watchshopping.com/admin_oy97dk/admin/index/index/key/aedc094374deb9f5ffa9c64e71abefa45ec41b1a0192029f08244204925c0d76/')
        userBar = eleByXPATH(self.driver, 10, '//input[@id="username"]', 'username field not found')
        if not userBar : raise Exception
        userBar.clear()
        userBar.send_keys(self.username)

        passBar = eleByXPATH(self.driver, 10, '//input[@id="login"]', 'password field not found')
        if not passBar : raise Exception
        passBar.clear()
        passBar.send_keys(self.password)
        passBar.send_keys(Keys.ENTER)

        return True

    def goToOrders(self):
        orderEle = eleByXPATH(self.driver, 10, '//li[@data-ui-id="menu-magento-sales-sales-order"]//a', 'order button not found')
        if not orderEle : raise Exception
        self.driver.get(orderEle.get_attribute('href'))

        return True

    def sesarchOrder(self, idNum):
        searchEle = eleByXPATH(self.driver, 10, '//*[@id="fulltext"]', 'searchbar not found')
        if not searchEle : raise Exception
        searchEle.clear()
        searchEle.send_keys(idNum)
        idEle = eleByXPATH(self.driver, 5, '//*[@id="container"]/div/div[4]/table/tbody/tr/td[2]/div', 'id Element not found')
        if not idEle : raise Exception
        searchEle.send_keys(Keys.ENTER)
        
        time.sleep(2)
        idEle = elesByXPATHTillTextExist(self.driver, 5, '//*[@id="container"]/div/div[4]/table/tbody/tr/td[2]/div', idNum, 'could not find Id from search result')
        if not idEle : raise Exception
        idEle = eleByXPATH(idEle, 1, '..')
        idEle = eleByXPATH(idEle, 1, '..')
        viewButton = eleByXPATH(idEle, 2, './/td[10]/a', 'view button not found')
        if not viewButton : raise Exception
        self.driver.get(viewButton.get_attribute('href'))

    def getBilling(self):
        editEle = eleByXPATH(self.driver, 10, '//div[@class="admin__page-section-item order-billing-address"]/div/div/a', 'billing edit not found')
        if not editEle : raise Exception
        self.driver.get(editEle.get_attribute('href'))

        data = {}
        firstName = eleByXPATH(self.driver, 5, '//input[@id="firstname"]')
        data['firstName'] = firstName.get_attribute('value')
        lastName = eleByXPATH(self.driver, 2, '//input[@id="lastname"]')
        nameStr = firstName.get_attribute('value')
        if(lastName.get_attribute('value') == '' and len(nameStr.split(' ')) > 1):
            data['firstName'] = nameStr.split(' ')[0]
            data['lastName'] = nameStr[nameStr.find(nameStr.split(' ')[1]):]
        else:
            data['lastName'] = lastName.get_attribute('value')
        address1 = eleByXPATH(self.driver, 2, '//input[@id="street0"]')
        data['address1'] = address1.get_attribute('value')
        address2 = eleByXPATH(self.driver, 2, '//input[@id="street1"]')
        data['address2'] = address2.get_attribute('value')
        address3 = eleByXPATH(self.driver, 2, '//input[@id="street2"]')
        data['address3'] = address3.get_attribute('value')
        city = eleByXPATH(self.driver, 2, '//input[@id="city"]')
        data['city'] = city.get_attribute('value')
        country = eleByXPATH(self.driver, 2, '//select[@id="country_id"]/option[@selected = "selected"]')
        data['country'] = country.text
        stateVal = eleByXPATH(self.driver, 2, '//select[@id="region_id"]')
        state = eleByXPATH(self.driver, 2,'//select[@id="region_id"]/option[@value=' + str(stateVal.get_attribute("defaultvalue")) + ']')
        if not state:
            state = eleByXPATH(self.driver, 2, '//input[@id="region"]')
            data['state'] = state.get_attribute('value')
        else:
            data['state'] = state.text
        zipCode = eleByXPATH(self.driver, 2, '//input[@id="postcode"]')
        data['zip'] = zipCode.get_attribute('value')
        phoneNum = eleByXPATH(self.driver, 2, '//input[@id="telephone"]')
        data['phone'] = phoneNum.get_attribute('value')

        self.goBackAPage()
        return data

    def getShipping(self):
        editEle = eleByXPATH(self.driver, 10, '//div[@class="admin__page-section-item order-shipping-address"]/div/div/a', 'shipping edit not found')
        if not editEle : raise Exception
        self.driver.get(editEle.get_attribute('href'))

        data = {}
        firstName = eleByXPATH(self.driver, 5, '//input[@id="firstname"]')
        data['firstName'] = firstName.get_attribute('value')
        lastName = eleByXPATH(self.driver, 2, '//input[@id="lastname"]')
        nameStr = firstName.get_attribute('value')
        if(lastName.get_attribute('value') == '' and len(nameStr.split(' ')) > 1):
            data['firstName'] = nameStr.split(' ')[0]
            data['lastName'] = nameStr[nameStr.find(nameStr.split(' ')[1]):]
        else:
            data['lastName'] = lastName.get_attribute('value')
        address1 = eleByXPATH(self.driver, 2, '//input[@id="street0"]')
        data['address1'] = address1.get_attribute('value')
        address2 = eleByXPATH(self.driver, 2, '//input[@id="street1"]')
        data['address2'] = address2.get_attribute('value')
        address3 = eleByXPATH(self.driver, 2, '//input[@id="street2"]')
        data['address3'] = address3.get_attribute('value')
        city = eleByXPATH(self.driver, 2, '//input[@id="city"]')
        data['city'] = city.get_attribute('value')
        country = eleByXPATH(self.driver, 2, '//select[@id="country_id"]/option[@selected = "selected"]')
        data['country'] = country.text
        stateVal = eleByXPATH(self.driver, 2, '//select[@id="region_id"]')
        state = eleByXPATH(self.driver, 2,'//select[@id="region_id"]/option[@value=' + str(stateVal.get_attribute("defaultvalue")) + ']')
        if not state:
            state = eleByXPATH(self.driver, 2, '//input[@id="region"]')
            data['state'] = state.get_attribute('value')
        else:
            data['state'] = state.text
        data['state'] = state.text
        zipCode = eleByXPATH(self.driver, 2, '//input[@id="postcode"]')
        data['zip'] = zipCode.get_attribute('value')
        phoneNum = eleByXPATH(self.driver, 2, '//input[@id="telephone"]')
        data['phone'] = phoneNum.get_attribute('value')

        self.goBackAPage()
        return data

    def getPaymentMethod(self):
        paymentEle = eleByXPATH(self.driver, 2, '//div[@class="order-payment-method-title"]', 'payment element not found')
        if not paymentEle : raise Exception
        paymentType = paymentEle.text.split('\n')[0]
        return paymentType

    def getProductDeatils(self):
        retObj = {}

        descriptionEles = elesByXPATH(self.driver, 2, '//div[@class="product-title"]', 'product description not found')
        if not descriptionEles : raise Exception
        descriptionArr = []
        for descriptionEle in descriptionEles:
            descriptionArr.append(descriptionEle.text)
        retObj['productDescription'] = descriptionArr

        skuEles = elesByXPATH(self.driver, 2, '//div[@class="product-sku-block"]', 'sku element not found')
        if not skuEles : raise Exception
        skuArr = []
        for skuEle in skuEles:
            skuArr.append(skuEle.text)
        retObj['SKU'] = skuArr

        unitPriceEles = elesByXPATH(self.driver, 2, '//td[@class="col-price"]/div[@class="price-excl-tax"]/span', 'unit price not found')
        if not unitPriceEles : raise Exception
        unitPriceArr = []
        for unitPriceEle in unitPriceEles:
            unitPriceArr.append(unitPriceEle.text)
        retObj['unitPrice'] = unitPriceArr

        quantityEles = elesByXPATH(self.driver, 2, '//table[@class="qty-table"]/tbody/tr[1]/td', 'quantity not found')
        if not quantityEles : raise Exception
        quantityArr = []
        for quantityEle in quantityEles:
            quantityArr.append(quantityEle.text)
        retObj['quantity'] = quantityArr

        return retObj
    
    def getOrderTotals(self):
        orderEles = elesByXPATH(self.driver,2,'//table[@class="data-table admin__table-secondary order-subtotal-table"]/tbody/tr', 'order totals table not found')
        if not orderEles : raise Exception
        data = {}
        for orderEle in orderEles:
            data[eleByXPATH(orderEle, 2, './/td[@class="label"]').text] = eleByXPATH(orderEle, 2, './/span[@class="price"]').text.replace('$', '')
        
        orderEles = elesByXPATH(self.driver, 2,'//table[@class="data-table admin__table-secondary order-subtotal-table"]/tfoot/tr', 'order totals table not found')
        if not orderEles : raise Exception
        for orderEle in orderEles:
            data[eleByXPATH(orderEle, 2, './/td[@class="label"]').text] = eleByXPATH(orderEle, 2, './/span[@class="price"]').text.replace('$', '')
        return data

    def getCapturedDate(self):
        noteEles = elesByXPATH(self.driver, 2, '//div[@id="order_history_block"]/ul[@class="note-list"]/li[@class="note-list-item"]','notes list not found')
        if not noteEles : raise Exception
        date = ''
        for noteEle in noteEles:
            time.sleep(0.5)
            note = eleByXPATH(noteEle, 2, './/div').text
            if(note.find('Captured amount') != -1):
                date = eleByXPATH(noteEle, 2, './/span[@class="note-list-date"]').text
                break
        #print(date)
        date = date.replace(',', '')
        date = datetime.strptime(date, '%b %d %Y').date()
        date = date.strftime('%m/%d/%Y')
        return date

    def getOrderedDate(self):
        orderEle = eleByXPATH(self.driver, 2, '//section[@class="admin__page-section order-view-account-information"]/div[@class="admin__page-section-content"]/div[1]/div[2]/table/tbody/tr[1]/td', 'order date not found')
        if not orderEle : raise Exception
        date = datetime.strptime(orderEle.text, '%b %d, %Y, %X %p').date()
        date = date.strftime('%m/%d/%Y')
        return date

    def getCustomerContact(self):
        #phone is already captured in shipping and billing
        data = {'email':''}
        emailEle = eleByXPATH(self.driver, 2, '//section[@class="admin__page-section order-view-account-information"]/div[@class="admin__page-section-content"]/div[2]/div[2]/table/tbody/tr[2]/td/a', 'email element not found')
        if not emailEle : raise Exception
        data['email'] = emailEle.text
        return data

    def goBackAPage(self):
        self.driver.execute_script("window.history.go(-1)")

    def close(self):
        self.driver.close()





