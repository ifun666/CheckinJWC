# AutoSignIn
打卡时间：每天的8-19点，每3小时运行一次。  

## 操作说明
### 1、fork 此仓库
直接fork此仓库到自己的GitHub；
![image](https://user-images.githubusercontent.com/26132150/119790603-a7271f00-bf06-11eb-90c6-d022732c38cd.png)

### 2、设置账号信息
Settings→Secrets→New repository secret；  
变量说明：
| Name | Value | 说明 |
| ---- | ---- | ---- |
| STUID | 11120211111111 | 学号 |
| PW | ****** | 密码 |
| SERVER | on/off | 是否开启server酱|
| SCKEY | SCU111... | 若SERVER=on，则填写自己的sckey；否则空着就行 |
| MAIL_NOTICE | on/off | 是否开启邮箱推送 |
| MAILBOX | 1@1.com | 用于接收通知的邮箱 |

![image](https://user-images.githubusercontent.com/26132150/119790859-d76ebd80-bf06-11eb-893e-aed9ff9b4d62.png)
![image](https://user-images.githubusercontent.com/26132150/119790869-da69ae00-bf06-11eb-90a9-ecc93bce687e.png)

### 3、启用Acitons
启用GitHub Actions，并修改任意文件Commit一次即可运行。  
可在Actions→Update...→build→SignIn查看运行结果。
微信推送和邮箱通知可选。
![image](https://user-images.githubusercontent.com/26132150/119792113-05083680-bf08-11eb-9473-5f096d8dadf7.png)
