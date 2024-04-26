#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
# sys.path.append('D:\work\vscode\mycode\devPython\python\free')
import time

from filter_github import downloader_use_proxy


# 根据语言查询
def get_info(language, page, pre_page):
    url = "https://api.github.com/search/repositories?q=language:%s&sort=stars&order=desc&page=%s&per_page=%s" % (
    language, page, pre_page)
    r = downloader_use_proxy(url)
    return r


a = get_info('python', str(1), str(1))
# print(a)
total_count = a['total_count']
page_size = 100
page_number = 1
#比较好的翻页方法
while page_size * (page_number - 1) <= total_count:
    # print(page_number)
    b = get_info('python', page_number, page_size)
    time.sleep(0.2)
    page_number += 1
    for n in b['items']:
        uurl = n['owner']['url']
        repo = n['owner']['html_url']
        print("用户连接: "+uurl)
        r = downloader_use_proxy(uurl)
        d = r
        # print(d)
        if d['location'] is None:
            continue
        elif d['email'] is None:
            d['email'] = "None"
        else:
            e = d['location'].lower()
            if "china" in e:
                print("项目:" + repo)
                print("姓名:" + d['name'])
                print("博客:" + d['blog'])
                print("邮箱:" + d['email'])
