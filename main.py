import random
import urllib
import urllib.request
import urllib.request, urllib.parse
from urllib.request import urlopen  # 用于获取网页
import http.cookiejar
import requests
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread

# -*- coding: UTF-8 -*-

errorCount = 0  # 失败次数
failCount = 0  # 爬取失败次数
successCount = 0  # 保存成功次数

target = 'https://db.yaozh.com/pijian?p='
member = 'https://www.yaozh.com/member/'
target1 = 'https://db.yaozh.com'


class GetDataListByBS4(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self) :
        for i in range(10):
            hrefdata = []
            # 构造访问请求
            req = urllib.request.Request(target+str(i), headers=headers)
            html = opener.open(req).read().decode('utf-8')
            # print(html)
            soup = BeautifulSoup(html, "html5lib")
            table = soup.find(name='table', class_="table").find(name='tbody')
            if table:
                hospital = table.find_all(name='tr')
                if hospital:
                    for each in hospital:
                        url = each.find(name='a')['href']
                        self.queue.put(url)

class GetmedicineInfo(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self) :
        while True:
            medicine_info = ''
            info_url = self.queue.get()
            url = (target1 + str(info_url))
            req = urllib.request.Request(url, headers=headers)
            resp = opener.open(req).read().decode('utf-8')
            soup = BeautifulSoup(resp, "html5lib")
            table = soup.find(name='table', class_="table")
            if table:
                hospital = table.find_all(name='tr')
                if hospital:
                    for each in hospital:
                        hospital = each.find(name='span').get_text().strip()
                        if(len(hospital.split("  "))>1) :

                            info = ''.join(hospital.split("  ")[1:])
                            info = info.replace('\n', '').replace('\t', '')
                            medicine_info += info.strip()+'|'
                            continue
                        medicine_info += hospital + '|'

            print(medicine_info)
            self.queue.task_done()

if __name__ == "__main__":
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'

    # formData数据
    data = {'username': '18342987114',
            'pwd': 'TSLIUlei19891998',
            'formhash': '20117B831C',
            'backurl': 'https%3A%2F%2Fwww.yaozh.com%2F'}

    post_data = urllib.parse.urlencode(data).encode('utf-8')

    # 请求头设置
    headers = {
        'User-Agent': user_agent
    }

    #init opener , create opener with cookie of login
    url = 'https://www.yaozh.com/login'
    # 构造登陆请求
    req = urllib.request.Request(url, headers=headers, data=post_data)
    # cookie
    cookie = http.cookiejar.CookieJar()
    # 构造一个opener携带登录后的cookie
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
    # 发送登陆请求
    resp = opener.open(req)

    #run the thread
    queue = Queue()

    medicine_url_GET = GetDataListByBS4(queue)
    medicine_info_url_GET = GetmedicineInfo(queue)

    medicine_url_GET.start()
    medicine_info_url_GET.start()

    medicine_info_url_GET.join()
    medicine_url_GET.join()
