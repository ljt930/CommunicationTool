#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/26 21:57
# @Author  : Aries
# @Site    : 
# @File    : communicationBase.py
# @Software: PyCharm

class communicationBase():
    def __init__(self):


        print ("init:communicationBase")
        self._isBondLocalAddr = False #客户端，指定本地端口发送

        self._isHexSend = False
        self._isHexDisplay = False
        self._isAutoRecv = False

        self.link = False
        pass

    def open(self):
        print "Base::open"
    def close(self):
        print ("Base::close")
    def send(self,data):
        print "Base::send"


    def setAddress(self,ip, port):
        self._ip = ip
        self._port = port

    def setHexSend(self,isHexSend):
        self._isHexSend = isHexSend

    def setHexDisplay(self,isHexDisplay):
        self._isHexDisplay = isHexDisplay

    def setAutoRecv(self,isAutoRecv):
        self._isAutoRecv = isAutoRecv
