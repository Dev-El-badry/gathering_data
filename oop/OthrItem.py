from bs4 import BeautifulSoup
import requests
class OthrItem() :
    empty_lst = []
    #_data_seller = {};
    def __init__(self, url, seller_name_searched):
            self.url = url
            self.seller_name_searched = seller_name_searched
    
    def get_data_belong_to_seller_name(self) :
        #DECLRATION SOME VARS
        _seller_name = ''
        _offer_price = 0

        #Start GET DATA
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'lxml')

        # GET DATA MATCHED WITH SELLER NAME
        soup = BeautifulSoup(response.text, 'lxml')
        sellers_name = soup.find_all(class_='seller-name')
        price_item = soup.find(class_='price-field')
        for seller_name in sellers_name :
            
            if seller_name.find('a').get_text() == self.seller_name_searched:
                _seller_name = seller_name.get_text().strip()
                _offer_price = price_item.get_text().strip()
                break
            else :
                _seller_name = ''

        return  {
            'seller_name': _seller_name,
            'offer_price': _offer_price
        }
        # price_items = soup.find_all(class_='price-field')
        # for single_price_item in price_items :
