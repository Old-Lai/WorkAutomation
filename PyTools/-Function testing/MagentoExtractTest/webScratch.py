#This is a demo of how to use magento to search for an order number
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

class WSWebScratch:
    driver = webdriver.Chrome()
    username = 'henry.lai'
    password = 'bvifKD^&owh29'

    def logIntoMagento(self):
        self.driver.get('https://www.watchshopping.com/admin_oy97dk/admin/index/index/key/a4ec8da08f849038b9a3056bd01918cb74e113e7b9824de7571a861b0d829e1e/')
        user_bar = self.driver.find_element("id","username")
        user_bar.send_keys(self.username)
        password_bar = self.driver.find_element("id","login")
        password_bar.send_keys(self.password)
        password_bar.send_keys(Keys.ENTER)

    def goToOrders(self):
        travel = self.driver.find_element(By.CSS_SELECTOR,"[href*='https://www.watchshopping.com/admin_oy97dk/sales/order']")
        link = travel.get_attribute('href')
        self.driver.get(link)

    def logIntoMagentoAndGoToOrders(self):
        self.logIntoMagento()
        self.goToOrders()


    def searchIDInOrders(self, idNum):
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fulltext"]')))
        search_bar = self.driver.find_element(By.XPATH, "//*[@id='fulltext']")
        search_bar.clear()
        search_bar.send_keys(idNum)
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div[4]/table/tbody/tr/td[2]/div')))
        search_bar.send_keys(Keys.ENTER)
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="container"]/div/div[4]/table/tbody/tr/td[2]/div'), idNum))
        viewButton = self.driver.find_elements(By.XPATH, '//*[@id="container"]/div/div[4]/table/tbody/tr/td[10]/a')
        if(len(viewButton) > 0):
            viewButton[0].click()
            return True
        else:
            return False

    def goToBillingEdit(self):
        list = {}
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sales_order_view_tabs_order_info_content"]/section[4]/div[2]/div[1]/div/div/a')))
        edit_button = self.driver.find_element(By.XPATH, '//*[@id="sales_order_view_tabs_order_info_content"]/section[4]/div[2]/div[1]/div/div/a')
        self.driver.get(edit_button.get_attribute('href'))
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="firstname"]')))
        list['BFirstName'] = self.driver.find_element(By.XPATH, '//*[@id="firstname"]').get_attribute('value')
        list['BLastName'] = self.driver.find_element(By.XPATH, '//*[@id="lastname"]').get_attribute('value')
        list['BStreet1'] = self.driver.find_element(By.XPATH, '//*[@id="street0"]').get_attribute('value')
        list['BStreet2'] = self.driver.find_element(By.XPATH, '//*[@id="street1"]').get_attribute('value')
        list['BStreet3'] = self.driver.find_element(By.XPATH, '//*[@id="street2"]').get_attribute('value')
        list['BCity'] = self.driver.find_element(By.XPATH, '//*[@id="city"]').get_attribute('value')
        list['BZip'] = self.driver.find_element(By.XPATH, '//*[@id="postcode"]').get_attribute('value')
        list['BPhone'] = self.driver.find_element(By.XPATH, '//*[@id="telephone"]').get_attribute('value')

        selectEle = Select(self.driver.find_element(By.XPATH, '//*[@id="country_id"]'))
        selectEle = selectEle.first_selected_option
        list['BCountry'] = selectEle.text
        selectEle = Select(self.driver.find_element(By.XPATH, '//*[@id="region_id"]'))
        selectEle = selectEle.first_selected_option
        list['BState'] = selectEle.text

        list['BFullName'] = list['BFirstName'] + ' ' + list['BLastName']
        list['BFullAddress'] = list['BFullName'] + '\n' + list['BStreet1']
        if(list['BStreet2']):
            list['BFullAddress'] = list['BFullAddress'] + '\n' + list['BStreet2']
        if(list['BStreet3']):
            list['BFullAddress'] = list['BFullAddress'] + '\n' + list['BStreet3']
        list['BFullAddress'] += '\n' + list['BCity'] +', ' + list['BState'] + ' ' + list['BZip']
        list['BFullAddress'] += '\n' + list['BCountry']
        return list

    def goBackAPage(self):
        self.driver.execute_script("window.history.go(-1)")

    def goToShippingEdit(self):
        list = {}
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sales_order_view_tabs_order_info_content"]/section[4]/div[2]/div[2]/div/div/a')))
        edit_button = self.driver.find_element(By.XPATH, '//*[@id="sales_order_view_tabs_order_info_content"]/section[4]/div[2]/div[2]/div/div/a')
        self.driver.get(edit_button.get_attribute('href'))
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="firstname"]')))
        list['SFirstName'] = self.driver.find_element(By.XPATH, '//*[@id="firstname"]').get_attribute('value')
        list['SLastName'] = self.driver.find_element(By.XPATH, '//*[@id="lastname"]').get_attribute('value')
        list['SStreet1'] = self.driver.find_element(By.XPATH, '//*[@id="street0"]').get_attribute('value')
        list['SStreet2'] = self.driver.find_element(By.XPATH, '//*[@id="street1"]').get_attribute('value')
        list['SStreet3'] = self.driver.find_element(By.XPATH, '//*[@id="street2"]').get_attribute('value')
        list['SCity'] = self.driver.find_element(By.XPATH, '//*[@id="city"]').get_attribute('value')
        list['SZip'] = self.driver.find_element(By.XPATH, '//*[@id="postcode"]').get_attribute('value')
        list['SPhone'] = self.driver.find_element(By.XPATH, '//*[@id="telephone"]').get_attribute('value')
        selectEle = Select(self.driver.find_element(By.XPATH, '//*[@id="country_id"]'))
        selectEle = selectEle.first_selected_option
        list['SCountry'] = selectEle.text
        selectEle = Select(self.driver.find_element(By.XPATH, '//*[@id="region_id"]'))
        selectEle = selectEle.first_selected_option
        list['SState'] = selectEle.text

        list['SFullName'] = list['SFirstName'] + ' ' + list['SLastName']
        list['SFullAddress'] = list['SFullName'] + '\n' + list['SStreet1']
        if(list['SStreet2']):
            list['SFullAddress'] = list['SFullAddress'] + '\n' + list['SStreet2']
        if(list['SStreet3']):
            list['SFullAddress'] = list['SFullAddress'] + '\n' + list['SStreet3']
        list['SFullAddress'] += '\n' + list['SCity'] +', ' + list['SState'] + ' ' + list['SZip']
        list['SFullAddress'] += '\n' + list['SCountry']
        return list

    def completedTask(self):
        self.driver.close()
