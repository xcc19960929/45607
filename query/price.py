# -*- coding:utf-8 -*-
import random
import loguru
import requests
import re
import json
from library.constants import URL
from library.util import proxies

requests.packages.urllib3.disable_warnings()

class Price():
    def __init__(self, train_no, from_station_no, to_station_no, seat_types, train_date):
        self.train_no = train_no
        self.from_station_no = from_station_no
        self.to_station_no = to_station_no
        self.seat_types = seat_types
        self.train_date = train_date


    def request_config(self):
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
            "Referer": f"https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E4%B8%8A%E6%B5%B7,SHH&ts=%E6%88%90%E9%83%BD,CDW&date={self.train_date}&flag=N,N,Y",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/{random.randint(500, 600)}.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        params = {
            "train_no": self.train_no,
            "from_station_no": self.from_station_no,
            "to_station_no": self.to_station_no,
            "seat_types": self.seat_types,
            "train_date": self.train_date
        }
        return {
            'url': URL.queryTicketPrice,
            'params': params,
            'headers': headers,
            'verify': False,
            'timeout': 15,
            # 'proxies': proxies
        }


    def send_request(self, kwargs):
        try:
            response = requests.get(**kwargs)
            return response.json()
        except Exception as e:
            loguru.logger.error('查票接口错误！', e)
            return False

    def parse(self, resp_json):
        return json.dumps(resp_json['data'], ensure_ascii=False)


    def query(self):
        ci = self.request_config()
        query_r = self.send_request(ci)
        if not query_r or query_r['httpstatus'] != 200:
            loguru.logger.error(f"查价格请求错误！")
            return False
        price_r = self.parse(query_r)
        loguru.logger.error(f"查价格成功！")
        return price_r






if __name__ == '__main__':
    train_no = '550000K282D2'
    from_station_no = '01'
    to_station_no = '28'
    seat_types = '3141'
    train_date = '2022-01-13'
    price_r = Price(train_no, from_station_no, to_station_no, seat_types, train_date).query()
    loguru.logger.info(price_r)

