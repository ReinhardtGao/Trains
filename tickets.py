# coding: utf-8
"""命令行火车票查看器

Usage:
    tickets [-gdctkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -c          城铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 天津 2017-05-20
    tickets -dg 成都 南京 2017-05-20
"""
import colorama
import requests
from docopt import docopt
from prettytable import PrettyTable
from stations import stations

colorama.init()


class TrainsCollection(object):
    headers = "车次 起始站 终点站 出发时间 到达时间 历时 一等座 二等座 软卧 硬卧 硬座 无座".split()

    def __init__(self, available_trains, options):
        self.available_trains = available_trains
        self.options = options

    def _color_print(self, item, color):
        return color + item + colorama.Fore.RESET

    @property
    def trains(self):
        for item in self.available_trains['result']:
            item = item.split("|")
            train_no = item[3].lower()
            # 过滤为空或者是在过滤选项中
            if not self.options or train_no[0] in self.options:
                start_station = self.available_trains['map'].get(item[6])
                end_station = self.available_trains['map'].get(item[7])
                departure = item[8]
                arrival = item[9]
                duration = item[10]
                yideng = item[-4]
                erdeng = item[-5]
                ruanwo = item[23]
                yingwo = item[-7]
                yingzuo = item[-6]
                wuzuo = item[26]
                row = [train_no,
                       self._color_print(start_station, colorama.Fore.MAGENTA),
                       self._color_print(end_station, colorama.Fore.GREEN),
                       self._color_print(departure, colorama.Fore.MAGENTA),
                       self._color_print(arrival, colorama.Fore.GREEN),
                       duration, yideng, erdeng, ruanwo, yingwo, yingzuo, wuzuo]
                yield row

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.headers)
        for train in self.trains:
            pt.add_row(train)
        print(pt)


def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    # print(arguments)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    # url set up
    url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT".format(
        date, from_station, to_station)
    options = ''.join([
        k for k, v in arguments.items() if v is True
    ])
    res = requests.get(url, verify=False)
    data = res.json()['data']
    TrainsCollection(data, options).pretty_print()


if __name__ == '__main__':
    cli()
