# -*- coding:utf-8 -*-
import random
import loguru
import requests
import re
import json
from library.util import proxies, ticket_sheet, log
from library.constants import URL, CITY_MAP

requests.packages.urllib3.disable_warnings()


class Ticket(object):
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
            import traceback
            traceback.print_exc()
            loguru.logger.error('查票接口错误！', e)
            return False

    def request_config(self):

        journey_date, start_point, end__point, age_type = self.get_point()

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
            "Cookie": "_uab_collina=163843510026522868159604; tk=rfqYT7PvTNCZOToP_E6UmY14rTb_SdvROzUAvgy0z1z0; JSESSIONID=1DCAFFFAC2871CEE540D2C5338512DC4; _jc_save_wfdc_flag=dc; BIGipServerpool_passport=216269322.50215.0000; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; current_captcha_type=Z; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=821035530.64545.0000; _jc_save_fromStation=%u6DEE%u5357%2CHAH; _jc_save_toStation=%u676D%u5DDE%2CHZH; RAIL_EXPIRATION=1642683801231; RAIL_DEVICEID=cVLcmUrJTKiuHtXIuu8PEdtodRGYEJUqRcu65-ASHHNuSzHXfsips7uuG-uj79plfAusBcYtWiYgLnHebFDL9Nr5yDg3fSTisl4IU7K7j6UmUH_KP6nlfOszT4q2JQQwJhMH_cVZ78MYJRG41DycP4FtdwgYQ6rn; _jc_save_fromDate=2022-01-18; _jc_save_toDate=2022-01-18",
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
            "User-Agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/{random.randint(500, 600)}.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
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
            loguru.logger.error(f"出发地址错误: {self.start_point}")

            start_point = False

        try:
            end__point = CITY_MAP.CITY_CODE[self.end__point].upper()
        except Exception:
            loguru.logger.error(f"目标地址错误: {self.end__point}")
            end__point = False

        return journey_date, start_point, end__point, age_type

    def find_stations(self, stations):
        return CITY_MAP.CODE_CITY.get(stations, stations)

    def format_ticket(self, ticket):
        if ticket == '' or ticket == '无' or ticket == '有':
            return ticket
        return int(ticket)

    def parse_(self, resp_json):
        result = resp_json['data']['result']
        data_list = list()
        sheet = ticket_sheet()
        for tk_ in result:
            tk_info = tk_.split('预订')[1]
            pr_info = re.match(
                r'^\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(\d{2}:\d{2})\|(\d{2}:\d{2})\|(\d{2}:\d{2})\|([YN])\|',
                tk_info)
            if pr_info:
                tk_num_ = tk_info.split('|2022')[1]
                tk_num = tk_num_.split('|')
                train_info = {
                    '车次': pr_info[2],
                    '车起始': self.find_stations(pr_info[3]),
                    '车终点': self.find_stations(pr_info[4]),
                    '起始站': self.find_stations(pr_info[5]),
                    '终点站': self.find_stations(pr_info[6]),
                    '出发时间': pr_info[7],
                    '到达时间': pr_info[8],
                    '历时': pr_info[9],
                    '当日到达': pr_info.group(10),
                    '商务座': self.format_ticket(tk_num[19]),
                    '一等座': self.format_ticket(tk_num[18]),
                    '二等座': self.format_ticket(tk_num[17]),
                    '高级软卧': self.format_ticket(tk_num[8]),
                    '一等卧': self.format_ticket(tk_num[10]),
                    '动卧': self.format_ticket(tk_num[20]),
                    '二等卧': self.format_ticket(tk_num[15]),
                    '软卧': self.format_ticket(tk_num[11]),
                    '硬座': self.format_ticket(tk_num[16]),
                    '无座': self.format_ticket(tk_num[13])
                }
                data_list.append(train_info)
                sheet.add_train(train_info)
            else:
                loguru.logger.error('当前余票json解析错误')
        print(sheet.sheet)
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
    end__point = '淮南'
    journey_date = '2022-01-29'
    age_type = 'ADULT'
    tk_r = Ticket(start_point, end__point, journey_date, age_type).query()
    loguru.logger.info(tk_r)
