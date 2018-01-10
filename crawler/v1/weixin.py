
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
    url = "https://mp.weixin.qq.com/mp/profile_ext"  \
          "?action=home" \
          "&__biz=MjM5MTY3OTYyMQ==" \
          "&scene=124" \
          "&devicetype=iOS11.2.1" \
          "&version=16060124" \
          "&lang=zh_CN" \
          "&nettype=WIFI" \
          "&a8scene=3" \
          "&fontScale=100" \
          "&pass_ticket=wj2j8pp2XnstT6wupUoiIxRoY2JjT3FOCEPXdBYhs7CPwSzfTIogmELiy3YZ4mRs" \
          "&wx_header=1"

    headers = """
    Host: mp.weixin.qq.com
    Cookie: devicetype=iOS11.2.1; lang=zh_CN; pass_ticket=wj2j8pp2XnstT6wupUoiIxRoY2JjT3FOCEPXdBYhs7CPwSzfTIogmELiy3YZ4mRs; version=16060124; wap_sid2=CLzPvfkEEnBnRTdYc3Uxa1B4NzcxdUR3T3pyNEUwYVBRb09SQlk0MWk1bTVkdVdkUlpTdHk3VFRiX1lhZlcyNTNyQ0I1SVFnajFkeEpTUEVucFRuTmVOcHJ1LXFxYkJudlNyTWh2LWRuUGplb2pFNTUyT3FBd0FBMKzP1tIFOA1AAQ==; wxtokenkey=f9b3cef513031f0f50b8c9d88862ea0a8e44ae03f2dabb3e1e7d6b6f68c2233c; wxuin=1328506812; bk_token=fc1a7e18-e120-4f0a-a419-e1650f99b989; is_login=wx; is_wechat=1; platform=qq; pgv_pvid=6280301858; _scan_has_moon=1; eas_sid=Q1g5I1q201w0y4d0o2W5z3N4j4; _ga=GA1.2.557769603.1510924852; pac_uid=0_64f45f141b0a7; sd_cookie_crttime=1508507376988; sd_userid=58871508507376987
    X-WECHAT-KEY: adf81ceca9f731adf0616538f206352254c024fb523c4201c13b897fe415ac1b39358633f4ce3038a0e4f6d76f1a00dad282b120637fab1135bc877cf50cad37a7cd27f3a8d3f8ff1b68b8846f594e23
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


