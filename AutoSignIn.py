#! usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import requests as re

# 系统变量
StuID = os.environ['STUID']
PW = os.environ['PW']
SERVER = os.environ['SERVER']
SCKEY = os.environ['SCKEY']
MAIL_NOTICE = os.environ['MAIL_NOTICE']
MAILBOX = os.environ['MAILBOX']

CHROMEDRIVER_PATH = './chromedriver'

# 以下内容无需修改
mail_host = 'smtp.qq.com'
mail_sender = '973006245@qq.com'
mail_pw = 'ihoezpquhuawbfif'
url = 'https://xmuxg.xmu.edu.cn/app/214'
dkStart = datetime.now()

# 判断是否在打卡时间内
def timeFlag():
    startTime = time.strftime("%Y-%m-%d 23:00:00", time.localtime())
    endTime = time.strftime("%Y-%m-%d 11:30:00", time.localtime())
    startTimeStamp = time.mktime(time.strptime(startTime, "%Y-%m-%d %H:%M:%S"))
    endTimeStamp = time.mktime(time.strptime(endTime, "%Y-%m-%d %H:%M:%S"))
    if startTimeStamp < time.time() < endTimeStamp:
        print('目前处于打卡时间...')
        return True
    else:
        print("不在打卡时间!")
        sendMsg('不在打卡时间。')
        return False

# 自动打卡
def autoSignIn():
    global dkStart
    try:
        dkStart = datetime.now()
        print('正在打卡...')
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
        # driver = webdriver.Chrome(CHROMEDRIVER_PATH)
        driver.get(url)
        driver.maximize_window()
        driver.delete_all_cookies()

        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="loginLayout"]/div[3]/div[2]/div/button[2]').click()
        time.sleep(1)

        print('正在登录...')
        driver.find_element_by_xpath('//input[@id="username"]').send_keys(StuID)
        driver.find_element_by_xpath('//input[@id="password"]').send_keys(PW)
        driver.find_element_by_xpath('//input[@id="password"]').send_keys(Keys.ENTER)
        time.sleep(1)
        print('登录成功...\n正在更改表单...')

        # 判断学号密码是否正确
        print('driver.title is: {}'.format(driver.title))
        title = str(driver.title)
        if '厦门大学' in title:
            print('登录成功...\n正在更改表单...')
        elif title == '统一身份认证' or title == 'Unified Identity Authentication':
            msg = '学号或密码错误？or 登录频繁，需要验证码登录？'
            print('Error: {}'.format(msg))
            sendMsg(msg)
            return 0
        else:
            pass

        # 点击daily health report
        driver.find_element_by_xpath('//*[@id="mainPage-page"]/div[1]/div[3]/div[2]/div[2]/div[3]/div/div[1]/div[2]').click()
        time.sleep(1)

        window1 = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != window1:
                driver.switch_to.window(handle)
                # print(handle)
                break

        time.sleep(1)

        # 点击我的表单
        driver.find_element_by_xpath('//*[@id="mainM"]/div/div/div/div[1]/div[2]/div/div[3]/div[2]').click()
        time.sleep(2)

        span = driver.find_element_by_xpath('//*[@id="select_1582538939790"]/div/div/span[1]')
        print('span.get_attribute() is: {}'.format(span.get_attribute('innerHTML')))

        # 判断是否已打卡！
        if span.get_attribute('innerHTML') == '是 Yes':
            print("今日已打卡！请勿重复打卡。")
            driver.quit()
            sendMsg("今日已打卡！请勿重复打卡。")
        else:
            driver.find_element_by_xpath('//*[@id="select_1582538939790"]/div').click()
            driver.find_element_by_xpath('//span[text()="是 Yes"]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="pdfDomContent"]/../span/span').click()
            time.sleep(1)
            driver.switch_to.alert.accept()
            time.sleep(2)
            driver.quit()
            print('打卡成功！')
            sendMail("打卡成功！")
            sendMsg("打卡成功！")
    except Exception as e:
        print('打卡失败！\n{}'.format(str(e)))
        sendMsg("打卡失败！", str(e))
        sendMail("打卡失败！", str(e))

# 发送微信推送消息
def sendMsg(m, error=''):
    if SERVER == 'on':
        timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        duration = datetime.now() - dkStart
        if error == '':
            msg = '{} {}! 本次打卡耗时{}秒。'.format(timeNow, m, duration.seconds)
        else:
            msg = '{} {}!'.format(timeNow, error)
        url = 'https://sc.ftqq.com/{}.send?text={}&desp={}'.format(SCKEY, msg, '{}\n{}'.format(msg, error))
        re.get(url)

# 发送邮件通知
def sendMail(text="健康打卡成功", error=''):
    print('发送邮件...')
    if MAIL_NOTICE == 'on':
        timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        duration = datetime.now() - dkStart
        content = "{}\n{}\n本次耗时{}秒！".format(timeNow, text, duration)
        msg = MIMEText(content, 'plain', 'utf-8')
        msg["From"] = Header(mail_sender, 'utf-8')
        msg["To"] = Header(MAILBOX, 'utf-8')
        subject = "{0}-{1}".format(time.strftime("%Y%m%d", time.localtime()), text)
        msg["Subject"] = Header(subject, 'utf-8')
        try:
            server = smtplib.SMTP()
            server.connect(mail_host, 25)
            server.login(mail_sender, mail_pw)
            server.sendmail(mail_sender, MAILBOX, msg.as_string())
            server.quit()
            print("邮件发送成功！")
        except Exception as e:
            print("邮件发送失败！\n{}".format(e))

if __name__ == '__main__':
    if timeFlag():
        autoSignIn()
