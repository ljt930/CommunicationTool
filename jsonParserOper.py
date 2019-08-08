#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/15 11:16
# @Author  : Aries
# @Site    : 
# @File    : jsonParserOper.py
# @Software: PyCharm
### python3
import json

class jsonOper():
    def __init__(self):

        self.filepath = "test.json"

    def loadfile(self,filepath):
        try :
            fp = open(filepath,"r")
            self.jsondict = json.load(fp)
            fp.close()
        except IOError as e:
            print(e)
            return 0
        return 1
    def jsonloads(self,strdata):
        return json.loads(strdata)
    def jsondumps(self, dictdata,encoding='utf-8'):

        return json.dumps(dictdata, encoding=encoding)

    def jsondump(self,obj, fp, encoding='utf-8'):

        return json.dump(obj, fp, encoding=encoding)

    def getjsondict(self,filepath):
        if self.loadfile(filepath):
            return self.jsondict
        else:
            return 0

if __name__ == '__main__':
    jo = jsonOper()
    jo.getjsondict("jsonstrBaseStartupParam.json")
    s = json.dumps(str({"WFServer":{"port":"5555"}}), indent=4)
    print(s)