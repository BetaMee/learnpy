def str_to_dict(headers):
    """
    将"Host: mp.weixin.qq.com"格式的字符串转换成字典类型
    转换成字典类型
    :param headers: str
    :return: dict
    """
    headers = headers.split("\n")
    d_headers = dict()
    for h in headers:
        h = h.strip()
        if h:
            k, v = h.split(":", 1) # 分割字符串，第二参数是分割次数，这里只分割一次
            d_headers[k] = v.strip() # strip方法移除空格
    return d_headers