from SEWebScraping import SEWebScrap

seWeb = SEWebScrap()
if(seWeb.logIntoSE()):
    print('Logged in')
    list = ['000375303']
    for id in list:
        print('searching ' + id + ' ----------')
        seWeb.searchID(id)
        seWeb.extractDetails()
    
