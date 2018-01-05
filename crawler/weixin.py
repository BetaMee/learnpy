# -*- coding: utf-8 -*-
__author__ = "gongxiangqian"

import requests

def headers_to_dict(headers):
    """
    将字符串
    '''
    Host: mp.weixin.qq.com
    Connection: keep-alive
    Cache-Control: max-age=
    '''
    转换成字典类型
    :param headers: str
    :return: dict
    """
    headers = headers.split("\n")
    d_headers = dict()
    for h in headers:
        h = h.strip()
        if h:
            k, v = h.split(":", 1)
            d_headers[k] = v.strip()
    return d_headers

def extract_data(html_content):
    """
    从html页面中提取历史文章数据
    :param html_content 页面源代码
    :return: 历史文章列表
    """
    import re
    import html
    import json

    rex = "msgList = '({.*?})'"
    pattern = re.compile(pattern=rex, flags=re.S)
    match = pattern.search(html_content)
    if match:
        data = match.group(1)
        data = html.unescape(data)
        data = json.loads(data)
        articles = data.get("list")
        # for item in articles:
        #     print(item)
        return articles

# v0.1
def crawl():
    url = "https://mp.weixin.qq.com/mp/profile_ext" \
      "?action=home" \
      "&__biz=MzA5NDc1NzQ4MA==" \
      "&scene=124" \
      "&devicetype=iOS11.2.1" \
      "&version=16060120" \
      "&lang=zh_CN" \
      "&nettype=WIFI" \
      "&a8scene=3" \
      "&fontScale=100" \
      "&pass_ticket=kM7Us0OCNb%2FL1%2FAMPi7VzZrVqz2V9f5e2cPDyMr1ycFMlSS8Li6bIgSGlN3sx%2FyH" \
      "&wx_header=1" \

    headers = """
    Host: mp.weixin.qq.com
    Cookie: devicetype=iOS11.2.1; lang=zh_CN; pass_ticket=kM7Us0OCNb/L1/AMPi7VzZrVqz2V9f5e2cPDyMr1ycFMlSS8Li6bIgSGlN3sx/yH; version=16060120; wap_sid2=CLzPvfkEEogBd1BqWV9PSmpYdlhFaHpsUDVuTTdqYnVXRkt2dFlHc3F0U1p6UGZDZEJVY0JqQ2hHd0N4aFdZTEgyZlJfZS1uZEU5Njd1NUV1a2J4bGhmWUVfNTd6MEJodjN0emNnRm5VZ1k1eVUxS0tXaEY4eC1kOU5fWldSWlRmeDdrZkpySFZxUU1BQUF+fjCS9Z7SBTgNQJVO; wxuin=1328506812; wxtokenkey=bdddea93fcc8bc4d3ddabb59e827e937625841f1918ae245450622ff8f3bd362; rewardsn=77b3d521e82b23a83550; pgv_pvid=6280301858; _scan_has_moon=1; eas_sid=Q1g5I1q201w0y4d0o2W5z3N4j4; _ga=GA1.2.557769603.1510924852; pac_uid=0_64f45f141b0a7; sd_cookie_crttime=1508507376988; sd_userid=58871508507376987
    X-WECHAT-KEY: c5a4b5f1117b495aceef138df25145034f4542969ca0c5295004d4e7822cea1295e9411d39da5f616254387c633ab4d36b8f0799e057e47688b35a88d22a55a628ce4af637369264b5892f762419f957
    X-WECHAT-UIN: MTMyODUwNjgxMg%3D%3D
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C153 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN
    Accept-Language: zh-cn
    Accept-Encoding: br, gzip, deflate
    Connection: keep-alive
    """
    headers = headers_to_dict(headers)
    response = requests.get(url, headers=headers, verify=False)

    if '<title>验证</title>' in response.text:
        raise Exception("获取微信公众号文章失败，可能是因为你的请求参数有误，请重新获取")
    data = extract_data(response.text)
    for item in data:
        print(item)
    # 保存
    with open("weixin_history.html", "w", encoding="utf-8") as f:
      f.write(response.text)

    

if __name__ == '__main__':
    crawl()


