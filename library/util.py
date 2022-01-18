import os
import prettytable as pt

proxy_host = 'http-dyn.abuyun.com'
proxy_port = '9020'
proxy_user = os.getenv('ABY_PROXY_USER', '')
proxy_pass = os.getenv('ABY_PROXY_PASS', '')
proxies = {
    'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
    'https': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
}


def log(s, color=None):
    s = str(s)
    if color == 'r':
        return "\033[31m%s\033[0m" % s
    elif color == 'y':
        return "\033[33m%s\033[0m" % s
    elif color == 'g':
        return "\033[32m%s\033[0m" % s
    elif color == 'b':
        return "\033[36m%s\033[0m" % s
    else:
        return s


class ticket_sheet:
    def __init__(self, fields: list = None):
        self.pt = pt.PrettyTable()
        self.fields = fields or ['车次', '车起始', '车终点', '起始站', '终点站', '出发时间', '到达时间', '历时', '当日到达', '商务座', '一等座',
                                 '二等座', '高级软卧', '一等卧', '动卧', '二等卧', '软卧', '硬座', '无座']
        self.pt.field_names = self.fields
        self.pt.align = 'l'

    def add_train(self, train):
        train_fields = list()
        for field in self.fields[1:]:
            value = train[field]
            if isinstance(value, int):
                if value <= 5:
                    value = log(value, 'r')
                else:
                    value = log(value, 'y')
            train_fields.append(value)
        self.add_row(
            train['车次'],
            train_fields
        )

    def add_row(self, key: str, value: list):
        _value = list()
        for v in value:
            if isinstance(v, int) and v <= 5:
                _value.append(log(v, 'r'))
            else:
                _value.append(v)
        _value.insert(0, log(key, color='g'))
        self.pt.add_row(_value)

    def add_column(self, key: str, value: list):
        self.pt.add_column(key, value)

    @property
    def sheet(self):
        return self.pt


if __name__ == '__main__':
    print(log('asdas', 'b'))
