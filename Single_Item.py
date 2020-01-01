from bs4 import BeautifulSoup
import requests

class Single_Item() :

    def __init__(self, url):
        self.url = url
        
    def getDataFromURL(self):
        response = requests.get(self.url) 
        soup = BeautifulSoup(response.text, 'lxml')
        print('before seller name')
        sellerName = soup.find(class_='unit-seller-link').find('a').get_text()
        print('after seller name')
        

        return {'seller_name': sellerName}
