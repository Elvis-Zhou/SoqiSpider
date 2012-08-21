#!/usr/bin/env python
# -*- coding: utf-8 -*-
#encoding=utf-8
#import sys
import urllib ,urllib2
import re
import chardet
urllib2.socket.setdefaulttimeout(30)
from bs4 import BeautifulSoup

f=open("input.txt",'r')
out=open('output.txt','a')
htmlfile=""
website=""
charset=""

def findtitle(web):
    global htmlfile,charset,website
    website=web
    print "processing "+web,
    #charset=""
    try:
        htmlfile=urllib2.urlopen(web).read()
        title=re.findall(r'(?<=<title>).*?(?=</title>)',htmlfile,re.DOTALL)[0]
        charset=chardet.detect(htmlfile)['encoding'].lower()
    except BaseException:
        title="此网站无标题或者标题错误"
    if charset=='gbk' :
        title = title.decode('gbk',"ignore").encode('utf-8')
    if charset=='gb2312' :
        title = title.decode('gb2312',"ignore").encode('utf-8')
    if charset=='utf-8' or charset=='utf8':
        #title = title.encode('utf-8')
        pass
    print title
    out.write(website+"网址标题:\n"+title.strip()+"\n")
    return title

def findkeyword():
    global htmlfile,website,charset
    #website=web
    print "processing keyword and description "+website,
    if not htmlfile:
        try:
            htmlfile=urllib2.urlopen(website).read()
        except:
            pass
            #title=re.findall(r'(?<=<title>).*?(?=</title>)',htmlfile,re.DOTALL)[0]
    #print htmlfile
    htmlfile=htmlfile.decode(charset,"ignore").encode("utf-8")
    #print htmlfile
    #print charset
    soup=BeautifulSoup(htmlfile)

    keyword=soup.find("meta",{"name":"Keywords"})
    if not keyword:
        keyword=soup.find("meta",{"name":"keywords"})

    if keyword:
        keyword= keyword["content"]
    else:
        keyword=u"该网站没有关键词"
    print keyword

    description=soup.find("meta",{"name":"Description"})
    if not description:
        description=soup.find("meta",{"name":"description"})

    if description:
        description=description["content"]
    else:
        description=u"该网站没有网站描述"
    print description


    out.write("关键词\n"+keyword.encode("utf-8")+"\n")
    out.write("网站描述\n"+description.encode("utf-8")+"\n")
    out.write("####################################\n")




def startinput():
    global website
    while True:
        web=f.readline()
        if len(web)==0:
            break
        website=web
        title=findtitle(web)
        findkeyword()
        print "success"
        htmlfile=""
        #out.write(title.strip()+'\n')
        out.flush()
    f.close()
    out.close()
    print "finish"

if __name__ == "__main__":
    startinput()
    #findtitle()
    #findkeyword()