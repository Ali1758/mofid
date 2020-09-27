from bs4 import BeautifulSoup as BS
from unidecode import unidecode
import re
import requests
import random


user_agent_list = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


def urlcontent(address):
    page = requests.get(url=address,
                        headers={
                            'User-Agent': random.choice(user_agent_list)})
    html = page.text
    return str(html)


class Mofidteb:
    def __init__(self, url):
        self.name = 'مفیدطب'
        html = urlcontent(url)
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
        html = urlcontent(url)
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
        html = urlcontent(url)
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
        html = urlcontent(url)
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
        html = urlcontent(url)
        self.content = BS(unidecode(html), 'html.parser')

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
    def __init__(self, url):
        self.name = 'ایزی دارو'
        html = urlcontent(url)
        self.content = BS(unidecode(html), 'html.parser')

    def price(self):
        panel = self.content.find('div', {'class': 'detail-container'})
        q = panel.find('ul', {'class': 'list-unstyled'}).findAll('span')[3].text
        return re.search(r'\d+', re.sub(',', '', q)).group()
    
    def available(self):
        panel = self.content.find('div', {'class': 'detail-container'})
        avail = panel.find('ul', {'class': 'list-unstyled'}).findAll('span')[1].text
        if avail.isnumeric():
            return 'موجود'
        else:
            return 'ناموجود'
