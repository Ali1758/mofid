from telegram.telegram import send_message
from users.models import User
from .crawler import crawler_engine
from .models import Storage
from jdatetime import datetime


def crawler():
    user = User.access.all()
    # output_name = "Output {}.xlsx".format(str(datetime.now().date()))
    output_name = "Output {}.xlsx".format(str(datetime.now()).split('.')[-2])
    s = Storage(name=output_name, complete=False)
    s.save()
    crawler_engine.delay(output_name)
    send_message(chat_id=user[0].telegram_id, text="Job Started")
    return None
