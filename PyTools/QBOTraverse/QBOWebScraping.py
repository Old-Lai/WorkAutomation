from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

import sys
sys.path.append('/Users/henry/Documents/Others/WorkSpace/WatchShoppingAutomation/Credentials')
sys.path.append('/Users/henry/Documents/Others/WorkSpace/WatchShoppingAutomation/PyTools/myToolHelpers')
import loginDetails
from webScratchHelper import *

class QBOWebScrap:
    driver = webdriver.Chrome()
    username = loginDetails.QBO_username
    password = loginDetails.QBO_password

    def loginToQBO(self):
        self.driver.get('https://app.qbo.intuit.com/app/homepage')
        user_bar = eleByXPATH(self.driver, 10, '//*[@id="iux-identifier-first-international-email-user-id-input"]', 'QBO login element not found!!!!')
        if not user_bar : return
        user_bar.clear()
        user_bar.send_keys(self.username)
        user_bar.send_keys(Keys.ENTER)

        pass_bar = eleByXPATH(self.driver, 10, '//*[@id="iux-password-confirmation-password"]', 'QBO login element not found!!!!')
        if not pass_bar : return
        pass_bar.clear()
        pass_bar.send_keys(self.password)
        pass_bar.send_keys(Keys.ENTER)

    def openSearch(self):
        search_button = eleByXPATH(self.driver, 15, '//button[@data-id="search"]', 'QBO search button not found!!!!')
        if not search_button : return
        search_button.click()

    def searchOrder(self, idNum):
        print('Attempting ' + idNum + '.............')
        search_bar = eleByXPATH(self.driver, 15, '//input[@aria-label="Search"]', 'QBO search bar not found!!!!')
        if not search_bar : return
        search_bar.clear()
        search_bar.send_keys(idNum)

        searchEle = eleByXPATH(self.driver, 10, '//div[@class="Category__CategoryContainer-sc-1unw0w7-0 fEIJyV GlobalResults__StyledCategory-mf8t9s-1 kRbmnL"]', 'idNum not found')
        if not searchEle : return

        headerEles = elesByXPATH(searchEle, 10, './/div[@class="GlobalCategoryHeader__Header-sc-1snla1w-0 fXqgyU"]', 'Headers not found')
        if not headerEles : return
        for headerEle in headerEles:
            if(headerEle.text == 'TRANSACTIONS'):
                buttonEles = elesByXPATH(self.driver, 5, '//button[@class="FocusableButton__StyledButton-sc-1typn4h-0 llUVZq qbshared-core-search-ui-keyboard-focusable"]', 'options not found')
                if not buttonEles : return
                for buttonEle in buttonEles:
                    textArr = buttonEle.text.split('|')
                    if(textArr[0].find('Invoice') != -1):
                        print(textArr[0])
                        buttonEle.click()
                        return
    
    def findPaymentRecieved(self):
        WebDriverWait(self.driver, 3)
        desEles = elesByXPATH(self.driver, 10, '//td[@class="dgrid-cell dgrid-cell-padding dgrid-column-4 clickable field-description"]', 'tabel columns not found!!!')
        if not desEles : return
        for desEle in desEles:
            desText = eleByXPATH(desEle, 5, './/div').text
            if not desText.find('Payment received:') == -1:
                return True
        return False

    def addPaymentRecieved(self, estDate):
        desEles = elesByXPATH(self.driver, 5, '//td[@class="dgrid-cell dgrid-cell-padding dgrid-column-4 clickable field-description"]', 'tabel columns not found!!!')
        if not desEles : return
        for desEle in desEles:
            desText = eleByXPATH(desEle, 2, './/div').text
            if not desText:
                desEle.click()
                break

        
        textBox = eleByXPATH(self.driver, 4, '//div[@data-dojo-attach-point="_descriptionOverlayCell"]/textarea', 'Textbox not found!!!')
        if not textBox : return
        textBox.send_keys('Payment received: ' + estDate)

    def addClassToProducts(self):
        rowEles = elesByXPATH(self.driver, 4, '//td[@class="dgrid-cell dgrid-cell-padding dgrid-column-2 clickable field-itemId"]/parent::*', 'row elements not found')
        if not rowEles : return
        for rowEle in rowEles:
            productEle = eleByXPATH(rowEle, 1, './/td[@class="dgrid-cell dgrid-cell-padding dgrid-column-2 clickable field-itemId"]', 'product element not found')
            if (productEle) and productEle.text != ' ':
                classEle = eleByXPATH(rowEle, 1, './/td[@class="dgrid-cell dgrid-cell-padding dgrid-column-9 clickable field-klassId"]', 'class ele not found')
                classEle.click()

                inputEle = eleByXPATH(self.driver, 4, '//input[@aria-labelledby="txns-accessibilityInputClass"]', 'input not found!!!')
                inputEle.send_keys('WhatNot - Direct Sales')
                time.sleep(0.5)
                self.driver.find_element(By.XPATH, '//textarea[@data-automation-id="input-statement-memo-sales"]').click()
                time.sleep(0.5)
                
    def leaveWithoutSave(self):
        closeButton = eleByXPATH(self.driver, 2, '//i[@aria-label="Close"]', 'close button not found!!')
        if not closeButton : return
        self.driver.execute_script("arguments[0].click();", closeButton)

        yesButton = eleByXPATH(self.driver, 5, '//button[normalize-space()="Yes"]', 'cant find yes button after close button pressed!!!')
        if not yesButton : return
        yesButton.click()

    def saveAndClose(self):
        saveButton = eleByXPATH(self.driver, 5, '//button[text()="Save"]', 'save button not found')
        if not saveButton:return
        saveButton.click()

        time.sleep(2)
        confirmButton = eleByXPATH(self.driver, 5,'//div[@aria-labelledby="yesNoDialog_title"]/div/div[@data-dojo-attach-point="containerNode"]/div[@class="buttons "]/div[3]/button')
        if confirmButton:
            time.sleep(0.1)
            confirmButton.click()
            time.sleep(2)
            confirmButton2 = eleByXPATH(self.driver, 3,'//div[@role="dialog"]/div/div[@data-dojo-attach-point="containerNode"]/div[@class="buttons "]/div[2]/button')
            if confirmButton2:
                print(confirmButton2)
                time.sleep(0.1)
                confirmButton2.click()

        time.sleep(3.5)

        cancelButton = eleByXPATH(self.driver, 5, '//div[@data-extension-point="general-extension/universal-footer-left"]/button[text()="Cancel"]', 'cancel button not found!!')
        if not cancelButton : return
        time.sleep(0.1)
        cancelButton.click()
        print('Success')

    def gotoAdvSearch(self):
        self.openSearch()

        ele = eleByXPATH(self.driver, 20, '//a[text()="Advanced Search"]', 'QBO adv search button not found!!!!')
        if not ele : return
        ele.click()

    def setAdvSearch(self):
        if(webWaitByXPATH(self.driver, 20, '//div[@id="dijit_form_Select_1"]')):
            self.driver.find_element(By.XPATH, '//div[@id="dijit_form_Select_1"]').click()
            if(webWaitByXPATH(self.driver, 20, '//td[@id="dijit_MenuItem_16_text"]')):
                self.driver.find_element(By.XPATH, '//td[@id="dijit_MenuItem_16_text"]').click()
            else:
                print('Error: QBO adv search failed to select invoices')
        else:
            print('Error: failed to find QBO select 1 button')

        if(webWaitByXPATH(self.driver, 20, '//div[@id="dijit_form_Select_2"]')):
            self.driver.find_element(By.XPATH, '//div[@id="dijit_form_Select_2"]').click()
            if(webWaitByXPATH(self.driver, 20, '//td[@id="dijit_MenuItem_30_text"]')):
                self.driver.find_element(By.XPATH, '//td[@id="dijit_MenuItem_30_text"]').click()
            else:
                print('Error: QBO adv search faild to select invoice no.')
        else:
            print('Error: failed to find QBO select 2 button')

    def getEstDate(self):
        estEle = eleByXPATH(self.driver, 2, '//div[@class="dijitInline topFieldInput dijitTextBox dijitComboBox dijitDateTextBox dijitValidationTextBox"]/input[@type = "hidden"]', 'Estimate element not found')
        if not estEle : return
        dateStr = estEle.get_attribute('value')
        dateArr = dateStr.split('-')
        dateArr[2] = int(dateArr[2]) + 1
        dateStr = dateArr[1] + '/' + str(dateArr[2]) + '/' + dateArr[0]
        print(dateStr)
        return dateStr

    def checkShipping(self, shipAddr):
        time.sleep(4)
        qboShipEle = eleByXPATH(self.driver, 2, '//textarea[@id="shippingAddress"]', 'shipping element not found')
        if not qboShipEle : return
        shipAddrArr = shipAddr.split(' ')
        qboShipAddr = qboShipEle.get_attribute('value')
        for addr in shipAddrArr:
            if qboShipAddr.find(addr) < 0:
                print(addr + " not found!")
        return True

    def close(self):
        self.driver.close()
