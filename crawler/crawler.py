# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import shared_task
import numpy as np
import requests
import pandas as pd
import os
import time
from django.conf import settings
from telegram.telegram import send_message, send_file
from users.models import User
from .models import Storage
from .sites import Darukade, Digikala, Ezdaru, Mofidteb, Mosbatesabz, Shider


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
    global available, other_url, other_avail, other_store, mofid_avail, mofid_price, other_price, price
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
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'})
        html = page.text
        return str(html)

    def check(item, string):
        if item in str(string):
            return True
        return False

    output = list()
    summary = list()
    for row_num in range(data.shape[0]):
        product_code = data.iloc[row_num, 0]
        product_name = data.iloc[row_num, 1]
        used_sites = list()
        for url in data.iloc[row_num][4:].values:
            if check('http', url):
                site_name = str(url.split('/')[2].split('.')[-2])
                if site_name in sites:
                    product = eval('{}()'.format(site_name.capitalize()))
                    product.init(urlcontent(url))
                    price = product.price()
                    available = product.available()
                    output.append([product_code, product_name, site_name, available, price])

                if site_name == 'mofidteb':
                    mofid_price = price
                    mofid_avail = available

                    other_store = site_name
                    other_price = price
                    other_avail = available
                    other_url = url

                elif site_name != 'mofidteb' and int(other_price) >= int(price) > 0:
                    other_store = site_name
                    other_price = price
                    other_avail = available
                    other_url = url

                used_sites.append(site_name)
                time.sleep(60)

        summary.append([product_code, product_name, mofid_price, mofid_avail,
                        other_store, other_price, other_avail, other_url])

        for site in [s for s in sites if s not in used_sites]:
            output.append([product_code, product_name, site, 'عدم تامین', 0])

        if row_num % 50 == 0:
            save2file('backup' + str(int(row_num / 50)), data, output, summary)

        percent = row_num + 1 / data.shape[0] * 100
        obj.percentage = round(percent, 2)
        obj.save()

    save2file(output_name, data, output, summary)
    obj.percentage = 100.00
    obj.complete = True
    obj.save()

    for user in users:
        send_message(chat_id=user.telegram_id,
                     text='Job done\nYou can download it <a href="{}">from here</a>'.format(obj.download_link()))
    return None
