from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

def webWaitByXPATH(driver, duration, searchInfo):
    try:
        WebDriverWait(driver, duration).until(EC.presence_of_element_located((By.XPATH, searchInfo)))
    except Exception:
        return False
    else:
        return True

def webWaitByCSS(driver, duration, searchInfo):
    try:
        WebDriverWait(driver, duration).until(EC.presence_of_element_located((By.CSS_SELECTOR, searchInfo)))
    except Exception:
        return False
    else:
        return True

def eleByXPATH(driver, duration, searchInfo, errorMessage = ''):
    if(webWaitByXPATH(driver, duration, searchInfo)):
        return driver.find_element(By.XPATH, searchInfo)
    else:
        if errorMessage : print('Error: ' + errorMessage)
        return False

def elesByXPATH(driver, duration, searchInfo, errorMessage = ''):
    if(webWaitByXPATH(driver, duration, searchInfo)):
        return driver.find_elements(By.XPATH, searchInfo)
    else:
        if errorMessage : print('Error: ' + errorMessage)
        return False