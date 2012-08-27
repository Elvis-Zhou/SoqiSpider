#!/usr/bin/env python
# -*- coding: utf-8 -*-
#encoding=utf-8
#import sys

from pyExcelerator import Workbook
import traceback
import urllib ,urllib2
import re,time
import chardet
urllib2.socket.setdefaulttimeout(30)
from bs4 import BeautifulSoup
f=open("input.txt",'r')
out=open('output.txt','a')
htmlfile=""
website=""
charset=""


class ExcelWriter(object):

    #XLS_HEADERS = [u'公司ID编码', u'公司名', u'公司简介', u'公司主要产品', u'公司网站', u'公司网站标题']
    XLS_HEADERS = [ u'公司名', u'公司网址', u'网站标题',u'网站描述', u'网站搜索关键词或产品']
    COLS = len(XLS_HEADERS)

    def __init__(self, output_name='findKeywordAndTitle.xls'):
        #self.logger = logger
        self.workbook = Workbook()
        self.worksheet = self.workbook.add_sheet('CompanyInformation')
        self.output_name = output_name
        self.row = 1

        for col in range(ExcelWriter.COLS):
            self.worksheet.write(0, col, ExcelWriter.XLS_HEADERS[col])


    def insert(self,obj):
        items = obj
        for col, item in enumerate(items):
            self.worksheet.write(self.row, col, item)
            #self.logger.info('成功在%s中写入%s', self.output_name, obj.corp_name)


    def next_row(self):
        self.row += 1
        return self.row


    def commit(self):
        self.workbook.save(self.output_name)




class finding():
    def __init__(self):
        self.htmlfile=""
        self.website=""
        self.charset=""
        self.title=""
        self.keyword=""
        self.description=""

    def findtitle(self,web):
        #global htmlfile,charset,website
        self.website=web
        print "processing "+web,
        #charset=""
        try:
            self.htmlfile=urllib2.urlopen(self.website).read()
            #print self.htmlfile
            self.title=re.findall(r'(?<=<title>).*?(?=</title>)',self.htmlfile,re.DOTALL)[0]
            #self.charset=chardet.detect(self.htmlfile)
            self.charset=chardet.detect(self.htmlfile)['encoding'].lower()
            #print self.charset
            #if self.charset=='gbk' :
            #    self.title = self.title.decode('gbk',"ignore")
            #if self.charset=='gb2312' :
            #    self.title = self.title.decode('gb2312',"ignore")
            #if self.charset=='utf-8' or self.charset=='utf8':
            #    self.title = self.title.decode('utf-8',"ignore")
            #pass
            self.title=self.title.decode(self.charset,"ignore")
        except BaseException:
            #print traceback.print_exc()
            self.title=u"此网站无标题或者标题错误"

        print self.title.encode('utf-8')
        out.write(self.website+"网址标题:\n"+self.title.strip().encode('utf-8')+"\n")
        return self.title

    def findkeyword(self):
        #global htmlfile,website,charset
        #website=web
        print "processing keyword and description "+self.website,
        if not self.htmlfile:
            try:
                self.htmlfile=urllib2.urlopen(self.website).read()
            except:
                pass
                #title=re.findall(r'(?<=<title>).*?(?=</title>)',htmlfile,re.DOTALL)[0]
        #print htmlfile
        #print
        self.htmlfile=self.htmlfile.decode(self.charset,"ignore").encode("utf-8")
        #print htmlfile
        #print charset
        soup=BeautifulSoup(self.htmlfile,"lxml")

        self.keyword=soup.find("meta",{"name":"Keywords"})
        if not self.keyword:
            self.keyword=soup.find("meta",{"name":"keywords"})

        if self.keyword:
            self.keyword= self.keyword["content"]
        else:
            self.keyword=u"该网站没有关键词"
        ss=re.sub(r'\b','|',self.keyword.encode("utf-8"),re.M)
        ss=ss.replace("？","|")
        ss=ss.replace("?","|")
        ss=ss.replace("、","|")
        ss=ss.replace("，","|")
        ss=ss.replace("。","|")
        ss=ss.replace(",","|")
        ss=ss.replace(".","|")
        ss=ss.replace("||","|")
        ss=ss.replace("||","|")
        if ss.endswith("|"):
            ss=ss[:-1]
        if ss.startswith("|"):
            ss=ss[1:]
        self.keyword=ss.decode("utf-8")
        print self.keyword

        self.description=soup.find("meta",{"name":"Description"})
        if not self.description:
            self.description=soup.find("meta",{"name":"description"})

        if self.description:
            self.description=self.description["content"]
        else:
            self.description=u"该网站没有网站描述"
        print self.description


        out.write("关键词\n"+self.keyword.encode("utf-8")+"\n")
        out.write("网站描述\n"+self.description.encode("utf-8")+"\n")
        out.write("####################################\n")

    def get_as_tuple(self):
        return (
            "",self.website,self.title,self.description,self.keyword
            )

def startinput():
    #global website
    soqi=finding()
    excel=ExcelWriter("findKeywordAndDescription%s.xls" % time.strftime("%y-%m-%d-%H-%M-%S",time.localtime(time.time())))

    while True:
        web=f.readline()
        if len(web)==0:
            break
        #website=web
        if web.strip():
            soqi.findtitle(web)
            soqi.findkeyword()
            excel.insert(soqi.get_as_tuple())
            excel.next_row()
            excel.commit()
        print "success"
        #htmlfile=""
        #out.write(title.strip()+'\n')
        out.flush()
    f.close()
    out.close()
    print "finish"

if __name__ == "__main__":
    startinput()
    #web="http://www.icbc.com.cn/icbc"
    #soqi=finding()
    #excel=ExcelWriter("findKeywordAndDescription%s.xls" % time.strftime("%y-%m-%d-%H-%M-%S",time.localtime(time.time())))
    #soqi.findtitle(web)
    #soqi.findkeyword()
    #excel.insert(soqi.get_as_tuple())
    #excel.next_row()
    #excel.commit()
    print "success"



