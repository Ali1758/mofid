from unidecode import unidecode
import re


class Mofidteb:
    def __init__(self):
        self.name = 'مفیدطب'

    def init(self, html):
        self.html = html

    def price(self):
        first = self.html.index('class="price"')
        num = re.findall('[0-9]+,', self.html[first: self.html.index('تومان')])[-1]
        price = self.html[self.html.index(num):].split()[0]
        return re.sub('[a-zA-Z</>,]', '', unidecode(price))

    def available(self):
        blocks = [item.start() for item in re.finditer('class="block-box"', self.html)]
        if self.html[blocks[0]:blocks[1]].count('افزودن به سبد خرید'):
            return 'موجود'
        return 'ناموجود'


class Darukade:
    def __init__(self):
        self.name = 'داروکده'

    def init(self, html):
        self.html = html

    def price(self):
        first = re.search('price-label">', self.html).span()[0]
        last = self.html.index('</div>', first)
        price = re.findall('[0-9]+', re.sub('[a-zA-Z</>,]', '', self.html[first:last]))[0]
        return price

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
        first = re.search('<p class="price"', self.html).span()[0]
        last = self.html.index('</p>', first)
        price = re.findall('[0-9]+', re.sub('[a-zA-Z</>,]', '', self.html[first:last]))[-1]
        return price

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
        except ValueError:
            return 0

    def available(self):
        if self.price():
            return 'موجود'
        return 'ناموجود'


class Shider:
    def __init__(self):
        self.name = 'شیدر'

    def init(self, html):
        self.html = html

    def price(self):
        st = self.html.index('قیمت:')
        sub = self.html[st: self.html.index('ریال', st)]
        return int(int(re.sub('[a-zA-Z</>,:=" -]', '', unidecode(sub))) / 10)

    def available(self):
        if self.html.count('ناموجود'):
            return 'ناموجود'
        return 'موجود'


class Ezdaru:
    def __init__(self):
        self.name = 'ایزی دارو'

    def init(self, html):
        self.html = html

    def price(self):
        html = self.html
        sub = html[html.index('class="price"'):html.index('class="product-buttons-wrap clearfix"')]
        return min(re.findall('[0-9]+', re.sub('[,]', '', sub)))

    def available(self):
        if self.html.count('ناموجود'):
            return 'ناموجود'
        return 'موجود'
