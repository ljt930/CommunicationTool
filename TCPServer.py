#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/5/28 11:28
# @Author  : linjinting
# @Site    : 
# @Software: CommunicationTool
# @File    : TCPServer.py
# @Function:

import socket
import struct
import threading
import stopThreading
import random
from communicationBase import communicationBase
from PyQt4 import QtCore

class TCPServer(QtCore.QThread,communicationBase):
    def __init__(self):
        super(TCPServer,self).__init__()
        communicationBase.__init__(self)

        self.client_socket_list = list()

    def open(self):
        """
        功能函数，TCP服务端开启的方法
        :return: None
        """
        self.socket = self._socket.socket(self._socket.AF_INET, self._socket.SOCK_STREAM)
        # 取消主动断开连接四次握手后的TIME_WAIT状态
        self.socket.setsockopt(self._socket.SOL_SOCKET, self._socket.SO_REUSEADDR, 1)
        # 设定套接字为非阻塞式
        self.socket.setblocking(False)
        try:
            # port = int(self.lineEdit_port.text())
            self.socket.bind((self._ip, self._port))
        except Exception as ret:
            msg = "监听失败，请检查端口号"
            self.emit(QtCore.SIGNAL("signal_show_stat"), msg)
        else:
            self.socket.listen(128)
            self.socket_th = threading.Thread(target=self.tcp_server_concurrency)
            self.socket_th.start()
            msg = 'TCP服务端正在监听端口:%s' % self._port
            self.emit(QtCore.SIGNAL("signal_show_stat"), msg)

    def tcp_server_concurrency(self):
        """
        功能函数，供创建线程的方法；
        使用子线程用于监听并创建连接，使主线程可以继续运行，以免无响应
        使用非阻塞式并发用于接收客户端消息，减少系统资源浪费，使软件轻量化
        :return:None
        """
        while True:
            try:
                client_socket, client_address = self.socket.accept()
            except Exception as ret:
                # print ret
                pass
            else:
                client_socket.setblocking(False)
                # 将创建的客户端套接字存入列表,client_address为ip和端口的元组
                self.client_socket_list.append((client_socket, client_address))
                self.client_th = threading.Thread(target=self.clientsocket_concurrency,args=(client_socket, client_address))
                self.client_th.start()
                msg = '客户端IP:%s端口:%s已连接\n' % client_address
                self.emit(QtCore.SIGNAL("signal_write_msg"), msg)

            # for client, client_addr in self.client_socket_list:
            #     try:
            #         recv_msg = client.recv(1024)
            #     except Exception as ret:
            #         pass
            #     else:
            #         if recv_msg:
            #             # receive_data = recv_msg.decode('utf-8')
            #             # receive_data = recv_msg.encode('hex')
            #             receive_data = recv_msg
            #             msg = "from %s:%s|%s\n" % (client_addr[0], client_addr[1], receive_data)
            #             self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
            #             # print msg
            #         else:
            #             msg = "客户端IP:%s端口:%s已断开连接\n" % (client_addr[0], client_addr[1])
            #             self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
            #             client.close()
            #             self.client_socket_list.remove((client, client_addr))

    def clientsocket_concurrency(self,client,client_addr):
        while True:
            try:
                recv_msg = client.recv(1024)
            except Exception as ret:
                pass
            else:
                if recv_msg:
                    # receive_data = recv_msg.decode('utf-8')
                    # receive_data = recv_msg.encode('hex')
                    receive_data = recv_msg
                    msg = "from %s:%s|%s\n" % (client_addr[0], client_addr[1], receive_data)
                    self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
                    # print msg
                else:
                    msg = "客户端IP:%s端口:%s已断开连接\n" % (client_addr[0], client_addr[1])
                    self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
                    client.close()
                    self.client_socket_list.remove((client, client_addr))
                    break
        print "client thread exit"