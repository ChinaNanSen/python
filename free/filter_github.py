# !/usr/bin/python3
# @Readme : 反爬之headers的伪装
# 对于检测Headers的反爬虫

import requests
from fake_useragent import UserAgent
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_proxy_ip():
    api = "http://39.103.185.241:44567/api/v1.0/get-one-proxy-ip"  #这个是IP代理连接池
    while True:
        try:
            r = requests.get(api, timeout=10)
            if r.status_code == 200:
                proxy = {"http": f"http://{r.text}"}
                print(proxy)
                return proxy
            else:
                print(f"\nHTTP状态码报错：{r.status_code}\n重新获取IP代理...\n")
                continue
        except Exception as e:
            print(f"\n获取IP代理报错：{e}\n重新获取IP代理...\n")
            continue



def downloader_use_proxy(url):
    #github 个人token，谨慎不要泄露
    access_token = "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"
    while True:
        proxies = get_proxy_ip()
        try:
            r = requests.get(url, headers={'User-Agent': UserAgent().random, 'Authorization': 'token ' + access_token},
                             proxies=proxies, verify=False, timeout=10)
            if r.status_code == 200:
                return r.json()
            else:
                print(r.text)
                print(f"http状态码报错：{r.status_code}，重新获取代理ip...\n")
                continue
        except Exception as e:
            print(f"报错：{e}\n重新获取代理ip...\n")
            continue


