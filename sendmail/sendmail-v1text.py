#!/usr/bin/python
# -*- coding: utf8 -*-

runhelp = """
-------------------------
send命令：
    python sendmail.py Recvmail [Explain]
    参数说明：
    Recvmail (必选)发送的收件人邮箱，多个收件人用逗号隔开
    Explain  (可选)备注的内容。注意，最好使用引号引起来。因为程序是按照空格位分割参数的

快捷设置：
    alias send="python /ifs/TJPROJ3/Plant/chenjun/mytools/sendmail.py "
    alias send="python /NJPROJ2/Plant/chenjun/mytools/sendmail.py "

【命令示例】：
send ***@163.com "今天天气真好，谢谢\""""

import sys
import smtplib
import re
from email.mime.text import MIMEText

mailserver = "smtp.126.com"  # 邮箱服务器地址
username_send = 'wan230114@126.com'  # 邮箱用户名
password = 'cj1234567'  # 邮箱密码：需要使用授权码
# sys.argv = ["","wan230114@126.com", "ang~"]
# print(sys.argv)
try:
    try:
        username_recv = sys.argv[1]   # 收件人，多个收件人用逗号隔开
        if not re.findall('.+@.+\..+', username_recv):
            raise NameError
        text_add = sys.argv[2]
        mailtext = '备注信息：\n%s' % text_add
    except IndexError:
        # username_recv = "wan230114@126.com"  # "1170101471@qq.com"
        mailtext = '备注信息：\n无'
    # print(len(sys.argv))
    if len(sys.argv) > 3:  # 检查参数是否过多
        raise ValueError
    print("正在发送邮件给%s" % username_recv)
    mail = MIMEText(mailtext, 'plain', 'utf-8') # 这是邮件内容
    mail['Subject'] = '来自wan230114的温馨提示'   # '这是邮件主题'
    mail['From'] = username_send  # 发件人
    mail['To'] = username_recv  # 收件人；[]里的三个是固定写法，别问为什么，我只是代码的搬运工
    smtp = smtplib.SMTP(mailserver, port=25, timeout=10)  # 连接邮箱服务器，smtp的端口号是25
    # smtp=smtplib.SMTP_SSL('smtp.qq.com',port=465) #QQ邮箱的服务器和端口号
    smtp.login(username_send, password)  # 登录邮箱
    # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
    smtp.sendmail(username_send, username_recv, mail.as_string())
    smtp.quit()  # 发送完毕后退出smtp
    print('发送成功，通知邮件已发送至%s' % username_recv)
except NameError as e:
    print("发送未完成，请输入正确的收件人邮箱地址\n%s" % runhelp)
except ValueError:
    print("发送未完成，您输入的参数过多，请检查输入的备注信息(参数：Explain)中是否有空格。\n若有，请将备注信息用双引号括起来\n%s" % runhelp)
# except:
    # print("发送未完成，可能原因是网络故障")
# finally：


"""
放置此处以后待探索云服务API：
https://dm.aliyuncs.com/?Action=SingleSendMail
&AccountName=time@shijianzhushou.xyz
&ReplyToAddress=true
&AddressType=1   
&ToAddress=1170101471@qq.com
&Subject=Hello New World
&HtmlBody=Hello MyFriend

https://dm.aliyuncs.com/?Action=BatchSendMail
&AccountName=test@shijianzhushou.xyz
&AddressType=1
&TemplateName=test1
&ReceiversName=test2
&TagName=test3

名称	类型	是否必须	描述
Action	String	必须	操作接口名，系统规定参数，取值：BatchSendMail。
AccountName	String	必须	管理控制台中配置的发信地址。
AddressType	Number	必须	取值范围 0~1: 0 为随机账号；1 为发信地址。
TemplateName	String	必须	预先创建且通过审核的模板名称。
ReceiversName	String	必须	预先创建且上传了收件人的收件人列表名称。
TagName	String	可选	邮件标签名称
ClickTrace	String	可选	取值范围 0~1: 1 为打开数据跟踪功能; 0 为关闭数据跟踪功能。该参数默认值为 0。

"""
