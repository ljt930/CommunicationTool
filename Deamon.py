#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/13 23:05
# @Author  : Aries
# @Site    : 
# @File    : Deamon.py
# @Software: PyCharm



import subprocess,os,time

class Deamon():
    def __init__(self):
        self.p = None
        self.env = os.environ.copy()
        p_path = "D:\\contron\\PSM70_Standalone-pub_SZES"
        self.work = "%s\\bin"%(p_path)
        self.env['PATH'] = "%s\\lib\\cyg;%s\\lib\\other;%s\\lib\\qt"%(p_path,p_path,p_path)
        # self.env['PATH'] = "D:\\contron\\PSM70_Standalone-pub_SZES\\bin"

        self.cmd ="%s\\Phoenix.exe"%(self.work)
    def starproc(self):
        self.p = subprocess.Popen([self.cmd], stdout=None, shell=False,
                 cwd=self.work, env=self.env)


    def show(self):
        # print self.p.stdout.read()
        print self.p.pid
        r = self.p.poll()
        print r
        return r
if __name__ == '__main__':
    d = Deamon()
    d.starproc()
    while 1:
        time.sleep(10)
        r = d.show()
        if r is not None:
            if r == 0 :
                break
            d.starproc()