from bs4 import BeautifulSoup
import requests
from Seller import Seller
from OthrItem import OthrItem
from openpyxl import Workbook
from openpyxl.styles import Font, Color, Alignment, Border, Side, colors, NamedStyle, PatternFill
import time
import os



class Project(Seller, OthrItem) :

    #empty  list
    __items_list = []
    #Get Unixsttamp
    unix_dt = int(time.time())

    wb = Workbook()
    sh = wb.active

    def __init__(self, item_search):
        self.item_search = item_search

        #start work get html
        self.main_function()
    
    def __get_target_url(self):
        target_url = "https://egypt.souq.com/eg-ar/"+self.item_search+"/s"
        return target_url

    def get_seller_name(self, url) :
        
        seller = Seller(url)
        selller_name = seller.getDataFromURL()
        return selller_name

    def get_othr_price_of_item(self, url) :
        priceItem = OthrItem(url)
        price = priceItem.getDataFromURL()
        return price

    def setup_excel(self) :
        #setup excel
        
        self.sh.sheet_view.rightToLeft=True
        self.sh.title = "Report"
        self.wb.create_sheet(title="items")
        self.sh.sheet_properties.tabColor = "1072BA"

        # Let's create a style template for the header row
        # header_line1 = NamedStyle(name="header")
        # header_line1.font = Font(bold=True)
        # header_line1.border = Border(bottom=Side(border_style="thin"))
        # header_line1.alignment = Alignment(horizontal="center", vertical="center")

        # pattern fill for cell
        # redFill = PatternFill(start_color='FFFF0000',
        #                 end_color='FFFF0000',
        #                 fill_type='solid')

        headers = ['اسم المنتج','link-href',  'سعر المنتج', 'السعر المنافس', 'اسم البائع','صورة المنتج']


        c = 1
        for i in headers:
            self.sh.cell(row=1, column=c).value = i
            c += 1

        # Now let's apply this to all first row (header) cells
        # header_row = self.sh[1]
        # for cell in header_row:
        #     cell.style = header_line1

        return

    def main_function(self) :
        target_url = self.__get_target_url()
        response = requests.get(target_url)
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all(class_="single-item")

        #call setup excel
        self.setup_excel()
        r=2
        i=1
        for item in items:
            item_img = item.find('img',  {'class': 'img-size-medium'}).attrs.get("data-src")
            
            item_title = item.find(class_='itemTitle')
            item_price = item.find(class_='itemPrice')
            url_item = item.find(class_="quickViewAction")['href']
            new_url = url_item.replace(url_item[-2], 'io')
            priceItem = self.get_othr_price_of_item(new_url)
            seller_of_item_name = self.get_seller_name(url_item)

            if item_title is not None :
                _item_title = item_title.get_text()
            if item_price is not None :
                _item_price = item_price.get_text()
            list = [_item_title,url_item, _item_price, priceItem,  seller_of_item_name, item_img]
            
            
            
            for lst1 in list :
                if i > len(list) :
                    i = 1

                self.sh.cell(row=r, column=i).value = lst1
                i += 1
            r += 1

        self.save_file_excel()


    def save_file_excel(self) :

        filename = 'Report-'+str(self.unix_dt)+'.xlsx'
        home_path = os.path.join(os.environ['HOMEPATH'], 'Desktop')
        #Saving File
        self.wb.save(os.path.join(home_path, filename))









































