#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import sys
import urllib ,urllib2
import re
import chardet
urllib2.socket.setdefaulttimeout(30)
f=open("input.txt",'r')
out=open('output.txt','w')
def findtitle(web):
    print "processing "+web,
    try:
        htmlfile=urllib2.urlopen(web).read()
        title=re.findall(r'(?<=<title>).*?(?=</title>)',htmlfile,re.DOTALL)[0]
    except BaseException:
        title="此网站无标题或者标题错误"
        charset=chardet.detect(htmlfile)['encoding'].lower()
        if charset=='gbk' :
            title = title.decode('gbk').encode('utf-8')
        if charset=='gb2312' :
            title = title.decode('gb2312').encode('utf-8')
        if charset=='utf-8' or charset=='utf8':
            #title = title.encode('utf-8')
            pass
    return title

def startinput():
    while True:
        web=f.readline()
        if len(web)==0:
           break
        title=findtitle(web)
        print "success"
        out.write(title.strip()+'\n')
        out.flush()
    f.close()
    out.close()
    print "finish"

if __name__ == "__main__":
    startinput()