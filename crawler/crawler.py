# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import shared_task
import numpy as np
import requests
import pandas as pd
import os
import time
import random
import re
from django.conf import settings
from telegram.telegram import send_message
from users.models import User
from .models import Storage, Backup
from .sites import Darukade, Digikala, Ezdaroo, Mofidteb, Mosbatesabz, Shiderstore

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


def save2file(name, data, output, summary):
    output_cols = ['کد محصول', 'نام محصول', 'فروشنده', 'وضعیت موجودی', 'قیمت']
    summary_cols = ['کد محصول', 'نام محصول', 'قيمت مفيد', 'وضعيت مفيد', 'ارزانترين فروشگاه', 'قيمت', 'وضعیت', 'لینک']

    out_path = settings.MEDIA_ROOT + os.sep + str(name) + ".xlsx"
    output_sheet = pd.DataFrame(np.array(output), columns=output_cols)
    summary_sheet = pd.DataFrame(np.array(summary), columns=summary_cols)
    file = pd.ExcelWriter(out_path)
    data.to_excel(file, 'ورودي')
    output_sheet.to_excel(file, 'خروجي')
    summary_sheet.to_excel(file, 'گزارش')
    file.save()
    return True


@shared_task
def crawler_engine(output_name, sites, users):
    # global available, other_url, other_avail, other_store, mofid_avail, mofid_price, other_price, price
    users = User.access.filter(username__in=users)
    for user in users:
        send_message(chat_id=user.telegram_id, text="Job Started")
    data_url = 'https://docs.google.com/spreadsheets/d/12EdKTrZ1pcJ6ce3GID6V-1W7MbafF8AnXBMSr_uoXRw/gviz/tq?tqx=out:csv'
    data = pd.read_csv(data_url)
    data = data.dropna(axis='columns', how='all')

    obj = Storage.objects.get(name=output_name)

    def urlcontent(address):
        page = requests.get(url=address,
                            headers={
                                'User-Agent': random.choice(user_agent_list)})
        html = page.text
        return str(html)

    output = list()
    summary = list()
    for row_num in range(data.shape[0]):
        product_code = data.iloc[row_num, 0]
        product_name = data.iloc[row_num, 1]
        used_sites = list()
        for url in data.iloc[row_num][4:].values:
            try:
                link, site = re.search(r'(https?://(\S+).\w+)', url).groups()
            except (AttributeError, TypeError):
                continue
            
            if site in sites:
                product = eval('{}()'.format(site.capitalize()))
                product.init(urlcontent(link))
                price = product.price()
                if price:
                    available = product.available()
                else:
                    available = "ناموجود"
                output.append([product_code, product_name, site, available, price])

                if site == 'mofidteb':
                    mofid_price = price
                    mofid_avail = available

                    other_store = site
                    other_price = price
                    other_avail = available
                    other_url = link

                elif site != 'mofidteb' and int(other_price) > int(price) > 0:
                    other_store = site
                    other_price = price
                    other_avail = available
                    other_url = link

            used_sites.append(site)

        summary.append([product_code, product_name, mofid_price, mofid_avail,
                        other_store, other_price, other_avail, other_url])

        for site in [s for s in sites if s not in used_sites]:
            output.append([product_code, product_name, site, 'عدم تامین', 0])

        percent = (row_num + 1) / data.shape[0] * 100
        obj.percentage = round(percent, 2)
        obj.save()

        if row_num % 200 == 0 and row_num != 0:
            backup_name = output_name + '_backup_' + str(int((row_num + 1) / 200))
            save2file(backup_name, data[:][:row_num], output, summary)
            Backup.create(name=backup_name, parent=obj, address=backup_name + ".xlsx")
            time.sleep(300)

    save2file(output_name, data, output, summary)
    obj.percentage = 100.00
    obj.complete = True
    obj.save()

    for user in users:
        send_message(chat_id=user.telegram_id,
                     text='Job done\nYou can download it from <a href="85.185.93.78:88{}">here</a>'.format(
                         obj.download_link()))
    return None
