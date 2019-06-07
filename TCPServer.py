#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/5/28 11:28
# @Author  : linjinting
# @Site    : 
# @Software: CommunicationTool
# @File    : TCPServer.py
# @Function: TCPServer


# from communicationBase import communicationBase
import select
from TCPServerBase import TCPServerBase
from PyQt4 import QtCore

class TCPServer(QtCore.QThread,TCPServerBase):
    def __init__(self):
        super(TCPServer,self).__init__()
        TCPServerBase.__init__(self)


        # self.client_socket_list = list()
        # self.socket = None
        self.isStopDisplay = False



    def tcp_server_concurrency(self):
        inputs = [self.socket]
        # self.outputs = []
        # 创建epoll对象
        while True:
            try:
                r_list, w_list, e_list = select.select(inputs, [], [], )
            except Exception as ret:
                print ret
                self.client_socket_list= list()
                break
            else:
            # print w_list
                for e in e_list: continue
                for client_socket in r_list:
                    # socket, address = item
                    if client_socket == self.socket:
                        client_socket, client_address = client_socket.accept()
                        inputs.append(client_socket)
                        self.client_socket_list.append((client_socket, client_address))
                        msg = '客户端IP:%s端口:%s,已连接' % (client_address[0], client_address[1])
                        self.show_msg("statusmsg", msg)
                        self.show_msg("addclient")
                    else:
                        try:
                            recv_msg = client_socket.recv(1024)
                            address = client_socket.getpeername()
                        except Exception as ret:
                            print ret
                        else:
                            if recv_msg != b'':
                                if self._isAutoRecv:
                                    client_socket.send(recv_msg)

                                if self._isHexDisplay:
                                    recv_data = self.encode_to_hex(recv_msg)
                                else:
                                    recv_data = recv_msg

                                msg = "from %s:%s|%s\n" % (address[0], address[1], recv_data)
                                self.show_msg("write", msg)
                                # if item not in self.outputs:
                                #     self.outputs.append(item)

                            else:
                                msg = "客户端IP:%s端口:%s,已断开连接" % (address[0], address[1])
                                self.show_msg("statusmsg", msg)

                                self.client_socket_list.remove((client_socket, address))
                                self.show_msg("addclient")
                                inputs.remove(client_socket)
                                client_socket.close()

                    for client_socket in e_list:
                        address = client_socket.getsockname()
                        msg = ("完蛋，{:d} 出现异常了！".format(client_socket.fileno()))
                        self.show_msg("statusmsg", msg)
                        inputs.remove(client_socket)
                        self.client_socket_list.remove((client_socket, address))


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
        if self.isStopDisplay :
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

    def setStopDisplay(self,isStopDisplay):
        self.isStopDisplay = isStopDisplay

if __name__ == '__main__':
    tcps = TCPServer()
    tcps.setAddress("127.0.0.1",5566)
    tcps.open()