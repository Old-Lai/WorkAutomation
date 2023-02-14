from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

username = 'henry@watchshopping.com'
password = 'Ps16212045!'
driver = webdriver.Chrome()

def loginToQBO():
    driver.get('https://app.qbo.intuit.com/app/homepage')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ius-signin-userId-input"]')))
    user_bar = driver.find_element(By.XPATH, '//*[@id="ius-signin-userId-input"]')
    user_bar.clear()
    user_bar.send_keys(username)
    user_bar.send_keys(Keys.ENTER)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="iux-password-confirmation-password"]')))
    pass_bar = driver.find_element(By.XPATH, '//*[@id="iux-password-confirmation-password"]')
    pass_bar.clear()
    pass_bar.send_keys(password)
    pass_bar.send_keys(Keys.ENTER)

def searchID(idNum):
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.cssSelector, '[data-id="search"]')))
    search_bar = driver.find_element(By.cssSelector, '[data-id="search"]')
    search_bar.click()

def checkIfIDExist(idNum):
    WebDriverWait(driver,20).until(EC.presence_of_element_located(EC.presence_of_element_located((By.XPATH, '//*[@id="headerFlyoutNode-search"]/div/div/div/div/div[2]/div/div[2]/div[1]'))))
    transPanel = driver.find_element(By.XPATH, '//*[@id="headerFlyoutNode-search"]/div/div/div/div/div[2]/div/div[2]')

    transType = driver.find_element(By.XPATH, '//*[@id="headerFlyoutNode-search"]/div/div/div/div/div[2]/div/div[2]/div[1]')
    print(transType.text)


loginToQBO()
searchID('WS000369783')
#checkIfIDExist('WS000369783')
