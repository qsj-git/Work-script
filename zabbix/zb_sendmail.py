#!/bin/env  python
#coding:utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import sys


# 第三方 SMTP 服务，配置服务器，配置账号和授权码
smtpaddr = 'smtp.163.com'       # 配置163smtp服务器
myemail = '*******@163.com'     # 邮箱账号
password = '*************'      # 注意这里是在邮箱设置里开启SMTP服务后的授权码，不是账号登录密码

# 获取系统变量，脚本后三个变量
recvmail = sys.argv[1]
subject = sys.argv[2]
content = sys.argv[3]

# 配置发件内容
msg = MIMEText('''{}'''.format(content), "plain", "utf-8")
# 设置主题
msg['Subject'] = Header(subject, 'utf-8').encode()
# 设置发件人
msg['From'] = myemail
# 设置收件人
msg['To'] = recvmail


try:
    smtp = SMTP_SSL(smtpaddr)
    smtp.login(myemail, password)
    smtp.sendmail(myemail, recvmail.split(','), msg.as_string())
    smtp.quit()
    print("success")
except Exception as e:
    print("fail:"+str(e))
