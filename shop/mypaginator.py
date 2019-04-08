# encoding:utf-8

import math

class MyPaginator:
    def __init__(self,object_list,pagenum=5,nowpage=0):
        self.totalpage = 0
        self.object_list = object_list
        self.pagenum = int(pagenum)
        if self.object_list.count() != 0 :
            self.totalpage = math.ceil(self.object_list.count()/self.pagenum)
        self.nowpage = nowpage
        '''
        传入：
            对象集合    object_list
            每一页的条数  pagenum

        变量：
            总页数， object_list/pagenum

        函数：
            判断是否有上一页 has_previous
            判断是否有下一页 has_next
            返回 object_list: page(页数 num)
            

       
分页功能
    针对对象： 所有对象，传入
    传入： 页数， 默认： 第一页 ，初始化： 第一页
    跟 django 的 paginator 一样， 需要先把需要的数据 filter， 然后根据后面的集合，进行分页。
    
'''
    # 是否有上一页
    def has_previous(self):
        if self.nowpage <= 1 :
            return False
        return True

    # 是否有下一页
    def has_next(self):
        if self.nowpage>=1 and self.nowpage < self.totalpage:
            return True
        else:
            return False

    # 返回 object_list 对象
    def getpage(self,nowpage):
        self.nowpage = nowpage
        beginnum = self.pagenum * (self.nowpage - 1 )
        endnum = beginnum + self.pagenum
        pagelist = self.object_list[beginnum:endnum]
        return pagelist

    # 取下一页
    '''
    return object_list (next page) 
    '''
    def next_page(self):
        if self.has_next():
            self.nowpage += 1
            pagelist = self.getpage(self.nowpage)
            return pagelist



    # 取上一页
    '''
    return object_list(previous page)
    '''
    def previous_page(self):
        if self.has_previous():
            self.nowpage = self.nowpage - 1
            pagelist = self.getpage(self.nowpage)
            return pagelist



