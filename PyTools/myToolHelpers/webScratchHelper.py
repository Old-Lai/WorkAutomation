from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def webWaitTillTextExistByXPATH(driver, duration, searchXPATH, searchText):
    try:
        WebDriverWait(driver, duration).until(EC.text_to_be_present_in_element((By.XPATH, searchXPATH), searchText))
    except Exception:
        return False
    else:
        return True

def printError(errorMessage):
    if errorMessage : print('Error: ' + errorMessage)

def eleByXPATH(driver, duration, searchInfo, errorMessage = ''):
    if(webWaitByXPATH(driver, duration, searchInfo)):
        return driver.find_element(By.XPATH, searchInfo)
    else:
        printError(errorMessage)
        return False

def elesByXPATH(driver, duration, searchInfo, errorMessage = ''):
    if(webWaitByXPATH(driver, duration, searchInfo)):
        return driver.find_elements(By.XPATH, searchInfo)
    else:
        printError(errorMessage)
        return False

def eleByXPATHTillTextExist(driver, duration, searchXPATH, searchText, errorMessage = ''):
    if(webWaitTillTextExistByXPATH(driver, duration, searchXPATH, searchText)):
        return eleByXPATH(driver, duration, searchXPATH, errorMessage)
    else:
        printError(errorMessage)
        return False

def elesByXPATHTillTextExist(driver, duration, searchXPATH, searchText, errorMessage = ''):
    if(elesByXPATH(driver, duration, searchXPATH)):
        elements = elesByXPATH(driver, duration, searchXPATH)
        for element in elements:
            if(element.text == searchText):
                print(element.text)
                return element
    else:
        printError(errorMessage)
        return False