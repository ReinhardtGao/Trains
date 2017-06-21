import re
import requests
from pprint import pprint

url = 'https://kyfw.railway_inquiry.cn/otn/resources/js/framework/station_name.js?station_version=1.9015'
response = requests.get(url, verify=False)
station = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
pprint(dict(station), indent=4)
