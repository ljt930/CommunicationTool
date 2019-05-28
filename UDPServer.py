#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/5/27 20:28
# @Author  : linjinting
# @Site    : 
# @Software: CommunicationTool
# @File    : UDPServer.py
# @Function:

import socket
import struct
import threading
import stopThreading
import random
from communicationBase import communicationBase
from PyQt4 import QtCore

class UDPServer(QtCore.QThread, communicationBase):
    # signal_show_stat = QtCore.SIGNAL("signal_show_stat")
    def __init__(self):
        super(UDPServer,self).__init__()
        communicationBase.__init__(self)

        self.client_socket_list = list()
        self._socket = None
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(3)



        # self.setAddress()



    # def setAddress(self):
    #     """
    #     获取ip地址、端口等参数
    #     :return:
    #     """
    #     self._port = 1235
    #     self._ip = ""
    #     pass

    def open(self):
        """
        开启UDP服务端方法
        :return:
        """
        print "UDPServer::open"

        try:
            # port = int(self.lineEdit_port.text())
            self.address = (self._ip, self._port)
            print self.address
            self._socket.bind(self.address)
        except Exception as ret:
            print ret
            msg = "请检查：%s"%(ret)
            self.emit(QtCore.SIGNAL("signal_show_stat"), msg)

        else:
            self.link = True
            self._socket_th = threading.Thread(target=self.udp_server_concurrency)
            self._socket_th.start()
            msg = "UDP服务端正在监听端口:%s" %(self._port)
            self.emit(QtCore.SIGNAL("signal_show_stat"), msg)

    def udp_server_concurrency(self):
        """
        用于创建一个线程持续监听UDP通信
        :return:
        """
        while True:
            try:
                # print self.address
                recv_msg, client_addr = self._socket.recvfrom(1024)
                if not recv_msg :
                    print "exit"
                    break
                self.client_socket_list.append(client_addr)
                # msg  = "has udp client for %s:%s"% (client_addr[0], client_addr[1])
                # self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
                # receive_data = recv_msg.decode('utf-8')
                if self._isHexDisplay:
                    recv_msg = recv_msg.encode('hex')

                msg = "from %s:%s|%s\n" % (client_addr[0], client_addr[1], recv_msg)
                self.emit(QtCore.SIGNAL("signal_write_msg"), msg,client_addr)
            except socket.timeout:
                print "time out"
                continue
            except EOFError,e:
                print e
                break
            # else:
            #     print "continue"
            #udp收到信息自动回复
            # if self._isautoRecv:
            #     self._socket.sendto(recv_msg, (client_addr[0], client_addr[1]))

        print "server Thread exit"
    def send(self,data):
        if self.link is False:
            msg = '请选择服务，并点击连接网络\n'
            self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
        else:
            try:
                if self._isHexSend:
                    data_hex = data.encode('hex')
                else:
                    data_hex = data
                if self._isHexDisplay:
                    recv_data = data.encode('hex')
                else:
                    recv_data = data

                for client_addr in self.client_addr_list:
                    self.address = client_addr
                    self.udp_socket.sendto(data_hex, self.address)
                    msg = "sendto %s:%s|%s\n" % (self.address[0], self.address[1], recv_data)
                    self.emit(QtCore.SIGNAL("signal_write_msg"), msg)


            except Exception as ret:
                msg = "failed sendto %s:%s|%s\n" % (self.address[0], self.address[1],ret)
                self.emit(QtCore.SIGNAL("signal_show_stat"), msg)