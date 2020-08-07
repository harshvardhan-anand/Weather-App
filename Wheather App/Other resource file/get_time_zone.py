from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import re
import time

req = urlopen('https://en.wikipedia.org/wiki/List_of_time_zone_abbreviations')
html = req.read()

obj = bs(html,features="lxml")

pattern = r'''<td>(\w+)</td>
<td><(?:\w|\W)+?>((?:\w|\W)+?)<'''
regex = re.compile(pattern)

data = re.findall(regex,str(obj.find('table',{'class':"wikitable sortable"})))

print(data)

time.sleep(100)