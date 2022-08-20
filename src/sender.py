import os
import requests
from requests.adapters import HTTPAdapter, Retry
from pathlib import Path

class SendMessage:

    def __init__(self, content):
        self.content = content
        self.session = requests.Session()
        retries = Retry(total = 3, backoff_factor = 0.3, status_forcelist = [500, 502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    # server酱推送
    def send_to_serverJ(self):
        serverJ_send_key = os.environ["SERVERJ_SEND_KEY"]
        if serverJ_send_key:
            url = f'https://sctapi.ftqq.com/{serverJ_send_key}.send'
            desp = self.content.replace('\n', '\n\n')
            data = {
                'title': 'Q宠大乐斗脚本执行详情',
                'desp': desp
            }
            return self.session.post(url, data)

    # telegram 消息推送
    def send_to_telegram(self):
        telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
        telegram_chat_id = os.environ["TELEGRAM_CHAT_ID"]
        if all([telegram_bot_token, telegram_chat_id]):
            url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
            data = {
                'chat_id': telegram_chat_id,
                'text': self.content
            }
            return self.session.post(url, data)

if __name__ == "__main__":
    content = Path('./result.txt').read_text()
    sm = SendMessage(content)
    sm.send_to_serverJ()
    sm.send_to_telegram()
        