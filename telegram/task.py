from __future__ import absolute_import
from celery import shared_task
from .telegram import send_message


@shared_task  # Use this decorator to make this a asyncronous function
def generate_report(chat_id, text):
    send_message(65908245, "OK. It's work.")
