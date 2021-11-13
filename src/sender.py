import os
import requests
from pathlib import Path

class SendMessage:

    def __init__(self, url, data):
        self.url = url
        self.data = data

    def send_to_serverJ(self):
        return requests.post(self.url, self.data)

    def send_to_telegram(self):
        return requests.post(self.url, self.data)

if __name__ == "__main__":

    # server酱 send key
    serverJ_send_key = os.environ["SERVERJ_SEND_KEY"]

    # telegram bot token 和 chat id
    telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    telegram_chat_id = os.environ["TELEGRAM_CHAT_ID"]

    content = Path('./result.txt').read_text()
    content = content.replace('\n', '\n\n')

    # Server酱
    if serverJ_send_key:
        url = f'https://sctapi.ftqq.com/{serverJ_send_key}.send'
        title = 'Q宠大乐斗脚本执行详情'
        data = {
            'title': title,
            'desp': content
        }
        sm = SendMessage(url, data)
        sm.send_to_serverJ()

    if telegram_bot_token and telegram_chat_id:
        url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
        data = {
            'chat_id': telegram_chat_id,
            'text': content,
            'parse_mode': 'MarkdownV2'
        }
        sm = SendMessage(url, data)
        sm.send_to_telegram()