# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-14 14:12:40
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-14 14:47:18

import re
import requests
from bs4 import BeautifulSoup


def queryIpAddress(ipaddress):
    try:
        reaponse = requests.get("https://ip.cn/index.php?ip={}".format(ipaddress))
        soup = BeautifulSoup(reaponse.content, 'lxml')
        a = soup.find('div', attrs={'class': 'well'})
        address = a.find_all('code')[1].text

        # 以上4行代码是获取中文的地理位置
        # reaponse = requests.get("https://ip.cn/index.php?ip={}".format(ipaddress), timeout=10)
        # soup = BeautifulSoup(reaponse.content, 'lxml')

        # a = soup.find('div', attrs={'class': 'well'})
        # b = a.find_all('p')[3].text
        # address = b.replace("GeoIP: ", "")

        # 以上返回 英文或拼音的地理位置
        return address
    except:
        return 'get filed.'


def main():
    with open('file-server.py.log', 'rb') as fi:
        # L =
        while True:
            line = fi.readline()
            if not line:
                break
            if line.startswith(b'Connect from'):
                print(fi.readline().decode().strip())
                IP = re.findall(b"Connect from \('(.*)',", line)[0]
                print(IP.decode())
                s = queryIpAddress(IP.decode())
                print(s+'\n')

if __name__ == '__main__':
    main()
