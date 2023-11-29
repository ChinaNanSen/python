import requests
import json

def main():
    # Prometheus API URL
    prometheus_url = 'http://prometheus.prod.vevor.net/api/v1/query'

    # 构造查询字符串
    query_strings = [
        # 'mem_used_percent{ident=~"crp-dms.*"} >= 10'
        'mem_used_percent{ident=~"crp-.*|cop-.*"} >= 90',
        '100 - cpu_usage_idle{ident=~"crp.*|cop.*",cpu="cpu-total"} >= 90'
    ]

    unique_idents = []

    for query_string in query_strings:
        # 查询参数
        query = {'query': query_string}

        # 发送 GET 请求
        response = requests.get(prometheus_url, params=query)
        

        # 解析响应
        if response.status_code == 200:
            data = response.json()
            # print(data)
            process_data_and_add_to_set(data, unique_idents)

    # 生成 URL
    # print(unique_idents)
    urls = generate_urls(unique_idents)
    for url in urls:
        # print(url)
        # 这里可以添加对 URL 的请求逻辑，例如 POST 请求
        nres = requests.post(url)
        if nres.status_code == 200:
            print("ok")
        else:
            print("fail")

def process_data_and_add_to_set(data, unique_idents):
    """ 处理 Prometheus 数据并添加 ident 到集合 """
    for item in data['data']['result']:
        ident_full = item['metric']['ident']
        # 分割 ident 并获取前两部分，然后用 '-' 连接
        # ident_parts = ident_full.split('-', 2)
        ident_required = ident_full

        # 添加到集合中以去重
        unique_idents.append(ident_required)

def generate_urls(unique_idents):
    """ 为每个唯一的 ident 生成 URL """
    # 提供的字典
    ident_dictionary = {
  "cop-application-portal": [
    "cop-application-portal-ecs-p001.shl.vevor.net",
    "cop-application-portal-ecs-p002.shl.vevor.net"
  ],
  "cop-data-process": [
    "cop-data-process-ecs-p001.shl.vevor.net",
    "cop-data-process-ecs-p002.shl.vevor.net"
  ],
  "cop-data-extract": [
    "cop-data-extract-ecs-p001.shL.vevor.net",
    "cop-data-extract-ecs-p002.shL.vevor.net"
  ],
  "cop-data-monitor": [
    "cop-data-monitor-ecs-p001.shl.vevor.net",
    "cop-data-monitor-ecs-p002.shL.vevor.net"
  ],
  "cop-dct": [
    "cop-dct-ecs-p001.shL.vevor.net",
    "cop-dct-ecs-p002.shL.vevor.net"
  ],
  "cop-application-open": [
    "cop-application-open-ecs-p001.shL.vevor.net",
    "cop-application-open-ecs-p002.shL.vevor.net"
  ],
  "cop-auth-proxy-channel": [
    "cop-auth-proxy-channel-p001.apE.vevor.net",
    "cop-auth-proxy-channel-p002.apE.vevor.net"
  ],
  "crp-analysis": [
    "crp-analysis-ecs-p001.shL.vevor.net",
    "crp-analysis-ecs-p002.shL.vevor.net"
  ],
  "crp-collector": [
    "crp-collector-ecs-p001.shL.vevor.net",
    "crp-collector-ecs-p002.shL.vevor.net"
  ],
  "crp-dms": [
    "crp-dms-ecs-p001.shL.vevor.net",
    "crp-dms-ecs-p002.shL.vevor.net"
  ],
  "crp-data-portal": [
    "crp-data-portal-ecs-p001.shL.vevor.net",
    "crp-data-portal-ecs-p002.shL.vevor.net"
  ],
  "crp-collector-admin": [
    "crp-collector-admin-ecs-p001.shl.vevor.net",
    "crp-collector-admin-ecs-p002.shl.vevor.net"
  ],
  "crp-component-admin": [
    "crp-component-admin-ecs-p001.shL.vevor.net"
  ]
}

    # 生成 URL
    urls = []
    for ident in unique_idents:
        # print(ident)
        # 检查 ident 是否在字典中，并获取对应的 key
        key = find_key_in_dict(ident, ident_dictionary)
        # print(key)
        if key:
            url = f"http://n9e-jmap.vevor.net/alert?ident={key}"
            urls.append(url)
    return set(urls)

def find_key_in_dict(ident, ident_dictionary):
    """ 在字典中查找 ident 对应的 key """
    for key, idents in ident_dictionary.items():
        if ident in idents:
            return key
    return None

if __name__ == "__main__":
    main()
