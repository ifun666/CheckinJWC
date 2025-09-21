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
    last_resp = get_resp('get', 'https://api.textdb.online/' + txt_name)
    return last_resp


def save_text(txt_name, txt_content):
    data = {
        'key': txt_name,
        'value': txt_content,
    }
    last_resp = get_resp('post', 'https://api.textdb.online/update/', data=data)
    resp_json = json.loads(last_resp)
    if resp_json["status"] == 1:
        return True
    else:
        return None


def main():
    print("\n===============程序信息===============")
    print("程序名称：ZCMU多渠道通知监控推送")
    print("程序作者：浙中医的Richard同学")
    print("更新时间：2022年9月8日")
    print("程序版本：1.2.0_Beta")
    print("===============信息结束===============")
    last = get_text('zcmutzgg')
    if last == '':
        last = '{"list": []}'
    last_text = json.loads(last)
    last_list = last_text['list']
    resp = get_resp('get', 'https://dylc.zcmu.edu.cn/xwdt/tzgg.htm')
    wzlist = re.findall(r'<li id=".*?"><a href="../(.*?)">(.*?)</a><i>.*?</i></li>', resp)
    for wz in wzlist:
        wzurl = wz[0]
        wztitle = wz[1]
        if quote(wztitle) in last_list:
            continue
        else:
            print(wztitle)
            wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
            wx_content = '【一临】在『通知公告』栏目发布了《' + wztitle + '》，详情请看：https://dylc.zcmu.edu.cn/' + wzurl
            send_wx_message(wx_url, wx_content)
            last_list.append(quote(wztitle))
    now_text = json.dumps({'list': last_list})
    save_text('zcmutzgg', now_text)

    last = get_text('zcmujxgz')
    if last == '':
        last = '{"list": []}'
    last_text = json.loads(last)
    last_list = last_text['list']
    resp = get_resp('get', 'https://dylc.zcmu.edu.cn/jxgz.htm')
    wzlist = re.findall(r'<li id=".*?"><a href="(.*?)">(.*?)</a><i>.*?</i></li>', resp)
    for wz in wzlist:
        wzurl = wz[0]
        wztitle = wz[1]
        if quote(wztitle) in last_list:
            continue
        else:
            print(wztitle)
            wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
            wx_content = '【一临】在『教学工作』栏目发布了《' + wztitle + '》，详情请看：https://dylc.zcmu.edu.cn/' + wzurl
            send_wx_message(wx_url, wx_content)
            last_list.append(quote(wztitle))
    now_text = json.dumps({'list': last_list})
    save_text('zcmujxgz', now_text)

    last = get_text('zcmujxjs')
    if last == '':
        last = '{"list": []}'
    last_text = json.loads(last)
    last_list = last_text['list']
    resp = get_resp('get', 'https://jwc.zcmu.edu.cn/jxjs.htm')
    wzlist = re.findall(r'<a class=".*?" href="(.*?)" target="_blank" title="(.*?)">', resp)
    for wz in wzlist:
        wzurl = wz[0]
        wztitle = wz[1]
        if quote(wztitle) in last_list:
            continue
        else:
            print(wztitle)
            wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
            wx_content = '【教务处】在『教学建设』栏目发布了《' + wztitle + '》，详情请看：https://jwc.zcmu.edu.cn/' + wzurl
            send_wx_message(wx_url, wx_content)
            last_list.append(quote(wztitle))
    now_text = json.dumps({'list': last_list})
    save_text('zcmujxjs', now_text)

    last = get_text('zcmujwgl')
    if last == '':
        last = '{"list": []}'
    last_text = json.loads(last)
    last_list = last_text['list']
    resp = get_resp('get', 'https://jwc.zcmu.edu.cn/jwgl.htm')
    wzlist = re.findall(r'<a class=".*?" href="(.*?)" target="_blank" title="(.*?)">', resp)
    for wz in wzlist:
        wzurl = wz[0]
        wztitle = wz[1]
        if quote(wztitle) in last_list:
            continue
        else:
            print(wztitle)
            wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
            wx_content = '【教务处】在『教务管理』栏目发布了《' + wztitle + '》，详情请看：https://jwc.zcmu.edu.cn/' + wzurl
            send_wx_message(wx_url, wx_content)
            last_list.append(quote(wztitle))
    now_text = json.dumps({'list': last_list})
    save_text('zcmujwgl', now_text)

    last = get_text('zcmusjjx')
    if last == '':
        last = '{"list": []}'
    last_text = json.loads(last)
    last_list = last_text['list']
    resp = get_resp('get', 'https://jwc.zcmu.edu.cn/sjjx.htm')
    wzlist = re.findall(r'<a class=".*?" href="(.*?)" target="_blank" title="(.*?)">', resp)
    for wz in wzlist:
        wzurl = wz[0]
        wztitle = wz[1]
        if quote(wztitle) in last_list:
            continue
        else:
            print(wztitle)
            wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
            wx_content = '【教务处】在『实践教学』栏目发布了《' + wztitle + '》，详情请看：https://jwc.zcmu.edu.cn/' + wzurl
            send_wx_message(wx_url, wx_content)
            last_list.append(quote(wztitle))
    now_text = json.dumps({'list': last_list})
    save_text('zcmusjjx', now_text)

    last = get_text('zcmuksgl')
    if last == '':
        last = '{"list": []}'
    last_text = json.loads(last)
    last_list = last_text['list']
    resp = get_resp('get', 'https://jwc.zcmu.edu.cn/ksg.htm')
    wzlist = re.findall(r'<a class=".*?" href="(.*?)" target="_blank" title="(.*?)">', resp)
    for wz in wzlist:
        wzurl = wz[0]
        wztitle = wz[1]
        if quote(wztitle) in last_list:
            continue
        else:
            print(wztitle)
            wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
            wx_content = '【教务处】在『考试管理	』栏目发布了《' + wztitle + '》，详情请看：https://jwc.zcmu.edu.cn/' + wzurl
            send_wx_message(wx_url, wx_content)
            last_list.append(quote(wztitle))
    now_text = json.dumps({'list': last_list})
    save_text('zcmuksgl', now_text)

    print('外网即可访问的检测完毕')

    get_ip = get_resp('get', 'https://www.zcmu.edu.cn/system/resource/ip.jsp?owner=1456529787')
    if 'true' in get_ip:
        print('【网络环境检测】当前IP地址处于内网')
        last = get_text('zcmugztz')
        if last == '':
            last = '{"list": []}'
        last_text = json.loads(last)
        last_list = last_text['list']
        resp = get_resp('get',
                        'https://portal.paas.zcmu.edu.cn/portal-api/v3/cms/content/getColumncontents?kw=&columnId=remote-8e9c3ee2-ddc2-41c3-a62f-95207b48cd37&pageNo=1&pageSize=22&loadContent=false&loadPicContents=true')
        resp_json = json.loads(resp)
        wzlist = resp_json['data']['allContents']
        for wz in wzlist:
            wzid = wz['id']
            wzurl = wz['url']
            wztitle = wz['title']
            if wzid in last_list:
                continue
            else:
                print(wztitle)
                wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
                wx_content = '【工作通知】OA系统发布了《' + wztitle + '》'
                send_wx_message(wx_url, wx_content)
                last_list.append(wzid)
        now_text = json.dumps({'list': last_list})
        save_text('zcmugztz', now_text)

        last = get_text('zcmugsgg')
        if last == '':
            last = '{"list": []}'
        last_text = json.loads(last)
        last_list = last_text['list']
        resp = get_resp('get',
                        'https://portal.paas.zcmu.edu.cn/portal-api/v3/cms/content/getColumncontents?kw=&columnId=remote-9f24ed05-0fb2-4ae0-8e72-6eb9e22c5d9e&pageNo=1&pageSize=22&loadContent=false&loadPicContents=true')
        resp_json = json.loads(resp)
        wzlist = resp_json['data']['allContents']
        for wz in wzlist:
            wzid = wz['id']
            wzurl = wz['url']
            wztitle = wz['title']
            if wzid in last_list:
                continue
            else:
                print(wztitle)
                wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
                wx_content = '【公示公告】OA系统发布了《' + wztitle + '》'
                send_wx_message(wx_url, wx_content)
                last_list.append(wzid)
        now_text = json.dumps({'list': last_list})
        save_text('zcmugsgg', now_text)

        last = get_text('zcmukyxs')
        if last == '':
            last = '{"list": []}'
        last_text = json.loads(last)
        last_list = last_text['list']
        resp = get_resp('get',
                        'https://portal.paas.zcmu.edu.cn/portal-api/v3/cms/content/getColumncontents?kw=&columnId=remote-a6ffde86-db1d-4996-9db3-598f6dcc6941&pageNo=1&pageSize=22&loadContent=false&loadPicContents=true')
        resp_json = json.loads(resp)
        wzlist = resp_json['data']['allContents']
        for wz in wzlist:
            wzid = wz['id']
            wzurl = wz['url']
            wztitle = wz['title']
            if wzid in last_list:
                continue
            else:
                print(wztitle)
                wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
                wx_content = '【科研学术】OA系统发布了《' + wztitle + '》'
                send_wx_message(wx_url, wx_content)
                last_list.append(wzid)
        now_text = json.dumps({'list': last_list})
        save_text('zcmukyxs', now_text)

        last = get_text('zcmuxxgw')
        if last == '':
            last = '{"list": []}'
        last_text = json.loads(last)
        last_list = last_text['list']
        resp = get_resp('get',
                        'https://portal.paas.zcmu.edu.cn/portal-api/v3/cms/content/getColumncontents?kw=&columnId=remote-b270c080-44d0-4fb1-ac4d-a7d76173cebc&pageNo=1&pageSize=22&loadContent=false&loadPicContents=true')
        resp_json = json.loads(resp)
        wzlist = resp_json['data']['allContents']
        for wz in wzlist:
            wzid = wz['id']
            wzurl = wz['url']
            wztitle = wz['title']
            if wzid in last_list:
                continue
            else:
                print(wztitle)
                wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f8ba152-c44b-491e-abb7-d140f6100f54'
                wx_content = '【学校公文】OA系统发布了《' + wztitle + '》'
                send_wx_message(wx_url, wx_content)
                last_list.append(wzid)
        now_text = json.dumps({'list': last_list})
        save_text('zcmuxxgw', now_text)
    else:
        print('【网络环境检测】当前IP地址处于外网，程序退出')

    print("===============推送完毕===============")




if __name__ == '__main__':
    main()
