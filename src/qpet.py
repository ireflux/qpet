from typing import ByteString, List
import requests
import random
from urllib.parse import urlencode
from lxml import etree
from datetime import date
import time
import os

class qpet(object):

    def __init__(self, base_url: str, protocol: str, headers: str, proxies: str, pattern_1: str) -> None:
        self.protocol = protocol
        self.headers = headers
        self.proxies = proxies
        self.base_url = base_url
        self.pattern_1 = pattern_1

    def get_content(self, url: str) -> ByteString:
        try:
            resp = requests.get(url, proxies = self.proxies, headers = self.headers)
            if 200 == resp.status_code:
                return resp.content
        except requests.ConnectionError:
            return None

    def content_parser(self, url: str, pattern: str) -> List[str]:
        content = self.get_content(url)
        return etree.HTML(content).xpath(pattern)

    def get_player_info(self) -> List[str]:
        print('----------玩家信息----------')
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

    def print_banner(self, banner_path) -> None:
        path = os.path.join(os.path.dirname(__file__), banner_path)
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                print(line.rstrip())

    def main(self) -> None:
        # 获取星期(一到日 -> 0到6)
        weekday = date.today().weekday()

        # 获取玩家信息
        player_info = self.get_player_info()
        print('\n'.join(player_info))

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
        keys = ['meridian', 'login']
        for item in keys:
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

        # 帮派远征军
        print('----------帮派远征军----------')
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
        print('----------任务派遣中心----------')
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
        print(result[2]) if len(result) > 2 else print(result[1])

        # 武林盟主 领奖暂未添加
        print('----------武林盟主----------')
        params = {
                'channel': 0,
                'g_ut': 1,
                'cmd': 'wlmz',
                'op': 'signup'
            }
        # 一三五报名
        signup_time = [0, 2, 4]
        # 二四六竞猜
        guess_time = [1, 3, 5]
        if weekday in signup_time:
            # 黄金(战力>2000)/白银(战力>1000)/青铜(战力>200) 赛场，懒得取战力判断，还是这样简单粗暴的省事儿
            for i in range(1,4):
                params['ground_id'] = i
                url = self.base_url + urlencode(params)
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)
        elif weekday in guess_time:
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
                print(result[1]) if len(result) > 1 else print(result[1])

        # 巅峰之战
        print('----------巅峰之战----------')
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
            if weekday > 1 and sub == 5:
                url = self.base_url + urlencode(params)
                for i in range(3):
                    result = self.content_parser(url, self.pattern_1)
                    print(result[:3]) if len(result) > 2 else print(result)
            elif sub != 5:
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
        params = {
                'B_UID': 0,
                'channel': 0,
                'g_ut': 1,
                'cmd': 'tbattle'
        }
        url = self.base_url + urlencode(params)
        if weekday < 5:
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
            print(type(self.get_content(url)))
            gang_list = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "op=cheerregionbattle") or contains(@href, "op=cheerchampionbattle")]/@href')
            if gang_list:
                result = self.content_parser(self.protocol + random.choice(gang_list), self.pattern_1)
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
        # op: 1: 参加帮派黄金联赛 5: 领取奖励 7: 领取帮派赛季奖励
        op_list = [7, 5, 1]
        for op in op_list:
            params['op'] = op
            url = self.base_url + urlencode(params)
            result = self.content_parser(url, self.pattern_1)
            print(result[0]) if len(result) > 0 else print(result)

        # 仙武修真
        print('----------仙武修真----------')
        params = {
            'channel': 0,
            'g_ut': 1,
            'cmd': 'immortals',
            'op': 'fightimmortals'
        }
        url = self.base_url + urlencode(params)
        mountain_list = self.content_parser(url, '//div[@id="id"]/a[contains(@href, "op=visitimmortals")]/@href')
        if mountain_list:
            mountains = random.sample(mountain_list, 2)
        for mountain in mountains:
            # 选择寻访山脉
            self.content_parser(self.protocol + mountain, self.pattern_1)
            # fight
            result = self.content_parser(url, self.pattern_1)
            print(result[4]) if len(result) > 4 else print(result)

        # 会武
        print('----------会武----------')
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
            if weekday < 3:
                if op == 'cheer':
                    params['sect'] = 1003
                    result = self.content_parser(url, self.pattern_1)
                    print(result[2]) if len(result) > 2 else print(result)
                elif op == 'dotraining':
                    for i in range(15):
                        result = self.content_parser(url, self.pattern_1)
                        print(result[:4]) if len(result) > 3 else print(result)
                        if '试炼书不足' in str(result):
                            break
            elif weekday > 4 and op == 'drawreward':
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
        op_list = ['fight', 'signup']
        for op in op_list:
            params['op'] = op
            url = self.base_url + urlencode(params)
            if weekday > 1 and op == 'fight':
                for i in range(5):
                    result = self.content_parser(url, self.pattern_1)
                    print(result[1]) if len(result) > 1 else print(result)
                    if '门派战书不足' in str(result):
                        break
            elif op == 'signup':
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
            else:
                params['box_id'] = 3
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
        if enemy_list:
            result = self.content_parser(self.protocol + random.choice(enemy_list), self.pattern_1)
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
        print('----------踢馆----------')
        params = {
            'B_UID': 0,
            'channel': 0,
            'g_ut': 1,
            'cmd': 'facchallenge',
            'subtype': 7
        }
        # subtype: 1:报名, 2:试炼, 3:挑战, 4:高倍转盘, 7:领奖, 13:排行奖励
        # 周六日领取
        if weekday > 4:
            subtype_list = [7, 13, 1]
            for item in subtype_list:
                params['subtype'] = item
                url = self.base_url + urlencode(params)
                result = self.content_parser(url, self.pattern_1)
                print(result[1]) if len(result) > 1 else print(result)
        elif weekday == 4:
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

        # 掠夺
        print('----------掠夺----------')
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
            if weekday == 1 and item == 3:
                granary_list = self.content_parser(url, '//div[@id="id"]/p/a[contains(@href, "subtype=4")]/@href')
                exit_flag = False
                for granary in granary_list[::-1]:
                    if exit_flag:
                        break
                    while True:
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

        # 矿洞副本
        print('----------矿洞副本----------')
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
        print('----------全民乱斗----------')
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
        print('----------帮派商会----------')
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

        # 领取帮战奖励
        print('----------领取帮战奖励----------')
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
        interrupt_signal = ['转转券不足', '该帮派已解散']
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
        print('----------领取活跃礼包----------')
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

if __name__ == "__main__":
    cookie = os.environ["QPET_COOKIE"]

    protocol = 'https:'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }
    proxies = {}
    base_url = 'https://dld.qzapp.z.qq.com/qpet/cgi-bin/phonepk?'
    pattern_1 = '//div[@id="id"]/text() | //div[@id="id"]/p/text()'
    banner_path = './banner.txt'

    pet = qpet(base_url, protocol, headers, proxies, pattern_1)
    pet.print_banner(banner_path)
    pet.main()
