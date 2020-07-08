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
    def __init__(self):
        self.name = 'داروکده'

    def init(self, html):
        self.html = html

    def price(self):
        try:
            # first = re.search('price-label">', self.html).span()[0]
            first = self.html.index('price-label">')
            last = self.html.index('</div>', first)
            price = re.findall('[0-9]+', re.sub('[a-zA-Z</>,]', '', self.html[first:last]))[0]
            return price
        except:
            return 0

    def available(self):
        if '<div class="product-img unavailable-product">' in self.html:
            return 'ناموجود'
        return 'موجود'


class Mosbatesabz:
    def __init__(self):
        self.name = 'مثبت سبز'

    def init(self, html):
        self.html = unidecode(html)

    def price(self):
        try:
            first = re.search('<p class="price"', self.html).span()[0]
            last = self.html.index('</p>', first)
            price = re.findall('[0-9]+', re.sub('[a-zA-Z</>,]', '', self.html[first:last]))[-1]
            return price
        except:
            return 0

    def available(self):
        first = re.search('info_box', self.html).span()[0]
        last = self.html.index('</div>', first)
        text = self.html[first:last]
        if 'موجود در انبار' in text:
            return 'موجود'
        return 'ناموجود'


class Digikala:
    def __init__(self):
        self.name = 'دیجیکالا'

    def init(self, html):
        self.html = html

    def price(self):
        try:
            first = self.html.index('<div class="c-product__seller-price-raw js-price-value"')
            last = self.html.index('</div>', first)
            price = re.findall('[0-9]+', unidecode(re.sub(',', '', self.html[first: last])))[-1]
            return price
        except:
            return 0

    def available(self):
        if self.price():
            return 'موجود'
        return 'ناموجود'


class Shiderstore:
    def __init__(self):
        self.name = 'شیدر'

    def init(self, html):
        self.html = html

    def price(self):
        try:
            st = self.html.index('قیمت:')
            sub = self.html[st: self.html.index('ریال', st)]
            return int(int(re.sub('[a-zA-Z</>,:=" -]', '', unidecode(sub))) / 10)
        except:
            return 0

    def available(self):
        if self.html.count('ناموجود'):
            return 'ناموجود'
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
