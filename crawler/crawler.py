# -*- coding: utf-8 -*-
import numpy as np
import requests
import pandas as pd
import re
import os
import time
from unidecode import unidecode
from django.conf import settings


def crawler():
    print('============= start: ' + time.ctime() + ' =============')

    URL = 'https://docs.google.com/spreadsheets/d/12EdKTrZ1pcJ6ce3GID6V-1W7MbafF8AnXBMSr_uoXRw/gviz/tq?tqx=out:csv'
    data = pd.read_csv(URL)

    numbers = data.count()[0]
    sites = data.columns[4:10]
    code = data.columns[0]
    name = data.columns[1]

    def ch(url):
        page = requests.get(url)
        html = page.text
        return html

    class Mofidteb:
        def __init__(self, html):
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
        def __init__(self, html):
            self.html = html

        def price(self):
            text = self.html.index('productcost')
            price = re.findall('[0-9]+', self.html[text:].split()[0])[0]
            return re.sub('[a-zA-Z</>,]', '', price)

        def available(self):
            first = self.html.index('DefaultDiv257')
            last = self.html.index('DefaultDiv316')
            text = self.html[first:last]
            if 'موجود نیست' in text:
                return 'ناموجود'
            return 'موجود'

    class Mosbatesabz:
        def __init__(self, html):
            self.html = html

        def price(self):
            text = re.search('itemprop="price"', self.html).span()[0]
            price = re.findall('[0-9]+', self.html[text:])[0]
            return price

        def available(self):
            if self.html.count('اتمام موجودی'):
                return 'ناموجود'
            return 'موجود'

    class Digikala:
        def __init__(self, html):
            self.html = html

        def price(self):
            try:
                first = self.html.index('class="js-price-value"')
                price = self.html[first + 24: first + self.html[first:].index('</span>')]
                return re.sub(',', '', unidecode(price))
            except:
                return 0

        def available(self):
            if self.html.count('class="c-product__attributes js-product-attributes"'):
                return 'موجود'
            return 'ناموجود'

    class Shider:
        def __init__(self, html):
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
        def __init__(self, html):
            self.html = html

        def price(self):
            html = self.html
            sub = html[html.index('class="price"'):html.index('class="product-buttons-wrap clearfix"')]
            return min(re.findall('[0-9]+', re.sub('[,]', '', sub)))

        def available(self):
            if self.html.count('ناموجود'):
                return 'ناموجود'
            return 'موجود'

    # =============================================================

    def cs(site, html):
        return {
            'مفیدطب': Mofidteb(html),
            'شیدر': Shider(html),
            'داروکده': Darukade(html),
            'مثبت سبز': Mosbatesabz(html),
            'دیجیکالا': Digikala(html),
            'ایزی دارو': Ezdaru(html)
        }[site]

    out = []
    rep = []

    for num in range(numbers):
        ss = []
        avail = []
        for site in sites:
            address = data[site][num]
            i = site[site.index('در') + 3:]
            try:
                re.match("^http", address)
                dd = ch(address)
                z = cs(i, dd)
                out.append([str(data[code][num]), data[name][num], i, z.available(), int(z.price())])
                if i == 'مفیدطب':
                    rep.append([str(data[code][num]), data[name][num], int(z.price()), z.available(), '', 0, '', ''])
                elif int(z.price()) > 0:
                    ss.append([i, int(z.price()), z.available(), address])
                    if z.available() == 'موجود':
                        avail.append([i, int(z.price()), z.available(), address])

            except:
                out.append([data[code][num], data[name][num], i, 'عدم تامین', 0])
        try:
            if avail:
                rep[-1][-4:] = min(avail, key=lambda x: x[1])
            else:
                rep[-1][-4:] = min(ss, key=lambda x: x[1])
            time.sleep(20)
        except:
            print('error in report at line{0}'.format(str(num)))
            rep[-1][-4:] = ['', '', '', '']

        if num % 50 == 0:
            out_path = settings.MEDIA_ROOT + '/' + 'backup.xlsx'
            if out_path in os.listdir():
                os.remove(out_path)
            output = pd.DataFrame(np.array(out), columns=['کد محصول', 'نام محصول', 'فروشنده', 'وضعیت موجودی', 'قیمت'])
            summary = pd.DataFrame(np.array(rep),
                                   columns=['کد محصول', 'نام محصول', 'قيمت مفيد', 'وضعيت مفيد', 'ارزانترين فروشگاه',
                                            'قيمت', 'وضعیت', 'لینک'])
            file = pd.ExcelWriter(out_path)
            data.to_excel(file, 'ورودي')
            output.to_excel(file, 'خروجي')
            summary.to_excel(file, 'گزارش')
            file.save()

    out_path = settings.MEDIA_ROOT + '/' + 'outputs.xlsx'
    output = pd.DataFrame(np.array(out), columns=['کد محصول', 'نام محصول', 'فروشنده', 'وضعیت موجودی', 'قیمت'])
    summary = pd.DataFrame(np.array(rep),
                           columns=['کد محصول', 'نام محصول', 'قيمت مفيد', 'وضعيت مفيد', 'ارزانترين فروشگاه', 'قيمت',
                                    'وضعیت', 'لینک'])
    file = pd.ExcelWriter(out_path)
    data.to_excel(file, 'ورودي')
    output.to_excel(file, 'خروجي')
    summary.to_excel(file, 'گزارش')
    file.save()

    return None
