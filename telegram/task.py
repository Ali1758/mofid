from __future__ import absolute_import
from celery import shared_task
from .telegram import send_message
import time


@shared_task  # Use this decorator to make this a asyncronous function
def generate_report(chat_id=65908245, text="OK. It's work."):
    time.sleep(120)
    send_message(chat_id=chat_id, text=text)
