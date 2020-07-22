from bs4 import BeautifulSoup as BS
from unidecode import unidecode
import re
import requests


class Mofidteb:
    def __init__(self, url):
        self.name = 'مفیدطب'
        html = requests.get(url).text
        self.content = BS(html, 'html.parser')

    def price(self):
        price = self.content.find('div', {'class': 'price'})
        try:
            return re.search(r'(\d+)', re.sub(',', '', str(price.find('span', {'class': 'text-discount'})))).group()
        except:
            return re.search(r'(\d+)', re.sub(',', '', str(price))).group()

    def available(self):
        avail = self.content.find('div', {'class': 'product-share'})
        ban = avail.find('i', {'class': 'fa-ban'})
        if ban:
            return 'ناموجود'
        return 'موجود'


class Darukade:
    def __init__(self, url):
        self.name = 'داروکده'
        html = requests.get(url).text
        self.content = BS(html, 'html.parser')

    def price(self):
        try:    
            return re.search(r'(\d+)', re.sub(',', '', str(self.content.find('div', {'class': 'off-price-label'}).find('i')))).group()
        except:
            return re.search(r'(\d+)', re.sub(',', '', str(self.content.find('div', {'class': 'price-label'}).find('i')))).group()

    def available(self):
        avail = self.content.find('div', {'class': 'product-price-layer'})
        ban = avail.find('button', {'class': 'notice-me'})
        if ban:
            return 'ناموجود'
        else:
            return 'موجود'



class Mosbatesabz:
    def __init__(self, url):
        self.name = 'مثبت سبز'
        html = requests.get(url).text
        self.content = BS(unidecode(html), 'html.parser')

    def price(self):
        price = self.content.find('p', {'class': 'price'})
        try:
            return re.search(r'(\d+)', re.sub(',', '', str(price.find('ins').text))).group()
        except:
            return re.search(r'(\d+)', re.sub(',', '', str(price.find('span', {'class': 'amount'}).text))).group()


    def available(self):
        avail = self.content.find('div', {'class': 'info_box'})
        ban = avail.find('i', {'class': 'fa-times-circle'})
        if ban:
            return 'ناموجود'
        else:
            return 'موجود'


class Digikala:
    def __init__(self, url):
        self.name = 'دیجیکالا'
        html = requests.get(url).text
        self.content = BS(unidecode(html), 'html.parser')

    def price(self):
        panel = self.content.find('div', {'class': 'c-product__summary'})
        try:
            return re.sub(',', '', str(panel.find('div', {'class': 'c-product__seller-price-raw'}).text.split()[0]))
        except:
            return 0

    def available(self):
        if self.price():
            return 'موجود'
        return 'ناموجود'


class Shiderstore:
    def __init__(self, url):
        self.name = 'شیدر'
        html = requests.get(url).text
        self.content = BS(unidecode(html), 'html.parser')

    def init(self, html):
        self.html = html

    def price(self):
        panel = self.content.find('fieldset', {'class': 'group-head'})
        c = panel.find('input', {'id': 'edit-submit'}).has_attr('disabled')
        if not c:
            return int(int(re.search(r'\d+', str(re.sub(',', '', str(panel.find('tr', {'class': 'commerce-price-savings-formatter-price'}).text)))).group())/10)
        else:
            return 0

    def available(self):
        panel = self.content.find('fieldset', {'class': 'group-head'})
        ban = panel.find('input', {'id': 'edit-submit'}).has_attr('disabled')
        if ban:
            return 'ناموجود'
        else:
            return 'موجود'


class Ezdaroo:
    def __init__(self):
        self.name = 'ایزی دارو'

    def init(self, html):
        self.html = html

    def price(self):
        try:
            html = self.html
            sub = html[html.index('class="price"'):html.index('class="product-buttons-wrap clearfix"')]
            return min(re.findall('[0-9]+', re.sub('[,]', '', sub)))
        except:
            return 0

    def available(self):
        if self.html.count('ناموجود'):
            return 'ناموجود'
        return 'موجود'
