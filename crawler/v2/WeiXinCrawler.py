# WeiXinCrawler.py
# -*- coding: utf-8 -*-

import logging
import time
import utils
import requests

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class WeiXinCrawler:

  def crawl(self, offset=0):
    """
    爬取更多文章
    :return:
    """
    url = "https://mp.weixin.qq.com/mp/profile_ext"\
          "?action=getmsg" \
          "&__biz=MjM5MTY3OTYyMQ==" \
          "&f=json"\
          "&offset=10"\
          "&count=10"\
          "&is_ok=1"\
          "&scene=124"\
          "&uin=777"\
          "&key=777"\
          "&pass_ticket=wj2j8pp2XnstT6wupUoiIxRoY2JjT3FOCEPXdBYhs7CPwSzfTIogmELiy3YZ4mRs"\
          "&wxtoken="\
          "&appmsg_token=938_DJXrTDktnbNkCkp3oOCg-lVbWhhbemMp0EkBLA~~"\
          "&x5=0"\
          "&f=json"

    headers = """
    Host: mp.weixin.qq.com
    Accept-Encoding: br, gzip, deflate
    Cookie: devicetype=iOS11.2.1; lang=zh_CN; pass_ticket=wj2j8pp2XnstT6wupUoiIxRoY2JjT3FOCEPXdBYhs7CPwSzfTIogmELiy3YZ4mRs; version=16060124; wap_sid2=CLzPvfkEEnBnRTdYc3Uxa1B4NzcxdUR3T3pyNEUwYVBRb09SQlk0MWk1bTVkdVdkUlpSdTh4QUExdWNVYkVxLTN0NnVVWVZhYk5VRXJCT1hpSmI1N0FCaDNmVURBclVSSlhOcDZXZDNpTXJPZkQ0NVd1S3FBd0FBMJ3S1tIFOAxAlE4=; wxuin=1328506812; wxtokenkey=f9b3cef513031f0f50b8c9d88862ea0a8e44ae03f2dabb3e1e7d6b6f68c2233c; bk_token=fc1a7e18-e120-4f0a-a419-e1650f99b989; is_login=wx; is_wechat=1; platform=qq; pgv_pvid=6280301858; _scan_has_moon=1; eas_sid=Q1g5I1q201w0y4d0o2W5z3N4j4; _ga=GA1.2.557769603.1510924852; pac_uid=0_64f45f141b0a7; sd_cookie_crttime=1508507376988; sd_userid=58871508507376987
    Connection: keep-alive
    Accept: */*
    User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C153 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN
    Referer: https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MTY3OTYyMQ==&scene=124&devicetype=iOS11.2.1&version=16060124&lang=zh_CN&nettype=WIFI&a8scene=3&fontScale=100&pass_ticket=wj2j8pp2XnstT6wupUoiIxRoY2JjT3FOCEPXdBYhs7CPwSzfTIogmELiy3YZ4mRs&wx_header=1
    Accept-Language: zh-cn
    X-Requested-With: XMLHttpRequest
    """
    
    
    headers = utils.str_to_dict(headers)
    response = requests.get(url, headers=headers, verify=False)
    result = response.json()

    if result.get("ret") == 0:
        msg_list = result.get("general_msg_list")
        logger.info("抓取数据：offset=%s, data=%s" % (offset, msg_list))
         # 递归调用
        has_next = result.get("can_msg_continue")
        if has_next == 1:
            next_offset = result.get("next_offset")
            time.sleep(2)
            self.crawl(next_offset)
    else:
        # 错误消息
        # {"ret":-3,"errmsg":"no session","cookie_count":1}
        logger.error("无法正确获取内容，请重新从Fiddler获取请求参数和请求头")
        exit()


if __name__ == '__main__':
    crawler = WeiXinCrawler()
    crawler.crawl()