#!/usr/bin/env/ python
# -*- coding:utf-8 -*-

from urllib import request
from os import path
from inspect import getfile, currentframe
import re, smtplib
from email.mime.text import MIMEText

index = request.urlopen("http://m.daizhuzai.com/1/list/?page=1&sort=desc")

result = index.read().decode('utf-8')

articleMatch = re.search(r"<a href=\"/1/t(.+).html\" title=\"(.+)\">", result)
newId = articleMatch.group(1)
newTitle = articleMatch.group(2)


currentDir = path.dirname(path.abspath(getfile(currentframe())))
fo = open(currentDir + '/daizhuzai_com.log', 'r+')
# fo.write(match[-1])
lastId = fo.read()

article = False

if int(lastId) < int(newId):
    info = request.urlopen("http://m.daizhuzai.com/1/t" + newId + ".html")
    articlePage = info.read().decode('utf-8')
    article = re.search(r"<p class=\"title\">.+<br/>", articlePage, re.S)


if article != False:
    sender = "isender@sina.cn"
    recevier = "temp@xianwangsou.com"

    message = MIMEText(article.group(0), 'html', 'utf-8')
    message['From'] = sender
    message['To'] = recevier
    message['Subject'] = '大主宰 ' + newTitle

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect('smtp.sina.cn')
        smtpObj.login(sender, '******')
        smtpObj.sendmail(sender, recevier, message.as_string())
        fo.seek(0, 0)
        fo.write(newId)
        print ('send article id: '+ newId +' success')
    except smtplib.SMTPException:
        print ('send mail fail')
else:
    print ('havn\'t new article')

fo.close()
