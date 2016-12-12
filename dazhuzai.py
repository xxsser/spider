#!/usr/bin/env/ python
# -*- coding:utf-8 -*-

from urllib import request
import re

index = request.urlopen("http://www.dazhuzaibook.com")

result = index.read().decode('utf-8')

ids = re.findall(r"http://www\.dazhuzaibook\.com/book/(\d+)\.html", result)

fo = open('tmp.log', 'r+')
# fo.write(match[-1])
lastId = fo.read()

for id in ids:
    if (int(id) > int(lastId)):
        fo.seek(0,0)
        info = request.urlopen("http://www.dazhuzaibook.com/book/"+id+".html")
        articlePage = info.read().decode('utf-8')
        article = re.findall(r"<!-- end header -->(.+)<div class=\"bg\">", articlePage,re.S)
        print(article[0])
        fo.write(id)
        break;

fo.close()
#print(match[-1])
