#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/5/28 11:29
# @Author  : linjinting
# @Site    : 
# @Software: CommunicationTool
# @File    : TCPClient.py
# @Function:

import socket
import struct
import threading
import stopThreading
import random
from communicationBase import communicationBase
from PyQt4 import QtCore

class TCPClient(QtCore.QThread,communicationBase):
    def __init__(self):
        communicationBase.__init__(self)

    def open(self):
        """
        开启UDP客户端方法
        :return:
        """
        print "TCPClient::open"