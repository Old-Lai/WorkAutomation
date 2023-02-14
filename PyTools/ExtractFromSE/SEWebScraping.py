from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

import sys
sys.path.append('Credentials')
sys.path.append('PyTools/myToolHelpers')
import loginDetails
from webScratchHelper import *

class SEWebScrap:
    driver = webdriver.Chrome()
    username = loginDetails.shippingEasy_username
    password = loginDetails.shippingEasy_password

    def logIntoSE(self):
        self.driver.get('https://app1.shippingeasy.com/login')
        if(webWaitByXPATH(self.driver, 10, '//*[@id="user_email"]')):
            user_bar = self.driver.find_element(By.XPATH, '//*[@id="user_email"]')
            user_bar.send_keys(self.username)
        else:
            print('Login element not found!!')
            return False
        if(webWaitByXPATH(self.driver, 10, '//*[@id="user_password"]')):
            password_bar = self.driver.find_element(By.XPATH, '//*[@id="user_password"]')
            password_bar.send_keys(self.password)
            password_bar.send_keys(Keys.ENTER)
        else:
            print('Login element not found!!')
            return False
        return True

    def searchID(self, idNum):
        searchBar = eleByXPATH(self.driver, 5, '//input[@id="input_2"]','search bar not found')
        if not searchBar : return
        searchBar.send_keys(idNum)
        searchBar.send_keys(Keys.ENTER)

    def extractDetails(self):
        statusEles = elesByXPATH(self.driver, 3, '//div[@class="column-layout"]/div/dl', 'status section not found')
        if not statusEles : return
        for statusEle in statusEles:
            status = elesByXPATH(statusEle, 2, './/dd')
            statusTitles = elesByXPATH(statusEle, 2,'.//dt')
            for i in range(len(statusTitles)):
                print(statusTitles[i].text + ':  ' + status[i].text)



    def close(self):
        self.driver.close()
