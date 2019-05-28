#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/5/27 20:08
# @Author  : linjinting
# @Site    : 
# @Software: CommunicationTool
# @File    : UDPClient.py
# @Function:
import socket
import struct
import threading
import stopThreading
import random
from communicationBase import communicationBase
from PyQt4 import QtCore

class UDPClient(QtCore.QThread,communicationBase):
    def __init__(self):
        communicationBase.__init__(self)

        # self.open()


    def open(self):
        """
        开启UDP客户端方法
        :return:
        """
        print "UDPClient::open"




if __name__ == '__main__':
    channel = UDPClient()


