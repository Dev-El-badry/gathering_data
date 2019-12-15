from bs4 import BeautifulSoup
import requests
class OthrItem() :
    def __init__(self, url):
            self.url = url
        
    def getDataFromURL(self):
        response = requests.get(self.url) 
        soup = BeautifulSoup(response.text, 'lxml')
        price_item = soup.find(class_='price-field').get_text()
        return price_item
    def getUserName(self) :
        response = requests.get(self.url) 
        soup = BeautifulSoup(response.text, 'lxml')
        sellerName = soup.find(class_='seller-name').find('a').get_text()
        return sellerName