#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/5/27 20:28
# @Author  : linjinting
# @Site    :
# @Software: CommunicationTool
# @File    : UDPServer.py
# @Function:

from UDPServerBase import UDPServerBase
from PyQt5.QtCore import QObject, pyqtSignal


class UDPServer(QObject, UDPServerBase):
    signal_show_statusmsg = pyqtSignal(str)
    signal_show_status = pyqtSignal(str)
    signal_write_msg = pyqtSignal(str)
    signal_client_change = pyqtSignal()
    def __init__(self):
        super(UDPServer, self).__init__()
        UDPServerBase.__init__(self)

        self.isStopDisplay = False

    def channel_change(self, type_):
        if type_ == "client":
            self.signal_client_change.emit()

    def show_msg(self, type_, msg=""):
        """
        功能函数，根据不同类型显示不同的信息内容
        参数---type_:statusmsg，status，write_msg,addclient,print
           ---msg:str类型数据，默认为空
        :return:
        """
        # print "--TCPServer---show-msg"

        if self.isStopDisplay:
            return
        if msg == "":
            return
        # print msg
        if type_ == "print":
            print(msg)
        if type_ == "statusmsg":
            self.signal_show_statusmsg.emit(msg)
        if type_ == "status":
            self.signal_show_status.emit(msg)
        if type_ == "write":
            self.signal_write_msg.emit( msg)

    def setStopDisplay(self, isStopDisplay):
        self.isStopDisplay = isStopDisplay


if __name__ == '__main__':
    s = UDPServer()
    s.setAddress("127.0.0.1", 5566)
    s.open()
