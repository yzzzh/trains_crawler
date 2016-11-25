# -*- coding: utf8 -*-
import re
from pprint import pprint
import requests

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971'

#返回值是requests类，需要调用.text转换为文本
response = requests.get(url,verify = False)
#使用正则表达式转化为多个元组对
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)',response.text)
#使用pprint是为了每个元祖自动换行
pprint(dict(stations),indent=4)