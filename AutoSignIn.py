#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import json
import re
import requests
import time
from urllib.parse import quote

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

def get_text(txt_name):
    last_resp = get_resp('get', 'https://api.txttool.cn/txtpad/txt/detail/?password=&txt_name=' + txt_name)
    resp_json = json.loads(last_resp)
    if resp_json["status"] == 1:
        txt_content = resp_json["data"]['txt_content']
        txt_content_json = json.loads(txt_content)
        return txt_content_json[0]['content']
    else:
        return None


def save_text(txt_name, txt_content):
    resp = get_resp('get', 'https://api.txttool.cn/txtpad/txt/detail/?password=&txt_name=' + txt_name)
    resp_json = json.loads(resp)
    if resp_json["status"] == 1:
        v_id = resp_json["data"]['v_id']
    else:
        return None
    data = {
        'txt_name': txt_name,
        'txt_content': '[{"title":"0","content":"' + txt_content + '"}]',
        'password': '',
        'v_id': v_id,
    }
    last_resp = get_resp('post', 'https://api.txttool.cn/txtpad/txt/save/', data=data)
    resp_json = json.loads(last_resp)
    if resp_json["status"] == 1:
        return True
    else:
        return None


def main():
    print("\n===============程序信息===============")
    print("程序名称：教务处通知")
    print("程序作者：浙中医的Richard同学")
    print("更新时间：2022年9月8日")
    print("程序版本：1.2.0_Beta")
    print("===============信息结束===============")
    isupdate = 0
    last = get_text('zcmujwxx')
    resp = get_resp('get', 'https://portal.paas.zcmu.edu.cn/portal-api/v3/cms/content/getColumncontents?kw=&columnId=remote-acc34940-f1ed-46b9-bfd2-1c3e518574fa&pageNo=1&pageSize=20&loadContent=false&loadPicContents=true')
    resp_json = json.loads(resp)
    wzlist = resp_json['data']['allContents']
    for wz in wzlist:
        wzid = wz['id']
        wzurl = wz['url']
        wztitle = wz['title']
        if isupdate == 0:
            save_text('zcmujwxx', wzid)
            isupdate =1
        if wzid == last:
            break
        print(wztitle)
        if "content.jsp" in wzurl:
            description = "本消息需要登陆查看，暂无内容简介"
        else:
            resp = get_resp('get', wzurl)
            description = re.findall(r'<META Name="description" Content="(.*?)" />|$', resp)[0]
        wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
        wx_content = '【教务处】教务处官网发布了《' + wztitle + '》，详情请看：' + wzurl + '\n\n内容简介：' + description
        send_wx_message(wx_url, wx_content)

    isupdate = 0
    last = get_text('zcmutzgg')
    resp = get_resp('get', 'https://dylc.zcmu.edu.cn/xwdt/tzgg.htm')
    wzlist = re.findall(r'<li id=".*?"><a href="../(.*?)">(.*?)</a><i>.*?</i></li>', resp)
    for wz in wzlist:
        wzurl = wz[0]
        wztitle = wz[1]
        if isupdate == 0:
            save_text('zcmutzgg', quote(wztitle))
            isupdate = 1
        if quote(wztitle) == last:
            break
        print(wztitle)
        if "content.jsp" in wzurl:
            description = "本消息需要登陆查看，暂无内容简介"
        else:
            resp = get_resp('get', 'https://dylc.zcmu.edu.cn/' + wzurl)
            description = re.findall(r'<META Name="description" Content="(.*?)" />|$', resp)[0]
        wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
        wx_content = '【第一临床医学院】学院官网在『通知公告』栏目发布了《' + wztitle + '》，详情请看：https://dylc.zcmu.edu.cn/' + wzurl + '\n\n内容简介：' + description
        send_wx_message(wx_url, wx_content)

    isupdate = 0
    last = get_text('zcmujxgz')
    resp = get_resp('get', 'https://dylc.zcmu.edu.cn/jxgz.htm')
    wzlist = re.findall(r'<li id=".*?"><a href="(.*?)">(.*?)</a><i>.*?</i></li>', resp)
    for wz in wzlist:
        wzurl = wz[0]
        wztitle = wz[1]
        if isupdate == 0:
            save_text('zcmujxgz', quote(wztitle))
            isupdate = 1
        if quote(wztitle) == last:
            break
        print(wztitle)
        if "content.jsp" in wzurl:
            description = "本消息需要登陆查看，暂无内容简介"
        else:
            resp = get_resp('get', 'https://dylc.zcmu.edu.cn/' + wzurl)
            description = re.findall(r'<META Name="description" Content="(.*?)" />|$', resp)[0]
        wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
        wx_content = '【第一临床医学院】学院官网在『教学工作』栏目发布了《' + wztitle + '》，详情请看：https://dylc.zcmu.edu.cn/' + wzurl + '\n\n内容简介：' + description
        send_wx_message(wx_url, wx_content)


    print("===============信息更新完毕===============")




if __name__ == '__main__':
    main()
