# coding:utf-8

"""
Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -d          动车
    -g          高铁
    -t          特快
    -k          快速
    -z          直达

Example:
    main 珠海 广州 2016-11-25
    main -gd 广州 北京 2016-11-26
"""

import re
from pprint import pprint
import requests
from docopt import docopt
from prettytable import PrettyTable
from colorama import init,Fore

from stations import stations

init()

class TrainsCollection:
    header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split(' ')

    def __init__(self,available_trains,options):
        self.available_trains = available_trains
        self.options = options

    #对历时的格式进行修改
    def _get_duration(self,raw_train):
        duration = raw_train.get('lishi').replace(':','小时') + '分'

        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    #根据原始数据返回处理好后的数据
    #生成器
    @property
    def trains(self):
        for raw_train in self.available_trains:
            train_number = raw_train['station_train_code']
            first_letter = train_number[0].lower()
            #要考虑没有填写选项的情况
            if not self.options or first_letter in self.options:
                train = [
                    train_number,
                    '\n'.join([Fore.GREEN + raw_train['from_station_name'] + Fore.RESET,Fore.RED + raw_train['to_station_name'] + Fore.RESET]),
                    '\n'.join([Fore.GREEN + raw_train['start_time'] + Fore.RESET,Fore.RED + raw_train['arrive_time'] + Fore.RESET]),
                    self._get_duration(raw_train),
                    raw_train['zy_num'],
                    raw_train['ze_num'],
                    raw_train['rw_num'],
                    raw_train['yw_num'],
                    raw_train['yz_num'],
                    raw_train['wz_num'],
                ]
                yield train

    def pretty_print(self):
        #表格
        pt = PrettyTable()
        #表头
        pt._set_field_names(self.header)
        #加入数据
        for train_row in self.trains:
            pt.add_row(train_row)
        print(pt)


def cli():

    #获取所有参数
    args = docopt(__doc__)

    #始发站
    from_station = stations.get(args['<from>'])
    #终点站
    to_station = stations.get(args['<to>'])
    #日期
    date = args['<date>']
    #选项
    options = ''.join([key for key,value in args.items() if value is True])

    #构建url
    # url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(date, from_station, to_station)
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate=2016-11-25&from_station=BJP&to_station=SHH'

    #爬取数据
    response = requests.get(url,verify = False)
    #结果为json类型，转换为字典
    response = response.json()
    #提取datas部分的数据
    available_trains = response['data']['datas']


    TrainsCollection(available_trains,options).pretty_print()

if __name__ == '__main__':
    cli()

