# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import shared_task
import numpy as np
import requests
import pandas as pd
import os
from django.conf import settings
from telegram.telegram import send_message, send_file
from users.models import User
from .sites import Darukade, Digikala, Ezdaru, Mofidteb, Mosbatesabz, Shider


# def save2file(name, data, output, summary):
def save2file(name, data, output):
    output_cols = ['کد محصول', 'نام محصول', 'فروشنده', 'وضعیت موجودی', 'قیمت']
    summary_cols = ['کد محصول', 'نام محصول', 'قيمت مفيد', 'وضعيت مفيد', 'ارزانترين فروشگاه', 'قيمت', 'وضعیت', 'لینک']

    out_path = settings.MEDIA_ROOT + os.sep + str(name)
    output_sheet = pd.DataFrame(np.array(output), columns=output_cols)
    # summary_sheet = pd.DataFrame(np.array(summary), columns=summary_cols)
    file = pd.ExcelWriter(out_path)
    data.to_excel(file, 'ورودي')
    output_sheet.to_excel(file, 'خروجي')
    # summary_sheet.to_excel(file, 'گزارش')
    file.save()
    return True


@shared_task
def crawler_engine(output_name):
    data_url = 'https://docs.google.com/spreadsheets/d/12EdKTrZ1pcJ6ce3GID6V-1W7MbafF8AnXBMSr_uoXRw/gviz/tq?tqx=out:csv'
    data = pd.read_csv(data_url)
    data = data[:][:2].dropna(axis='columns', how='all')

    # sites = ["Mofidteb", "Darukade", "Mosbatesabz", "Digikala", "Ezdaru", "Shider"]
    sites = ["mofidteb", "darukade", "mosbatesabz", "digikala", "ezdaru", "shider"]

    def urlcontent(address):
        page = requests.get(address)
        html = page.text
        return str(html)

    def check(item, string):
        if item in str(string):
            return True
        return False

    output = list()
    for row_num in range(data.shape[0]):
        product_code = data.iloc[row_num, 0]
        product_name = data.iloc[row_num, 1]
        # urls = [url for url in filter(lambda x:check('http', str(x)), list(data.iloc[row_num].values))]
        # for url, site in zip(urls, data.columns):
        used_sites = list()
        for url in data.iloc[row_num][4:].values:
            if check('http', url):
                site_name = str(url.split('/')[2].split('.')[-2])
                product = eval('{}()'.format(site_name.capitalize()))
                product.init(urlcontent(url))
                price = product.price()
                available = product.available()
                output.append([product_code, product_name, site_name, available, price])
                used_sites.append(site_name)

        for site in [s for s in sites if s not in used_sites]:
            output.append([product_code, product_name, site, 'عدم تامین', 0])

    # save2file(output_name, data, output, summary)
    save2file(output_name, data, output)

    user = User.access.all()
    send_message(chat_id=user[0].telegram_id, text="Job Done")
    send_file(chat_id=user[0].telegram_id, filename=output_name)

    #     if row_num % 50 == 0:
    #         save2file('backup'+str(int(row_num/50)), data, out, rep)
    # save2file('outputs', data, out, rep)
    return None
