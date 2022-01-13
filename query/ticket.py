# -*- coding:utf-8 -*-
import random
import loguru
import requests
import re
import json
from library.util import proxies
from library.constants import URL, CITY_MAP

requests.packages.urllib3.disable_warnings()


class Ticket():
    def __init__(self, start_point, end__point, journey_date, age_type: str = 'ADULT'):
        self.start_point = start_point
        self.end__point = end__point
        self.journey_date = journey_date
        self.age_type = age_type


    def send_request(self, kwargs):
        try:
            response = requests.get(**kwargs)
            return response.json()
        except Exception as e:
            loguru.logger.error('查票接口错误！', e)
            return False


    def request_config(self):

        journey_date, start_point, end__point, age_type= self.get_point()

        if not start_point and not end__point:
            return False

        params = {
            "leftTicketDTO.train_date": journey_date,
            "leftTicketDTO.from_station": start_point,
            "leftTicketDTO.to_station": end__point,
            "purpose_codes": age_type,
        }

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "JSESSIONID=63F76990BCFA7B7EF1F4B683AF7CA224; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=1356398858.24610.0000;",
            "Host": "kyfw.12306.cn",
            "If-Modified-Since": "0",
            "Pragma": "no-cache",
            "Referer": f"https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E4%B8%8A%E6%B5%B7,SHH&ts=%E6%88%90%E9%83%BD,CDW&date={journey_date}&flag=N,N,Y",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/{random.randint(500,600)}.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        return {
            'url': URL.queryTicketInfo,
            'params': params,
            'headers': headers,
            'verify': False,
            'timeout': 15,
            # 'proxies': proxies
        }


    def get_point(self):
        journey_date = self.journey_date
        age_type = self.age_type

        try:
            start_point = CITY_MAP.CITY_CODE[self.start_point].upper()
        except Exception:
            loguru.logger.error(f"出发地址错误: { self.start_point}")

            start_point = False


        try:
            end__point = CITY_MAP.CITY_CODE[self.end__point].upper()
        except Exception:
            loguru.logger.error(f"目标地址错误: { self.end__point}")
            end__point = False

        return journey_date, start_point, end__point, age_type


    def parse_(self, resp_json):
        result = resp_json['data']['result']
        data_list = list()
        for tk_ in result:
            tk_info = tk_.split('预订')[1]
            pr_info = re.match( r'^\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(\d{2}:\d{2})\|(\d{2}:\d{2})\|(\d{2}:\d{2})\|([YN])\|',tk_info)
            if pr_info:
                tk_num_ = tk_info.split('|2022')[1]
                tk_num = tk_num_.split('|')
                # train_no
                # loguru.logger.info(f'train _no: {pr_info.group(1)}')
                # # 车次
                # loguru.logger.info(f'车     次: {pr_info.group(2)}')
                # # 车次起点站
                # loguru.logger.info(f'车次起点站: {CITY_MAP.CODE_CITY[pr_info.group(3)]}')
                # # 车次终点站
                # loguru.logger.info(f'车次终点站: {CITY_MAP.CODE_CITY[pr_info.group(4)]}')
                # # 起点站
                # loguru.logger.info(f'起   点站: {CITY_MAP.CODE_CITY[pr_info.group(5)]}')
                # # 终点站
                # loguru.logger.info(f'终   点站: {CITY_MAP.CODE_CITY[pr_info.group(6)]}')
                # # 出发时间git
                # loguru.logger.info(f'出发 时间: {pr_info.group(7)}')
                # # 到达时间
                # loguru.logger.info(f'到达 时间: {pr_info.group(8)}')
                # # 历时
                # loguru.logger.info(f'历    时: {pr_info.group(9)}')
                # # 是否当日到达
                # loguru.logger.info(f'是否当日到达: {pr_info.group(10)}')
                # # 商务座、特等座
                # loguru.logger.info(f'商务座、  特等座: {tk_num[19]}')
                # # 一等座
                # loguru.logger.info(f'一等         座: {tk_num[18]}')
                # # 二等座、二等包座
                # loguru.logger.info(f'二等座、二等包座: {tk_num[17]}')
                # # 高级软卧
                # loguru.logger.info(f'高级       软卧: {tk_num[8]}')
                # # 软卧、一等卧
                # loguru.logger.info(f'软卧     一等卧: {tk_num[10]}')
                # # 动卧
                # loguru.logger.info(f'动          卧: {tk_num[20]}')
                # # 硬卧、二等卧
                # loguru.logger.info(f'软卧     二等卧: {tk_num[15]}')
                # # 软卧
                # loguru.logger.info(f'软          卧: {tk_num[11]}')
                # # 硬座
                # loguru.logger.info(f'硬          座: {tk_num[16]}')
                # # 无座
                # loguru.logger.info(f'无          座: {tk_num[13]}')
                # # from_station_no
                # loguru.logger.info(f'from_station_no: {tk_num[3]}')
                # # to_station_no
                # loguru.logger.info(f'to_station_no: {tk_num[4]}')
                # # seat_types
                # loguru.logger.info(f'seat    types: {tk_num[21]}')
                #
                # loguru.logger.info(f'----------------------------')
                data_list.append({
                    "train_info": {
                        'train _no': pr_info.group(1),
                        '车     次': pr_info.group(2),
                        '车次起点站': pr_info.group(3),
                        '车次终点站': pr_info.group(4),
                        '起   点站': pr_info.group(5),
                        '终   点站': pr_info.group(6),
                        '出发 时间': pr_info.group(7),
                        '到达 时间': pr_info.group(8),
                        '历    时': pr_info.group(9),
                        '是否当日到达': pr_info.group(10)
                    },
                    "ticket_info": {
                        '商务座、  特等座': tk_num[19],
                        '一等         座': tk_num[18],
                        '二等座、二等包座': tk_num[17],
                        '高级       软卧': tk_num[8],
                        '软卧     一等卧': tk_num[10],
                        '动          卧': tk_num[20],
                        '软卧     二等卧': tk_num[15],
                        '软          卧': tk_num[11],
                        '硬          座': tk_num[16],
                        '无          座': tk_num[13]
                    },
                    "price_info": {
                        'from_station_no': tk_num[3],
                        'to_station_no': tk_num[4],
                        'seat    types': tk_num[21],
                        'train    date': self.journey_date
                    }
                })
            else:
                loguru.logger.error('当前余票json解析错误')
        return data_list


    def query(self):
        ci = self.request_config()
        if not ci:
            loguru.logger.error(f"查票配置错误！")
            return False
        query_r = self.send_request(ci)
        if not query_r or query_r['httpstatus'] != 200:
            loguru.logger.error(f"查票请求错误！")
            return False
        tk_r = self.parse_(query_r)
        if tk_r:
            loguru.logger.error(f"查票成功！")
        return json.dumps(tk_r, ensure_ascii=False)


if __name__ == '__main__':
    start_point = '杭州'
    end__point = '芜湖'
    journey_date = '2022-01-14'
    age_type = 'ADULT'
    tk_r = Ticket(start_point, end__point, journey_date, age_type).query()
    loguru.logger.info(tk_r)
