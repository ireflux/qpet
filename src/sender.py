import os
import requests
from pathlib import Path

class SendMessage:

    def __init__(self, content):
        self.content = content

    # server酱推送
    def send_to_serverJ(self):
        serverJ_send_key = os.environ["SERVERJ_SEND_KEY"]
        if serverJ_send_key:
            url = f'https://sctapi.ftqq.com/{serverJ_send_key}.send'
            title = 'Q宠大乐斗脚本执行详情'
            data = {
                'title': title,
                'desp': self.content
            }
            return requests.post(url, data)

    # telegram 消息推送
    def send_to_telegram(self):
        telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
        telegram_chat_id = os.environ["TELEGRAM_CHAT_ID"]
        if all([telegram_bot_token, telegram_chat_id]):
            url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
            data = {
                'chat_id': telegram_chat_id,
                'text': self.content,
                'parse_mode': 'MarkdownV2'
            }
            return requests.post(url, data)

if __name__ == "__main__":
    content = Path('./result.txt').read_text()
    content = content.replace('\n', '\n\n')
        
    sm = SendMessage(content)
    sm.send_to_serverJ()
    sm.send_to_telegram()
        