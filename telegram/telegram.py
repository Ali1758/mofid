from django.conf import settings
import requests


def send_message(chat_id, text):
    TOKEN = '724028938:AAHybbVdMsuMglarLSHcPu6MOBHXnXcCdkY'
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    # requests.post("http://nameghi.ir/telegram/bot{token}/sendMessage".format(token=TOKEN), data=payload)
    requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TOKEN), data=payload)


def send_file(chat_id, filename):
    TOKEN = '724028938:AAHybbVdMsuMglarLSHcPu6MOBHXnXcCdkY'
    payload = {'chat_id': chat_id, 'parse_mode': 'HTML'}
    f = open(settings.MEDIA_ROOT + str(filename), 'rb')
    files = {'document': f}
    requests.post("http://nameghi.ir/telegram/bot{token}/sendDocument".format(token=TOKEN), files=files, data=payload)
    f.close()
