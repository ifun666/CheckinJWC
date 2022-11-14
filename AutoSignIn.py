#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import json
import re
import requests
import time

session = requests.session()  # 对全局进行会话实例化

default_headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://qczj.h5yunban.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://qczj.h5yunban.com/qczj-youth-learning/mine.php',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


def get_resp(method, url, headers=default_headers, timeout=5, **kwargs):
    for i in range(5):  # 最多重试5次
        try:
            response = session.request(method=method, url=url, headers=headers, timeout=timeout, **kwargs)
            if response.status_code == 200:
                return response.text
            else:
                if i == 4:
                    print('【致命错误】接口状态码' + str(response.status_code) + '异常：' + url)
                else:
                    time.sleep(1)
        except:
            if i == 4:
                print('【致命错误】接口连接异常：' + url)
            else:
                time.sleep(1)
    return None


def login():
    while 1 == 1:
        resp = get_resp('get', 'https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/login/we-chat/callback?callback=https%3A%2F%2Fqczj.h5yunban.com%2Fqczj-youth-learning%2Findex.php&scope=snsapi_userinfo&appid=wx56b888a1409a2920&openid=oO-a2txk3nyyiH81nkIUBiT6ZcSU&nickname=%25E6%259A%2597%25E9%25BB%2591%25E5%2590%258C%25E5%25AD%25A6&headimg=https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FVic3gRhvkNpgH3YHHiaO4IWk6zS6MicicaVgw3OxpiaFG6qtUhWsdrKZ5kDsiclDKFC9JO3L46mLSibAHrWpic7p3S4JdA%2F132&time=1668410297&source=common&sign=EF360516BBB0EBC9CBA6240419115FE3&t=1668410297')
        print(resp)
        accessToken = re.findall(r"'accessToken', '(.*?)'|$", str(resp))[0]
        if accessToken != '':
            print('登陆成功')
            return accessToken
        time.sleep(3)


def islogin(resp):
    if 'login-typetip' in resp:
        print('\n登录态失效，正在重新登陆！')
        login()
        return
    else:
        return


def main():
    print("\n===============程序信息===============")
    print("程序名称：青春浙江每日签到")
    print("程序作者：浙中医的Richard同学")
    print("更新时间：2022年11月8日")
    print("程序版本：1.2.0_Beta")
    print("===============信息结束===============")

    accessToken = login()

    params = {
        'accessToken': accessToken,
    }
    json_data = {}
    resp = get_resp('post', 'https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/sign-in', params=params, json=json_data)
    print(resp)

    params = {
        'pageSize': '10',
        'pageNum': '1',
        'type': '百年风华正青春',
        'desc': 'startTime',
        'pid': 'C0096',
    }
    list_resp = get_resp('get', 'https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/list', params=params)
    list_json = json.loads(list_resp)
    for item in list_json['result']['list']:
        # print(item['uriType'])
        params = {
            'accessToken': accessToken,
            'id': item['id'],
        }
        json_data = {}
        resp = get_resp('post', 'https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/course/study', params=params, json=json_data)
        print(resp)



if __name__ == '__main__':
    main()
