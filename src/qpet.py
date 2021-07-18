import requests
from urllib.parse import urlencode
from lxml import etree
from datetime import date

class qpet:

    def __init__(self, base_url, protocol, headers, proxies, pattern_1) -> None:
        self.protocol = protocol
        self.headers = headers
        self.proxies = proxies
        self.base_url = base_url
        self.pattern_1 = pattern_1

    def get_content(self, url):
        try:
            resp = requests.get(url, proxies = self.proxies, headers = self.headers)
            if 200 == resp.status_code:
                return resp.content
        except requests.ConnectionError:
            return None

    def content_parser(self, url, pattern):
        content = self.get_content(url)
        return etree.HTML(content).xpath(pattern)

    def main(self) -> None:
        # 获取星期(一到日 -> 0到6)
        weekday = date.today().weekday()

        # 领取徒弟经验
        print('----------领取徒弟经验----------')
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'exp'
        }
        url = self.base_url + urlencode(params)
        result = self.content_parser(url, self.pattern_1)
        print([item for item in result if '领取' in item])

        # 每日奖励
        print('----------每日奖励----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'dailygift',
            'op': 'draw',
            'key': 'meridian'
        }
        key_list = ['meridian', 'login']
        for item in key_list:
            params['key'] = item
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

        # 邪神秘宝
        print('----------邪神秘宝----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'tenlottery',
            'op': 2,
            'type': 0
        }
        for item in range(2):
            params['type'] = item
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

        # 武林大会
        print('----------武林大会----------')
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'fastSignWulin'
            # 'ifFirstSign': 1
        }
        url = self.base_url + urlencode(params)
        result = self.content_parser(url, self.pattern_1)
        print(result[1]) if len(result) > 1 else print(result)

        # 武林盟主
        print('----------武林盟主----------')
        signup_time = [0, 2, 4]
        if weekday in signup_time:
            params = {
                'channel': 0,
                'g_ut': 1,
                'cmd': 'wlmz',
                'op': 'signup',
                'ground_id': 2
            }
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)
        else:
            print('仅周一、周三、周五可报名')

        # 巅峰之战
        print('----------巅峰之战----------')
        if weekday > 1:
            params = {
                'channel': 0,
                'g_ut': 1,
                'cmd': 'gvg',
                'sub': 5,
                'group': 0,
                'check': 1
            }
            url = self.base_url + urlencode(params)
            for i in range(3):
                result = self.content_parser(url, self.pattern_1)
                print(result[2]) if len(result) > 2 else print(result)
        else:
            # 随机加入 南/北 派
            params['sub'] = 4
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

            # 领取奖励
            params['sub'] = 1
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

        # 历练
        print('----------历练----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'mappush',
            'subtype': 2,
            'mapid': 20,
            'pageid': 2
        }
        url = self.base_url + urlencode(params)
        area_list = self.content_parser(url, '//div[@id="id"]/a[contains(@href, "npcid")]/@href')
        if area_list:
            url = self.protocol + area_list[-1]
            for item in range(3):
                result = self.content_parser(url, self.pattern_1)
                print(result[3]) if len(result) > 3 else print(result)
            url = self.protocol + area_list[-2]
            for item in range(2):
                result = self.content_parser(url, self.pattern_1)
                print(result[3]) if len(result) > 3 else print(result)

        # 好友对战
        print('----------好友对战----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'viewxialv',
            'type': 1
        }
        cmd_list = ['viewxialv', 'friendlist', 'viewmem']
        pattern = '//div[@id="id"]/a[contains(@href, "cmd=fight")]/@href'
        for item in cmd_list:
            params['cmd'] = item
            url = self.base_url + urlencode(params)
            if item == 'viewmem':
                pattern = '//div[@id="id"]/a[contains(@href, "cmd=fight")][position()<5]/@href'
            else:
                pattern = '//div[@id="id"]/a[contains(@href, "cmd=fight")]/@href'
            friend_list = self.content_parser(url, pattern)
            for i in friend_list:
                result = self.content_parser(self.protocol + i, self.pattern_1)
                if item == 'viewmem':
                    print(result[2]) if len(result) > 2 else print(result)
                else:
                    print(result[3]) if len(result) > 3 else print(result)
                if '体力值不足' in str(result):
                    break

        # 侠士客栈
        print('----------侠士客栈----------')
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'warriorinn'
        }
        url = self.base_url + urlencode(params)
        reward_list = self.content_parser(url, '//div[@id="id"]/a[contains(@href, "op=getlobbyreward")]/@href')
        for item in reward_list:
            result = self.content_parser(self.protocol + item, self.pattern_1)
            print(result[2]) if len(result) > 2 else print(result)

        # 问鼎天下
        print('----------问鼎天下----------')
        if weekday < 5:
            params = {
                'B_UID': 0,
                'channel': 0,
                'g_ut': 1,
                'cmd': 'tbattle'
            }
            url = self.base_url + urlencode(params)
            area_list = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "op=occupy")][last()]/@href')
            if area_list:
                for i in range(5):
                    result = self.content_parser(self.protocol + area_list[0], self.pattern_1)
                    print(result[1]) if len(result) > 1 else print(result)
                    if '只能占领一个领地' in str(result):
                        break
        # 问鼎天下-领取奖励
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'tbattle',
            'op': 'drawreward'
        }
        url = self.base_url + urlencode(params)
        result = self.content_parser(url, self.pattern_1)
        print(result[1]) if len(result) > 1 else print(result)

        # 梦想之旅
        print('----------梦想之旅----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'dreamtrip',
            'sub': 2
        }
        url = self.base_url + urlencode(params)
        result = self.content_parser(url, self.pattern_1)
        print(result[1]) if len(result) > 1 else print(result)

        # 帮派黄金联赛
        print('----------帮派黄金联赛----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'factionleague',
            'op': 5
        }
        url = self.base_url + urlencode(params)
        result = self.content_parser(url, self.pattern_1)
        print(result[0]) if len(result) > 0 else print(result)

        # 会武
        print('----------会武----------')
        if weekday > 4:
            params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'sectmelee',
            'op': 'drawreward'
            }
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

        # 门派邀请赛
        print('----------门派邀请赛----------')
        params = {
                'channel': 0,
                'g_ut': 1,
                'cmd': 'secttournament',
                'op': 'fight'
        }
        if weekday > 1:
            url = self.base_url + urlencode(params)
            for i in range(5):
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)
        else:
            params['op'] = 'signup'
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

        # 门派
        print('----------门派----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'sect',
            'op': 'fumigatefreeincense'
        }
        op_list = ['fumigatefreeincense', 'trainingwithnpc', 'trainingwithmember', 'showcouncil']
        for item in op_list:
            params['op'] = item
            url = self.base_url + urlencode(params)
            if item == 'showcouncil':
                enemy_list = self.content_parser(url, '//div[@id="id"]/p/a/@href')
                for enemy in enemy_list:
                    result = self.content_parser(self.protocol + enemy, self.pattern_1)
                    print(result[1]) if len(result) > 1 else print(result)
            else:
                result = self.content_parser(url, self.pattern_1)
                if item == 'fumigatefreeincense':
                    print(result[2]) if len(result) > 2 else print(result)
                else:
                    print(result[1]) if len(result) > 1 else print(result)

        params['cmd'] = 'sect_task'
        url = self.base_url + urlencode(params)
        reward_list = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "subtype=2")]/@href')
        for item in reward_list:
            result = self.content_parser(self.protocol + item, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

        # 群雄逐鹿
        print('----------群雄逐鹿----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'thronesbattle',
            'op': 'signup'
        }
        op_list = ['signup', 'drawreward']
        for item in op_list:
            params['op'] = item
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[2]) if len(result) > 2 else print(result)

        # 幻境
        print('----------幻境----------')
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'misty',
            'stage_id': 8,
            'box_id': 2,
            'op': 'fight'
        }
        op_list = ['return', 'start', 'fight', 'reward']
        for item in op_list:
            params['op'] = item
            if 'fight' == item:
                url = self.base_url + urlencode(params)
                for i in range(5):
                    result = self.content_parser(url, self.pattern_1)
                    print(result[3]) if len(result) > 3 else print(result)
            else:
                url = self.base_url + urlencode(params)
                result = self.content_parser(url, self.pattern_1)
                print(result[3]) if len(result) > 3 else print(result)

        # 斗神塔
        print('----------斗神塔----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'towerfight',
            'type': 7,
            'confirm': 1
        }
        type_list = [7,1]
        for item in type_list:
            params['type'] = item
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

        # 抢地盘
        print('----------抢地盘----------')
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'recommendmanor',
            'type': 6,
            'page': 1
        }
        url = self.base_url + urlencode(params)
        enemy_list = self.content_parser(url, '//div[@id="id"]/a[contains(@href, "cmd=manorfight")]/@href')
        if len(enemy_list) > 0:
            result = self.content_parser(self.protocol + enemy_list[0], self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

        # 画卷谜踪
        print('----------画卷谜踪----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'scroll_dungeon',
            'op': 'fight',
            'buff': 0
        }
        url = self.base_url + urlencode(params)
        for i in range(10):
            result = self.content_parser(url, self.pattern_1)
            print(result[9]) if len(result) > 9 else print(result)
            if '弱爆了' in str(result):
                break

        # 十二宫
        print('----------十二宫----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'zodiacdungeon',
            'op': 'autofight',
            'scene_id': 1011,
            'pay_recover_times': 0
        }
        url = self.base_url + urlencode(params)
        result = self.content_parser(url, self.pattern_1)
        print(result)

        # 镖行天下
        print('----------镖行天下----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'cargo',
            'op': 16
        }
        op_list = [16, 8, 6, 3]
        for item in op_list:
            params['op'] = item
            url = self.base_url + urlencode(params)
            if item == 3:
                enemy_list = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "op=14")][position()<4]/@href')
                for item in enemy_list:
                    result = self.content_parser(self.protocol + item, self.pattern_1)
                    print(result[1]) if len(result) > 1 else print(result)
            else:
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)


        # 竞技场
        print('----------竞技场----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'arena',
            'op': 'challenge'
        }
        op_list = ['challenge', 'drawdaily']
        for item in op_list:
            params['op'] = item
            url = self.base_url + urlencode(params)
            if item == 'challenge':
                for i in range(5):
                    result = self.content_parser(url, self.pattern_1)
                    print(result[1]) if len(result) > 1 else print(result)
            else:
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)

        # 踢馆
        print('----------踢馆----------')
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'facchallenge',
            'subtype': 7
        }
        # 周六日领取
        if weekday > 4:
            subtype_list = [7, 13]
            for item in subtype_list:
                params['subtype'] = item
                url = self.base_url + urlencode(params)
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)
        else:
            # 周五挑战
            if weekday == 4:
                subtype_list = [4, 2, 3]
                for item in subtype_list:
                    params['subtype'] = item
                    url = self.base_url + urlencode(params)
                    if item == 4:
                        result = self.content_parser(url, self.pattern_1)
                        print(result[1]) if len(result) > 1 else print(result)
                    if item == 2:
                        for i in range(5):
                            result = self.content_parser(url, self.pattern_1)
                            print(result[1]) if len(result) > 1 else print(result)
                    elif item == 3:
                        for i in range(30):
                            result = self.content_parser(url, self.pattern_1)
                            print(result[1]) if len(result) > 1 else print(result)

        # 矿洞副本
        print('----------矿洞副本----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'factionmine',
            'op': 'fight'
        }
        url = self.base_url + urlencode(params)
        for i in range(3):
            result = self.content_parser(url, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

        # 一键完成每日任务
        print('----------一键完成每日任务----------')
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'task',
            'sub': 7
        }
        url = self.base_url + urlencode(params)
        result = self.content_parser(url, self.pattern_1)
        print(result)
        
        # 帮派任务
        print('----------帮派任务----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'factiontask',
            'sub': 1
        }
        url = self.base_url + urlencode(params)
        reward_list = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "sub=3")]/@href')
        for item in reward_list:
            result = self.content_parser(self.protocol + item, self.pattern_1)
            print(result)

        # 一键分享
        print('----------一键分享----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'sharegame',
            'subtype': 6
        }
        url = self.base_url + urlencode(params)
        result = self.content_parser(url, self.pattern_1)
        print(result[1]) if len(result) > 1 else print(result)

        # 帮派祭坛
        print('----------帮派祭坛----------')
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'altar',
            'op': 'spinwheel'
        }
        url = self.base_url + urlencode(params)
        for i in range(11):
            resp_bytes = self.get_content(url)
            result = etree.HTML(resp_bytes).xpath(self.pattern_1)
            if '选择帮派' in str(result):
                gang_list = etree.HTML(resp_bytes).xpath('//div[@id="id"]/p/a[last()]/@href')
                if gang_list:
                    resp_bytes = self.get_content(self.protocol + gang_list[0])
                    result = etree.HTML(resp_bytes).xpath(self.pattern_1)
                    if '选择路线' in str(result):
                        direction_list = etree.HTML(resp_bytes).xpath('//div[@id="id"]/p/a[last()]/@href')
                        if direction_list:
                            result = self.content_parser(self.protocol + direction_list[0], self.pattern_1)
            
            print(result[1]) if len(result) > 1 else print(result)
            if '转转券不足' in str(result):
                break

        # 领取活跃礼包
        print('----------领取活跃礼包----------')
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'liveness_getgiftbag',
            'giftbagid': 1,
            'action': 1
        }
        for i in range(1,3):
            params['giftbagid'] = i
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

if __name__ == "__main__":

    protocol = 'https:'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'cookie': '',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    }
    # proxies = {'http': 'http://10.5.3.9:80', 'https': 'http://10.5.3.9:80'}
    proxies = {}
    base_url = 'https://dld.qzapp.z.qq.com/qpet/cgi-bin/phonepk?'

    pattern_1 = '//div[@id="id"]/text() | //div[@id="id"]/p/text()'

    pet = qpet(base_url, protocol, headers, proxies, pattern_1)
    pet.main()
