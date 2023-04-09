import time
from urllib.parse import urlencode

def take_stroll(base_url, get_content):
    params_list = [
        {
            "name": "华藏寺",
            "zapp_uin": "",
            "sid": "",
            "channel": 0,
            "g_ut": 1,
            "cmd": "sect_art"
        }, {
            "name": "伏虎寺",
            "zapp_uin": "",
            "sid": "",
            "channel": 0,
            "g_ut": 1,
            "cmd": "sect_trump"
        }, {
            "name": "帮战",
            "zapp_uin": "",
            "B_UID": "0",
            "sid": "",
            "channel": 0,
            "g_ut": 1,
            "sub": 0,
            "id": 5,
            "cmd": "facwar",
        }, {
            "name": "贡献度",
            "zapp_uin": "",
            "sid": "0",
            "channel": 0,
            "g_ut": 1,
            "cmd": "factionhr",
            "subtype": 14,
        }, {
            "name": "要闻",
            "zapp_uin": "",
            "sid": "0",
            "channel": 0,
            "g_ut": 1,
            "cmd": "factionop",
            "subtype": 8,
            "pageno": 1,
            "type": 2
        }, {
            "name": "帮修",
            "zapp_uin": "",
            "sid": "0",
            "channel": 0,
            "g_ut": 1,
            "cmd": "factiontrain",
            "type": 1
        }, {
            "name": "贡献药水",
            "zapp_uin": "",
            "sid": "",
            "channel": 0,
            "g_ut": 1,
            "cmd": "use",
            "id": "3038",
            "store_type": "0",
            "page": "1"
        }
    ]
    for item in params_list:
        print(item["name"])
        del item["name"]
        get_content(base_url + urlencode(item))
        time.sleep(0.5)
