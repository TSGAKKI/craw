
import urllib
import urllib.request
import urllib.request, urllib.parse
from urllib.request import urlopen  # 用于获取网页
import http.cookiejar
import requests
from bs4 import BeautifulSoup


# -*- coding: UTF-8 -*-

errorCount = 0  # 失败次数
failCount = 0  # 爬取失败次数
successCount = 0  # 保存成功次数

target = 'https://db.yaozh.com/pijian?p=3'
member = 'https://www.yaozh.com/member/'
target1 = 'https://db.yaozh.com'


class GetUserListByBS4():

    def html_text(self):

        url = 'https://www.yaozh.com/login'

        # 构造登陆请求
        req = urllib.request.Request(url, headers=headers, data=post_data)

        # cookie
        cookie = http.cookiejar.CookieJar()

        # 构造一个opener携带登录后的cookie
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

        # 发送登陆请求
        resp = opener.open(req)

        print(resp)

        # 登录后个人中心
        url = target

        # 构造访问请求
        req = urllib.request.Request(url, headers=headers)

        resp = opener.open(req).read().decode('utf-8')

        return opener, resp
        # print(resp)
    # def get(self,url,coding):
    #
    def __init__(self):
        '''
        Constructor
        '''

    def start(self):
        hrefdata = []
        # html = hospitalGet.get(target, "utf-8")
        result = hospitalGet.html_text()
        html = result[1]
        # print(html)
        # html = hospitalGet.get(target + "ZpaRamQyNTEzZQ==.html" ,"utf-8")
        soup = BeautifulSoup(html, "html5lib")
        table = soup.find(name='table', class_="table").find(name='tbody')
        if table:
            hospital = table.find_all(name='tr')
            if hospital:
                for each in hospital:
                    hrefdata.append(each.find(name='a')['href'])

        for item in hrefdata:
            url = (target1 + str(item))
            req = urllib.request.Request(url, headers=headers)
            opener = result[0]
            resp = opener.open(req).read().decode('utf-8')
            soup = BeautifulSoup(resp, "html5lib")
            table = soup.find(name='table', class_="table")
            if table:
                hospital = table.find_all(name='tr')
                if hospital:
                    for each in hospital:
                        hospitalTitle = each.find(name='span').get_text().strip()
                        print(hospitalTitle.split(" ")[-1])
            print("-----" + str(1) + "--------")


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
    hospitalGet = GetUserListByBS4()
    hospitalGet.start()
