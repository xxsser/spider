#!/usr/bin/env/ python
# -*- coding:utf-8 -*-

from urllib import request
from os import path
from inspect import getfile, currentframe
import re
import smtplib
from email.mime.text import MIMEText

index = request.urlopen("http://www.dazhuzaibook.com")

result = index.read().decode('utf-8')

articleIds = re.findall(r"http://www\.dazhuzaibook\.com/book/(\d+)\.html", result)
currentDir = path.dirname(path.abspath(getfile(currentframe())))
fo = open(currentDir +'/dazhuzai.log', 'r+')
# fo.write(match[-1])
lastId = fo.read()

article = False

for articleId in articleIds:
    if int(articleId) > int(lastId):
        fo.seek(0, 0)
        info = request.urlopen("http://www.dazhuzaibook.com/book/" + articleId + ".html")
        articlePage = info.read().decode('utf-8')
        article = re.findall(r"<!-- end header -->(.+)<div class=\"bg\">", articlePage, re.S)
        break


if article != False:
    sender = "isender@sina.cn"
    recevier = "temp@xianwangsou.com"

    message = MIMEText(article[0], 'html', 'utf-8')
    message['From'] = sender
    message['To'] = recevier
    subject = re.findall(r"<h1>(.+)</h1>", article[0], re.S)
    message['Subject'] = '大主宰 ' + subject[0]

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect('smtp.sina.cn')
        smtpObj.login(sender, '******')
        smtpObj.sendmail(sender, recevier, message.as_string())
        fo.write(articleId)
        print ('send mail success')
    except smtplib.SMTPException:
        print ('send mail fail')

fo.close()
