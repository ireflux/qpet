from typing import ByteString, List
import requests
from requests.adapters import HTTPAdapter, Retry
import random
from urllib.parse import urlencode
from lxml import etree
from datetime import date
import time
import os

class qpet:

    def __init__(self, base_url: str, protocol: str, headers: str, proxies: str, pattern_1: str) -> None:
        self.protocol = protocol
        self.headers = headers
        self.proxies = proxies
        self.base_url = base_url
        self.pattern_1 = pattern_1
        session = requests.Session()
        retries = Retry(total = 3, backoff_factor = 0.3, status_forcelist = [500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        # 获取星期(一到日 -> 0到6)
        self.weekday = date.today().weekday()

    def get_content(self, url: str) -> ByteString:
        try:
            resp = self.session.get(url, proxies = self.proxies, headers = self.headers)
            if 200 == resp.status_code:
                return resp.content
        except requests.ConnectionError:
            raise ConnectionError

    def content_parser(self, url: str, pattern: str) -> List[str]:
        content = self.get_content(url)
        return etree.HTML(content).xpath(pattern)

    def get_player_info(self) -> List[str]:
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'totalinfo',
            'type': 1
        }
        url = self.base_url + urlencode(params)
        content = self.get_content(url)
        all_text = etree.HTML(content).xpath('//div[@id="id"]/text()')
        nick_name = etree.HTML(content).xpath('//div[@id="id"]/a[contains(@href, "cmd=ledouvip")]/preceding::text()[1]')
        title = etree.HTML(content).xpath('//div[@id="id"]/a[contains(@href, "cmd=titleshow")]/text()')
       
        keyword_list = ['称号:', '竞技分段:', '帮派:', '等级:', '体力:', '活力:', '生命:', '敏捷:', '阅历:', '胜率:', '佣兵:']
        player_info = [item for item in all_text if any(keyword in item for keyword in keyword_list)]
        if player_info:
            player_info[0] = player_info[0] + next(iter(title), '无')
            win_rate = [item for item in player_info if '胜率' in item]
            if win_rate:
                win_rate_index = player_info.index(win_rate[0])
                player_info[win_rate_index] = '战斗力' + player_info[win_rate_index]
        
        if nick_name:
            player_info.insert(0, nick_name[0])

        return player_info

    def print_banner(self, banner_path: str) -> None:
        path = os.path.join(os.path.dirname(__file__), banner_path)
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                print(line.rstrip())

    # 领取徒弟经验
    def exp(self):
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'exp'
        }
        url = self.base_url + urlencode(params)
        result = self.content_parser(url, self.pattern_1)
        print([item for item in result if '领取' in item])

    # 每日礼包
    def daily_gift(self):
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'dailygift',
            'op': 'draw',
            'key': 'meridian'
        }
        keys = ['meridian', 'login']
        for item in keys:
            params['key'] = item
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

    # 邪神秘宝
    def ten_lottery(self):
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'tenlottery',
            'op': 2
        }
        for item in range(2):
            params['type'] = item
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

    # 帮派远征军
    def faction_army(self):
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'factionarmy',
            'op': 'viewIndex',
            'island_id': 0
        }
        for island_id in range(5):
            params['island_id'] = island_id
            url = self.base_url + urlencode(params)
            rewards = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "op=getPointAward") or contains(@href, "op=getIslandAward")]/@href')
            for reward in rewards:
                result = self.content_parser(self.protocol + reward, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)

    # 任务派遣中心
    def mission_dispatch_center(self):
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'missionassign',
            'subtype': 0
        }
        url = self.base_url + urlencode(params)
        current_task_list = self.content_parser(url, '//div[@id="id"]/a[contains(@href, "subtype=1")]/@href')
        reward_task_list = [item.replace('subtype=1', 'subtype=5') for item in current_task_list]
        for reward in reward_task_list:
            result = self.content_parser(self.protocol + reward, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

    # 武林大会
    def martial_arts_conference(self):
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'fastSignWulin'
            # 'ifFirstSign': 1
        }
        url = self.base_url + urlencode(params)
        result = self.content_parser(url, self.pattern_1)
        print(result[2]) if len(result) > 2 else print(result)

    # 武林盟主
    def martial_lord(self):
        params = {
                'B_UID': 0,
                'channel': 0,
                'g_ut': 1,
                'cmd': 'wlmz',
                'op': 'view_index'
        }
        # 一三五报名
        signup_time = [0, 2, 4]
        # 二四六竞猜
        guess_time = [1, 3, 5]
        # 领取奖励
        url = self.base_url + urlencode(params)
        reward_url_list = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "op=get_award")]/@href')
        for reward_url in reward_url_list:
            result = self.content_parser(self.protocol + reward_url, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)
        if self.weekday in signup_time:
            params['op'] = 'signup'
            # 黄金(战力>2000)/白银(战力>1000)/青铜(战力>200) 赛场，懒得取战力判断，还是这样简单粗暴的省事儿
            for i in range(1,4):
                params['ground_id'] = i
                url = self.base_url + urlencode(params)
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)
        elif self.weekday in guess_time:
            # 选择玩家
            params['op'] = 'view_guess'
            url = self.base_url + urlencode(params)
            player_list = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "op=guess_up")]/@href')
            if player_list:
                select_result = self.content_parser(self.protocol + player_list[0], self.pattern_1)
                print(select_result[1]) if len(select_result) > 1 else print(select_result)
                # 确认竞猜
                params['op'] = 'comfirm'
                url = self.base_url + urlencode(params)
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)

    # 巅峰之战
    def decisive_battle(self):
        params = {
                'channel': 0,
                'g_ut': 1,
                'cmd': 'gvg',
                'sub': 5,
                'group': 0,
                'check': 1
        }
        # 5: 对战  4：随机加入 南/北 派  1：领取奖励
        sub_list = [5, 4, 1]
        for sub in sub_list:
            params['sub'] = sub
            if self.weekday > 1 and sub == 5:
                url = self.base_url + urlencode(params)
                for i in range(3):
                    result = self.content_parser(url, self.pattern_1)
                    print(result[:3]) if len(result) > 2 else print(result)
            elif sub != 5:
                url = self.base_url + urlencode(params)
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)

    # 历练
    def adventure(self):
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
    def friends_battle(self):
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
                pattern = '//div[@id="id"]/a[contains(@href, "cmd=fight")][position()<6]/@href'
            friend_list = self.content_parser(url, pattern)
            for i in friend_list:
                result = self.content_parser(self.protocol + i, self.pattern_1)
                if item == 'viewmem':
                    print(result[2]) if len(result) > 2 else print(result)
                elif item == 'friendlist':
                    print(result[5]) if len(result) > 5 else print(result)
                else:
                    print(result[3]) if len(result) > 3 else print(result)
                if '体力值不足' in str(result):
                    break

    # 侠士客栈
    def warrior_inn(self):
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
    def resource_battle(self):
        params = {
                'B_UID': 0,
                'channel': 0,
                'g_ut': 1,
                'cmd': 'tbattle'
        }
        url = self.base_url + urlencode(params)
        if self.weekday < 5:
            area_list = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "op=occupy")]/@href')
            if area_list:
                area = random.choice(area_list)
                for i in range(5):
                    result = self.content_parser(self.protocol + area, self.pattern_1)
                    print(result[1]) if len(result) > 1 else print(result)
                    if '只能占领一个领地' in str(result):
                        break

            op_list = ['drawreleasereward', 'drawreward']
            for op in op_list:
                params['op'] = op
                url = self.base_url + urlencode(params)
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)
        else:
            # 帮派助威
            gang_list = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "op=cheerregionbattle") or contains(@href, "op=cheerchampionbattle")]/@href')
            if gang_list:
                result = self.content_parser(self.protocol + random.choice(gang_list), self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)

    # 深渊之潮 
    # params[id]: (1:崎岖斗界/2:魂渡桥/3:须臾之河/4:曲镜空洞/5:光影迷界/6:吞厄源头)
    def abyssal_tide(self):
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'abysstide',
            'op': 'enterabyss',
            'id': 3
        }
        op_list = ['beginfight', 'endabyss']
        for num in range(2):
            params['op'] = 'enterabyss'
            url = self.base_url + urlencode(params)
            self.content_parser(url, self.pattern_1)
            for op in op_list:
                params['op'] = op
                url = self.base_url + urlencode(params)
                if 'beginfight' == op:
                    for i in range(5):
                        result = self.content_parser(url, self.pattern_1)
                        print(result[1]) if len(result) > 1 else print(result)
                        if '憾负' in str(result):
                            break
                elif 'endabyss' == op:
                    result = self.content_parser(url, self.pattern_1)
                    print(result[1]) if len(result) > 1 else print(result)

    # 飞升大作战
    def ascend_heaven(self):
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'ascendheaven',
            'op': 'signup',
            'type': 2
        }
        url = self.base_url + urlencode(params)
        result = self.content_parser(url, self.pattern_1)
        print(result[1]) if len(result) > 1 else print(result)

    # 梦想之旅
    def dream_trip(self):
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'dreamtrip',
        }
        url = self.base_url + urlencode(params)
        #sub: 2: 普通旅行/4: 领取奖励
        actions = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "sub=2") or contains(@href, "sub=4")]/@href')
        for action in actions:
            result = self.content_parser(self.protocol + action, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

    # 帮派黄金联赛
    def faction_league(self):
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'factionleague',
            'op': 5
        }
        # op: 1: 参加帮派黄金联赛 5: 领取奖励 7: 领取帮派赛季奖励
        op_list = [7, 5, 1]
        for op in op_list:
            params['op'] = op
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[0]) if len(result) > 0 else print(result)
    
    # 仙武修真
    def immortals(self):
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'immortals',
            'op': 'fightimmortals'
        }
        url = self.base_url + urlencode(params)
        mountain_list = self.content_parser(url, '//div[@id="id"]/a[contains(@href, "op=visitimmortals")]/@href')
        selected_mountains = []
        if mountain_list:
            selected_mountains = random.sample(mountain_list, 2)
        for mountain in selected_mountains:
            # 选择寻访山脉
            self.content_parser(self.protocol + mountain, self.pattern_1)
            # fight
            result = self.content_parser(url, self.pattern_1)
            print(result[4]) if len(result) > 4 else print(result)

    # 会武
    def sect_melee(self):
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'sectmelee',
            'op': 'dotraining'
        }
        # dotraining: 试炼；cheer: 冠军助威；drawreward: 领奖
        op_list = ['dotraining', 'cheer', 'drawreward']
        for op in op_list:
            params['op'] = op
            url = self.base_url + urlencode(params)
            if self.weekday < 3:
                if op == 'dotraining':
                    for i in range(15):
                        result = self.content_parser(url, self.pattern_1)
                        print(result[:4]) if len(result) > 3 else print(result)
                        if '试炼书不足' in str(result):
                            break
                elif op == 'cheer':
                    params['sect'] = 1003
                    url = self.base_url + urlencode(params)
                    result = self.content_parser(url, self.pattern_1)
                    print(result[2]) if len(result) > 2 else print(result)
            elif self.weekday > 4 and op == 'drawreward':
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)

    # 门派邀请赛
    def sect_tournament(self):
        params = {
                'channel': 0,
                'g_ut': 1,
                'cmd': 'secttournament',
                'op': 'fight'
        }
        op_list = ['fight', 'signup']
        for op in op_list:
            params['op'] = op
            url = self.base_url + urlencode(params)
            if self.weekday > 1 and op == 'fight':
                for i in range(5):
                    result = self.content_parser(url, self.pattern_1)
                    print(result[1]) if len(result) > 1 else print(result)
                    if '门派战书不足' in str(result):
                        break
            elif op == 'signup':
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)

    # 门派
    def sect(self):
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
                
                # 领取任务奖励
                params['cmd'] = 'sect_task'
                url = self.base_url + urlencode(params)
                reward_list = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "subtype=2")]/@href')
                for item in reward_list:
                    result = self.content_parser(self.protocol + item, self.pattern_1)
                    print(result[1]) if len(result) > 1 else print(result)
            else:
                result = self.content_parser(url, self.pattern_1)
                if item == 'fumigatefreeincense':
                    print(result[2]) if len(result) > 2 else print(result)
                else:
                    print(result[1]) if len(result) > 1 else print(result)

    # 群雄逐鹿
    def thrones_battle(self):
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
    def misty(self):
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'misty'
        }
        url = self.base_url + urlencode(params)
        area_list = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "op=start")][last()]/@href')
        if area_list:
            self.content_parser(self.protocol + area_list[0], self.pattern_1)
        op_list = ['fight', 'reward', 'return']
        for item in op_list:
            params['op'] = item
            if 'fight' == item:
                url = self.base_url + urlencode(params)
                for i in range(5):
                    result = self.content_parser(url, self.pattern_1)
                    print(result[3]) if len(result) > 3 else print(result)
                    if '挑战已结束' in str(result):
                        break
            else:
                params['box_id'] = 3
                url = self.base_url + urlencode(params)
                result = self.content_parser(url, self.pattern_1)
                print(result[3]) if len(result) > 3 else print(result)

    # 斗神塔
    def tower_fight(self):
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'towerfight',
            'type': 7,
            'confirm': 1
        }
        # params[type]: (7:结束战斗/11：自动挑战)
        type_list = [7,11]
        for item in type_list:
            params['type'] = item
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

    # 抢地盘
    def grab_territory(self):
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'recommendmanor',
            'type': 7,
            'page': 1
        }
        url = self.base_url + urlencode(params)
        enemy_list = self.content_parser(url, '//div[@id="id"]/a[contains(@href, "cmd=manorfight")]/@href')
        if enemy_list:
            result = self.content_parser(self.protocol + random.choice(enemy_list), self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

    # 画卷谜踪
    def scroll_dungeon(self):
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
    def zodiac_dungeon(self):
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
        result_str = '\n'.join(result)
        print(result_str)

    # 镖行天下
    def escort_cargo(self):
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
    def arena(self):
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'arena',
            'op': 'challenge'
        }
        op_list = ['challenge', 'drawdaily']
        interrupt_signal = ['免费挑战次数已用完', '不在比赛时间内']
        for item in op_list:
            params['op'] = item
            url = self.base_url + urlencode(params)
            if item == 'challenge':
                for i in range(5):
                    result = self.content_parser(url, self.pattern_1)
                    print(result[1]) if len(result) > 1 else print(result)
                    if any(item in str(result) for item in interrupt_signal):
                        break
            else:
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)

    # 踢馆
    def challenge(self):
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'facchallenge',
            'subtype': 7
        }
        # subtype: 1:报名, 2:试炼, 3:挑战, 4:高倍转盘, 7:领奖, 13:排行奖励
        # 周六日领取
        if self.weekday > 4:
            subtype_list = [7, 13, 1]
            for item in subtype_list:
                params['subtype'] = item
                url = self.base_url + urlencode(params)
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)
        elif self.weekday == 4:
            # 周五挑战
            subtype_list = [4, 2, 3]
            interrupt_signal = ['您的复活次数已耗尽', '当前不在试练时间范围']
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
                        if any(item in str(result) for item in interrupt_signal):
                            break
                elif item == 3:
                    for i in range(30):
                        result = self.content_parser(url, self.pattern_1)
                        print(result[1]) if len(result) > 1 else print(result)
                        if any(item in str(result) for item in interrupt_signal):
                            break

    # 掠夺粮仓
    def forage_war(self):
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'forage_war',
            'subtype': 3
        }
        subtype_list = [3, 5, 6]
        for item in subtype_list:
            params['subtype'] = item
            url = self.base_url + urlencode(params)
            if self.weekday == 1 and item == 3:
                granary_list = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "subtype=4")]/@href')
                exit_flag = False
                for granary in granary_list[::-1]:
                    if exit_flag:
                        break
                    while True:
                        # 停顿1.5秒
                        time.sleep(1.5)
                        result = self.content_parser(self.protocol + granary, self.pattern_1)
                        print(result[1]) if len(result) > 1 else print(result)
                        if '这个粮仓已被我方掠夺' in str(result):
                            break
                        if '你已经没有足够的复活次数' in str(result):
                            exit_flag = True
                            break
            elif item != 3:
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)

    # 矿洞
    def mine_cave(self):
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'factionmine',
            'op': 'fight'
        }
        op_list = ['fight', 'reward']
        for op in op_list:
            params['op'] = op
            url = self.base_url + urlencode(params)
            if op == 'fight':
                for i in range(3):
                    result = self.content_parser(url, self.pattern_1)
                    print(result[1]) if len(result) > 1 else print(result)
                    if '挑战次数不足' in str(result):
                        break
            elif op == 'reward':
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)

    # 全民乱斗
    def chaos_fight(self):
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'luandou',
            'op': 0,
            'acttype': 2
        }
        acttype_list = [2, 3, 4]
        for item in acttype_list:
            params['acttype'] = item
            url = self.base_url + urlencode(params)
            reward_list = self.content_parser(url, '//div[@id="id"]/a[contains(@href, "op=8")]/@href')
            for reward in reward_list:
                result = self.content_parser(self.protocol + reward, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)

    # 帮派商会
    def gang_market(self):
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'fac_corp',
            'op': 0
        }
        url = self.base_url + urlencode(params)
        gifts = self.content_parser(url, '//div[@id="id"]/a[contains(@href, "op=3")]/@href')
        for gift in gifts:
            result = self.content_parser(self.protocol + gift, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)
    
    # 一键完成任务
    def common_mission(self):
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'task',
            'sub': 7
        }
        url = self.base_url + urlencode(params)
        result = self.content_parser(url, self.pattern_1)
        result_str = '\n'.join(result)
        print(result_str)

    # 帮派任务
    def gang_mission(self):
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

    # 领取帮派奖励
    def gang_reward(self):
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'facwar',
            'sub': 4
        }
        url = self.base_url + urlencode(params)
        result = self.content_parser(url, self.pattern_1)
        print(result[3]) if len(result) > 3 else print(result)

    # 一键分享
    def share_game(self):
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
    def gang_altar(self):
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'altar'
        }
        # 高级祭坛升级满了之后会有祭祀奖励。领取祭祀奖励，如果存在的话
        url = self.base_url + urlencode(params)
        reward_urls = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "op=drawreward")]/@href')
        if reward_urls:
            result = self.content_parser(self.protocol + reward_urls[0], self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

        # 祭坛转盘
        interrupt_signal = ['转转券不足', '该帮派已解散']
        params['op'] = 'spinwheel'
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
            if any(item in str(result) for item in interrupt_signal):
                break

    # 领取活跃礼包
    def get_active_reward(self):
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'liveness_getgiftbag',
            'giftbagid': 1,
            'action': 1
        }
        for item in range(1,3):
            params['giftbagid'] = item
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[1]) if len(result) > 1 else print(result)

    # 领取活动免费礼包
    def get_special_event(self):
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'pacfg'
        }
        
        free_rewards = {'cmd=newAct&subtype=88': '神魔大转盘',
                        'cmd=newAct&subtype=124': '开心娃娃机',
                        'cmd=newAct&subtype=43': '每日好礼步步升',
                        'cmd=newAct&subtype=57': '幸运大转盘',
                        'cmd=newAct&subtype=94': '活跃礼包',
                        'cmd=menuact': '乐斗菜单',
                        'cmd=oddeven': '猜单双',
                        'cmd=weekgiftbag': '周周礼包'

        }
        url = self.base_url + urlencode(params)
        all_activity_url = self.content_parser(url, '//div[@id="id"]/p/a/@href')
        url_list = [item for item in all_activity_url if any(reward_url in item for reward_url in list(free_rewards))]
        reward_url = []
        for url in url_list:
            if 'cmd=newAct&subtype=43' in url:
                reward_url = self.content_parser(self.protocol + url, '//div[@id="id"]/p/a[contains(@href, "op=get")]/@href')
                if reward_url:
                    result = self.content_parser(self.protocol + reward_url[0], self.pattern_1)
                    print(result[1]) if len(result) > 1 else print(result)
            elif 'cmd=newAct&subtype=57' in url:
                reward_url = self.content_parser(self.protocol + url, '//div[@id="id"]/p/a[contains(@href, "op=roll")]/@href')
                if reward_url:
                    result = self.content_parser(self.protocol + reward_url[0], self.pattern_1)
                    print(result[1]) if len(result) > 1 else print(result)
            elif 'cmd=menuact' in url:
                reward_url = self.content_parser(self.protocol + url, '//div[@id="id"]/a[contains(@href, "sub=1")][last()]/@href')
                if reward_url:
                    result = self.content_parser(self.protocol + reward_url[0], self.pattern_1)
                    print(result[4]) if len(result) > 4 else print(result)
            elif 'cmd=oddeven' in url:
                options = self.content_parser(self.protocol + url, '//div[@id="id"]/p/a[contains(@href, "value=1") or contains(@href, "value=2")]/@href')
                if options:
                    while True:
                        result = self.content_parser(self.protocol + random.choice(options), self.pattern_1)
                        print(result[1]) if len(result) > 1 else print(result)
                        if '很遗憾，您猜错了' in str(result):
                            break
            elif 'cmd=weekgiftbag' in url:
                reward_url = self.content_parser(self.protocol + url, '//div[@id="id"]/p/a[contains(@href, "sub=1")]/@href')
                if reward_url:
                    result = self.content_parser(self.protocol + reward_url[0], self.pattern_1)
                    print(result[1]) if len(result) > 1 else print(result)
            else:
                reward_url = self.content_parser(self.protocol + url, '//div[@id="id"]/p/a[contains(@href, "op=1")]/@href')
                if reward_url:
                    result = self.content_parser(self.protocol + reward_url[0], self.pattern_1)
                    print(result[1]) if len(result) > 1 else print(result)
            
    def main(self):
        print('----------玩家信息----------')
        player_info = self.get_player_info()
        print('\n'.join(player_info))

        print('----------领取徒弟经验----------')
        self.exp()
        print('----------每日奖励----------')
        self.daily_gift()
        print('----------邪神秘宝----------')
        self.ten_lottery()
        print('----------帮派远征军----------')
        self.faction_army()
        print('----------任务派遣中心----------')
        self.mission_dispatch_center()
        print('----------武林大会----------')
        self.martial_arts_conference()
        print('----------武林盟主----------')
        self.martial_lord()
        print('----------巅峰之战----------')
        self.decisive_battle()
        print('----------历练----------')
        self.adventure()
        print('----------好友对战----------')
        self.friends_battle()
        print('----------侠士客栈----------')
        self.warrior_inn()
        print('----------问鼎天下----------')
        self.resource_battle()
        print('----------深渊之潮----------')
        self.abyssal_tide()
        print('----------飞升大作战----------')
        self.ascend_heaven()
        print('----------梦想之旅----------')
        self.dream_trip()
        print('----------帮派黄金联赛----------')
        self.faction_league()   
        print('----------仙武修真----------')
        self.immortals()
        print('----------会武----------')
        self.sect_melee()
        print('----------门派邀请赛----------')
        self.sect_tournament()
        print('----------门派----------')
        self.sect()
        print('----------群雄逐鹿----------')
        self.thrones_battle()
        print('----------幻境----------')
        self.misty()
        print('----------斗神塔----------')
        self.tower_fight()
        print('----------抢地盘----------')
        self.grab_territory()
        print('----------画卷谜踪----------')
        self.scroll_dungeon()
        print('----------十二宫----------')
        self.zodiac_dungeon()
        print('----------镖行天下----------')
        self.escort_cargo()
        print('----------竞技场----------')
        self.arena()
        print('----------踢馆----------')
        self.challenge()
        print('----------掠夺----------')
        self.forage_war()
        print('----------矿洞副本----------')
        self.mine_cave()    
        print('----------全民乱斗----------')
        self.chaos_fight()  
        print('----------帮派商会----------')
        self.gang_market()
        print('----------一键完成每日任务----------')
        self.common_mission()
        print('----------帮派任务----------')
        self.gang_mission()
        print('----------领取帮战奖励----------')
        self.gang_reward()
        print('----------一键分享----------')
        self.share_game()
        print('----------帮派祭坛----------')
        self.gang_altar()
        print('----------领取活跃礼包----------')
        self.get_active_reward()
        print('----------领取活动免费礼包----------')
        self.get_special_event()

if __name__ == "__main__":
    try:
        cookie = os.environ["QPET_COOKIE"]
    except Exception:
        raise ValueError

    protocol = 'https:'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }
    proxies = {}
    # Q宠大乐斗地址
    base_url = 'https://dld.qzapp.z.qq.com/qpet/cgi-bin/phonepk?'
    pattern_1 = '//div[@id="id"]/text() | //div[@id="id"]/p/text()'
    banner_path = './banner.txt'

    pet = qpet(base_url, protocol, headers, proxies, pattern_1)
    pet.print_banner(banner_path)
    pet.main()
