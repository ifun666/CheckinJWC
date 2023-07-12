#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import json
import re
import requests
import time

session = requests.session()  # 对全局进行会话实例化
default_headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Referer': 'http://jwmk.zcmu.edu.cn/jwglxt/xtgl/',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


def get_resp(method, url, headers=default_headers, timeout=60, **kwargs):
    for i in range(5):  # 最多重试5次
        try:
            response = session.request(method=method, url=url, headers=headers, timeout=timeout, **kwargs)
            if response.status_code == 200:
                response.encoding = 'utf-8'
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

def send_wx_message(webhook, content):
    for i in range(5):  # 最多重试5次
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            data = {
                'msgtype': 'text',
                'text': {
                    'content': content
                }
            }
            response = requests.post(webhook, headers=headers, data=json.dumps(data))
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

def main():
    print("\n===============程序信息===============")
    print("程序名称：教务处通知")
    print("程序作者：浙中医的Richard同学")
    print("更新时间：2022年9月8日")
    print("程序版本：1.2.0_Beta")
    print("===============信息结束===============")
    isupdate = 0
    resp = get_resp('get', 'https://jwc.zcmu.edu.cn/jwgl.htm')
    last_resp = get_resp('get', 'https://www.canpointgz.cn/cj/text.php?method=read&textid=jwgl')
    resp_json = json.loads(last_resp)
    last = resp_json["textcontent"]
    wzlist = re.findall(r'<a class=".*?" href="(.*?)" target="_blank" title="(.*?)">', resp)
    for wz in wzlist:
        wzurl = wz[0]
        wztitle = wz[1]
        if isupdate == 0:
            resp = get_resp('get', 'https://www.canpointgz.cn/cj/text.php?method=edit&textid=jwgl&textcontent=' + wztitle)
            isupdate =1
        if wztitle == last:
            break
        print(wztitle)
        if "content.jsp" in wzurl:
            description = "本消息需要登陆查看，暂无内容简介"
        else:
            resp = get_resp('get', 'https://jwc.zcmu.edu.cn/' + wzurl)
            description = re.findall(r'<META Name="description" Content="(.*?)" />|$', resp)[0]
        wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
        wx_content = '【教务处】教务处官网在『教务管理』栏目发布了《' + wztitle + '》，详情请看：https://jwc.zcmu.edu.cn/' + wzurl + '\n\n内容简介：' + description
        send_wx_message(wx_url, wx_content)

    isupdate = 0
    resp = get_resp('get', 'https://jwc.zcmu.edu.cn/jxjs.htm')
    last_resp = get_resp('get', 'https://www.canpointgz.cn/cj/text.php?method=read&textid=jxjs')
    resp_json = json.loads(last_resp)
    last = resp_json["textcontent"]
    wzlist = re.findall(r'<a class=".*?" href="(.*?)" target="_blank" title="(.*?)">', resp)
    for wz in wzlist:
        wzurl = wz[0]
        wztitle = wz[1]
        if isupdate == 0:
            resp = get_resp('get', 'https://www.canpointgz.cn/cj/text.php?method=edit&textid=jxjs&textcontent=' + wztitle)
            isupdate = 1
        if wztitle == last:
            break
        print(wztitle)
        if "content.jsp" in wzurl:
            description = "本消息需要登陆查看，暂无内容简介"
        else:
            resp = get_resp('get', 'https://jwc.zcmu.edu.cn/' + wzurl)
            description = re.findall(r'<META Name="description" Content="(.*?)" />|$', resp)[0]
        wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
        wx_content = '【教务处】教务处官网在『教学建设』栏目发布了《' + wztitle + '》，详情请看：https://jwc.zcmu.edu.cn/' + wzurl + '\n\n内容简介：' + description
        send_wx_message(wx_url, wx_content)

    isupdate = 0
    resp = get_resp('get', 'https://jwc.zcmu.edu.cn/sjjx.htm')
    last_resp = get_resp('get', 'https://www.canpointgz.cn/cj/text.php?method=read&textid=sjjx')
    resp_json = json.loads(last_resp)
    last = resp_json["textcontent"]
    wzlist = re.findall(r'<a class=".*?" href="(.*?)" target="_blank" title="(.*?)">', resp)
    for wz in wzlist:
        wzurl = wz[0]
        wztitle = wz[1]
        if isupdate == 0:
            resp = get_resp('get', 'https://www.canpointgz.cn/cj/text.php?method=edit&textid=sjjx&textcontent=' + wztitle)
            isupdate = 1
        if wztitle == last:
            break
        print(wztitle)
        if "content.jsp" in wzurl:
            description = "本消息需要登陆查看，暂无内容简介"
        else:
            resp = get_resp('get', 'https://jwc.zcmu.edu.cn/' + wzurl)
            description = re.findall(r'<META Name="description" Content="(.*?)" />|$', resp)[0]
        wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
        wx_content = '【教务处】教务处官网在『实践教学』栏目发布了《' + wztitle + '》，详情请看：https://jwc.zcmu.edu.cn/' + wzurl + '\n\n内容简介：' + description
        send_wx_message(wx_url, wx_content)





if __name__ == '__main__':
    main()
