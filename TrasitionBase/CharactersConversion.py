#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/14 12:57
# @Author  : Aries
# @Site    : 
# @File    : CharactersConversion.py
# @Software: PyCharm

class CharactersConversion():
    def QString2PyString(self, qStr):
        # # QString，如果内容是中文，则直接使用会有问题，要转换成 python string
        # print type(qStr)
        return unicode(qStr.toUtf8(), 'utf-8', 'ignore')

    def QStringToInt(self, qStr):
        i_tmp = qStr.toInt()
        ##example :tupe (int ,bool)
        if i_tmp[1]:
            i = i_tmp[0]
        else:
            i = 0
        return i
    def StrToBool(self,str): #字符转bool
        if str.lower() == "true":
            return True
        elif str == "1":
            return True
        else:
            return False
    def BoolToStr(self,bool):
        if bool:
            return "1"
        else:
            return "0"

if __name__ == '__main__':
    b =False