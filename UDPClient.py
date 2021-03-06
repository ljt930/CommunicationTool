#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/5/27 20:08
# @Author  : linjinting
# @Site    :
# @Software: CommunicationTool
# @File    : UDPClient.py
# @Function:

from UDPClientBase import UDPClientBase
from PyQt5.QtCore import QObject, pyqtSignal


class UDPClient(QObject, UDPClientBase):
    signal_show_statusmsg = pyqtSignal(str)
    signal_show_status = pyqtSignal(str)
    signal_write_msg = pyqtSignal(str)
    def __init__(self):
        super(UDPClient, self).__init__()

        # self.open()

        self.isStopDisplay = False

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
    # def __del__(self):
    #     del self.socket
    #     del self.socket_th
    #     del self.opaddress
    #     print "udp--client __del__"


if __name__ == '__main__':
    c = UDPClient()
    c.setopAddress("127.0.0.1", 2500)
    c.open()
