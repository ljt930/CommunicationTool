#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/5/28 11:28
# @Author  : linjinting
# @Site    :
# @Software: CommunicationTool
# @File    : TCPServer.py
# @Function: TCPServer


from TCPServerBase import TCPServerBase
from PyQt4 import QtCore


class TCPServer(QtCore.QThread, TCPServerBase):
    def __init__(self):
        super(TCPServer, self).__init__()
        TCPServerBase.__init__(self)

        # self.client_socket_list = list()
        # self.socket = None
        self.isStopDisplay = False

    def channel_change(self, type_):
        if type_ == "client":
            self.emit(QtCore.SIGNAL("signal_client_change"))

    def show_msg(self, type_, msg=""):
        """
        功能函数，根据不同类型显示不同的信息内容
        参数---type_:statusmsg，status，write_msg,addclient,print
           ---msg:str类型数据，默认为空
        :return:
        """
        # print "--TCPServer---show-msg"
        if type_ == "addclient":
            # print "addclient"
            self.emit(QtCore.SIGNAL("signal_addclient"))
        if self.isStopDisplay:
            return
        if msg == "":
            return
        # print msg
        if type_ == "print":
            print msg
        if type_ == "statusmsg":
            self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)
        if type_ == "status":
            self.emit(QtCore.SIGNAL("signal_show_status"), msg)
        if type_ == "write":
            self.emit(QtCore.SIGNAL("signal_write_msg"), msg)

    def setStopDisplay(self, isStopDisplay):
        self.isStopDisplay = isStopDisplay


if __name__ == '__main__':
    tcps = TCPServer()
    tcps.setAddress("127.0.0.1", 5566)
    tcps.open()
