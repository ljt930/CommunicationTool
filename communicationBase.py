#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/26 21:57
# @Author  : Aries
# @Site    : 
# @File    : communicationBase.py
# @Software: PyCharm
import socket
from TrasitionBase.CharactersConversion import CharactersConversion

class communicationBase(object):
    _socket = socket
    _isBondLocalAddr = False  # 客户端，指定本地端口发送

    _isHexSend = False
    _isHexDisplay = False
    _isAutoRecv = False
    _isDebug = False

    _islocaladdress = False
    _link = False
    def __init__(self):


        print ("init:communicationBase")


        # self._socket = socket
        # self._isBondLocalAddr = False #客户端，指定本地端口发送
        #
        # self._isHexSend = False
        # self._isHexDisplay = False
        # self._isAutoRecv = False
        # self._isDebug = False
        #
        # self._link = False


    def open(self):
        print "Base::open"
    def close(self):
        print ("Base::close")
    def send(self,data):
        print "Base::send"


    def setAddress(self,ip, port):
        self._ip = ip
        self._port = port

    def setopAddress(self,ip, port):
        self._opip = ip
        self._opport = port

    def setHexSend(self,isHexSend):
        self._isHexSend = isHexSend

    def setHexDisplay(self,isHexDisplay):
        self._isHexDisplay = isHexDisplay

    def setAutoRecv(self,isAutoRecv):
        self._isAutoRecv = isAutoRecv
        print self._isAutoRecv


    def setDebug(self):
        self._isDebug = True

    def show_msg(self,type_,msg=""):
        """
        功能函数，根据不同类型显示不同的信息内容
        参数---type_:statusmsg，status，write_msg,addclient,print
           ---msg:str类型数据，默认为空
        :return:
        """
        print "--Base---show-msg"
        if msg == "":
            return
        print msg

    def decode_to_hex(self,data):
        return CharactersConversion().decode_to_hex(data)

    def encode_to_hex(self,data):
        return CharactersConversion().encode_to_hex(data)

