# encoding: utf-8
from pyExcelerator import Workbook


class ExcelWriter(object):

    #XLS_HEADERS = [u'公司ID编码', u'公司名', u'公司简介', u'公司主要产品', u'公司网站', u'公司网站标题']
    XLS_HEADERS = [u'公司ID', u'公司名', u'公司网址', u'网站标题',u'网站描述', u'网站搜索关键词或产品']
    COLS = len(XLS_HEADERS)

    def __init__(self, logger, output_name='text.xls'):
        self.logger = logger
        self.workbook = Workbook()
        self.worksheet = self.workbook.add_sheet('CompanyInformation')
        self.output_name = output_name
        self.row = 1

        for col in range(ExcelWriter.COLS):
            self.worksheet.write(0, col, ExcelWriter.XLS_HEADERS[col])


    def insert(self, obj):
        items = obj.get_info_as_tuple()
        for col, item in enumerate(items):
            self.worksheet.write(self.row, col, item.decode('utf-8'))
        self.logger.info('成功在%s中写入%s', self.output_name, obj.corp_name)


    def next_row(self):
        self.row += 1
        return self.row


    def commit(self):
        self.workbook.save(self.output_name)


