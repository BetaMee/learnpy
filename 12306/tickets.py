# coding: utf-8

"""命令行火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""
from docopt import docopt
from stations import stations
import requests
from prettytable import PrettyTable
from colorama import init, Fore

init()

class TrainsCollection:

    header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()

    # 初始化函数
    def __init__(self, available_trains, station_map, options):
        """查询到的火车班次集合

        :param available_trains: 一个列表, 包含可获得的火车班次, 每个
                                 火车班次是一个字典
        :param options: 查询的选项, 如高铁, 动车, 比如 -k -d -g
        """
        self.available_trains = available_trains # 各个站点信息 []
        self.station_map = station_map # 出发到达站点中文code映射
        self.options = options # 命令行选项

    # 格式化时间
    def _get_duration(self, lishi):
        duration = lishi.replace(':', '小时') + '分'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    # 修饰器，只读属性
    @property
    def trains(self):
        for raw_train in self.available_trains:
            # 对单条数据进行解析
            train_info = raw_train.split('|')
            # 列车班次 如G310
            train_no = train_info[3]
            # 取首字母，用于判断过滤
            initial = train_no[0].lower()
            # 取火车区间站点映射信息 出发站点和到站站点
            from_station_name = self.station_map[train_info[6]]
            to_station_name = self.station_map[train_info[7]]
            # 取火车出发和到达时间
            start_time = train_info[8]
            arrive_time = train_info[9]

            if not self.options or initial in self.options:
                train = [
                    train_no, # 列车班次
                    '\n'.join([
                        Fore.GREEN + from_station_name + Fore.RESET,
                        Fore.RED + to_station_name + Fore.RESET
                    ]), # 出发到达区间
                    '\n'.join([
                        Fore.GREEN + start_time + Fore.RESET,
                        Fore.RED + arrive_time + Fore.RESET
                    ]), # 出发到达时间
                    self._get_duration(train_info[10]), # 历时时间
                    train_info[31] or '--', # 一等座
                    train_info[30] or '--', # 二等座
                    train_info[23] or '--', # 软卧
                    train_info[28] or '--', # 硬卧
                    train_info[29] or '--', # 硬座
                    train_info[26] or '--', # 无座
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    # 构建URL
    url = ('https://kyfw.12306.cn/otn/leftTicket/query?'
           'leftTicketDTO.train_date={}&'
           'leftTicketDTO.from_station={}&'
           'leftTicketDTO.to_station={}&'
           'purpose_codes=ADULT'
           ).format(date, from_station, to_station)
    # 选项
    options = ''.join([
        # 过滤操作
        key for key, value in arguments.items() if value is True
    ])
    # 发送请求
    r = requests.get(url, verify=True)
    # 返回数据
    trains_data = r.json()['data']
    available_trains = trains_data['result'] # 列车车次信息
    station_map = trains_data['map'] # 站点中文code映射
    # 打印成列表
    TrainsCollection(available_trains, station_map, options).pretty_print()

if __name__ == '__main__': cli()

