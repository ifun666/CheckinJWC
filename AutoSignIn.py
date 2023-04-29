#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import requests
import json
import yaml
import time

getToken_url = 'https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/login/we-chat/callback'
getUserInfo_url = 'https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/course/last-info'
getClass_url = 'https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current'
checkin_url = 'https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/course/join'

headers = {
    'Content-Type': 'text/plain'
}

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


def getYmlConfig(yaml_file='config.yml'):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        file_data = f.read()
    return dict(yaml.load(file_data, Loader=yaml.FullLoader))


def getToken(openId):
    # 根据openId获得token
    try:
        token = requests.get(url=getToken_url, params=openId, headers=headers)
        Token_raw = token.text
        Token = re.findall('[A-Z0-9]{8}[-][A-Z0-9]{4}[-][A-Z0-9]{4}[-][A-Z0-9]{4}[-][A-Z0-9]{12}', Token_raw)[0]
        print('获取到Token为：' + Token)
        return Token
    except:
        print('【致命错误】获取Token失败，请检查openId是否正确！')


def getinfo(accessToken):
    # 根据accessToken获得用户信息
    try:
        getUserInfo = requests.get(getUserInfo_url, params=accessToken, headers=headers)
        userInfo = getUserInfo.json()
        cardNo = userInfo["result"]["cardNo"]
        nid = userInfo["result"]["nid"]
        getClass = requests.get(getClass_url, params=accessToken, headers=headers)
        Class = getClass.json()
        classId = Class["result"]["id"]
        classTitle = Class["result"]["title"]
        infos: list = userInfo['result']['nodes']
        Faculty = [item['title'] for item in infos]
        print('本期大学习的课程编码：' + classId + '\n本期大学习的课程名称：' + classTitle + '\n系统中的个人信息为：' + cardNo + '\n您的签到所属组织为：' + str(Faculty))
        checkinData = {
            'course': classId,
            'subOrg': None,
            'nid': nid,
            'cardNo': cardNo
        }
        return checkinData
    except Exception as e:
        if "is not subscriptable" in str(e):
            print("【致命错误】openId出错,无法获得您的信息！")
        print(f'【致命错误】获取历史信息失败，请您手动打卡：{e}')


def signup(accessToken, checkinData):
    # 根据token和data完成打卡
    checkin = requests.post(checkin_url, params=accessToken, data=json.dumps(checkinData), headers=headers)
    result = checkin.json()
    if result["status"] == 200:
        print("成功完成本次青年大学习！")
        return 1
    else:
        print('【致命错误】出现错误，错误码：' + str(result["status"]))
        print('【致命错误】错误信息：' + str(result["message"]))
        return result["message"]


if __name__ == "__main__":
    print("\n===============程序信息===============")
    print("程序名称：浙江青年大学习部署到Action一键打卡")
    print("程序作者：lthero-big & 浙中医的Richard同学")
    print("更新时间：2022年11月20日")
    print("程序版本：1.0.0_Beta")
    print("===============信息结束===============")
    config = getYmlConfig()
    for index, eachuser in enumerate(config['users']):
        print("\n===============单次开始===============")
        print(eachuser['user']['name'] + 'openId为：' + eachuser['user']['openid'])
        openid = {
            'appid': 'wx56b888a1409a2920',
            'openid': eachuser['user']['openid']
        }
        accessToken = getToken(openid)

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

        print("===============单次结束===============")
        time.sleep(3)
