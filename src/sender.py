import os
import requests
from pathlib import Path

class SendMessage:

    def __init__(self, url, data):
        self.url = url
        self.data = data

    def send_to_serverJ(self):
        return requests.post(self.url, self.data)

if __name__ == "__main__":

    serverJ_send_key = os.environ["SERVERJ_SEND_KEY"]
    # Server酱地址
    if serverJ_send_key:
        url = f'https://sctapi.ftqq.com/{serverJ_send_key}.send'

        title = 'Q宠大乐斗脚本执行详情'
        content = Path('./result.txt').read_text()
        content = content.replace('\n', '\n\n')
        data = {
            'title': title,
            'desp': content
        }

        sm = SendMessage(url, data)
        sm.send_to_serverJ()
