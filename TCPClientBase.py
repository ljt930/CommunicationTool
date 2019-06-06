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
import threading
import stopThreading
from communicationBase import communicationBase

class TCPClientBase(communicationBase):
    def __init__(self):
        super(TCPClientBase, self).__init__()

    def open(self):
        """
        开启TCP客户端方法
        :return: 2,-2
        """
        print "TCPClient::open-1"
        self.socket = self._socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.opaddress = (self._opip, self._opport)
            if self._islocaladdress:
                self.localAddress = (self._ip, self._port)
                self.socket.bind(self.localAddress)
        except Exception as ret:
            print ret
            msg = "请检查目标IP，目标端口"
            self.show_msg("statusmsg", msg)
            # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)
        else:

            msg = "正在连接目标服务器"
            self.show_msg("statusmsg", msg)
            # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)
            ret = self._connect()

            if ret == 2:
                self.client_th = threading.Thread(target=self.tcp_client_concurrency)
                self.client_th.start()
                self._link = True
                msg = 'TCP客户端已连接IP:%s端口:%s' % self.opaddress
                self.show_msg("status", msg)
                # self.emit(QtCore.SIGNAL("signal_show_status"), msg)
                return 2
            else:
                msg = '无法连接目标服务器' + ret.message
                self.show_msg("statusmsg", msg)
                # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)
                return -2


    def _connect(self):
        """
        功能函数，用于TCP客户端连接方法
        :return: 2,-2
        """
        try:
            self.socket.connect(self.opaddress)
        except Exception as ret:
            return ret
        else:
            return 2

    def tcp_client_concurrency(self):
        """
        功能函数，用于TCP客户端创建子线程的方法，阻塞式接收
        :return:
        """
        while True:
            recv_msg = self.socket.recv(1024)
            if recv_msg:
                if self._isHexDisplay:
                    recv_data = self.encode_to_hex(recv_msg)
                else:
                    recv_data = recv_msg

                msg = "from %s:%s:|%s\n" %(self.opaddress[0], self.opaddress[1], recv_data)
                self.show_msg("write", msg)
                # self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
            else:
                self.socket.close()
                msg = "从服务器断开连接"
                self.show_msg("statusmsg", msg)
                # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)
                break

    def send(self,data,cl=()):
        """
        功能函数，用于TCP客户端发送消息
        :return: None
        """
        if self._link is False:
            msg = '请选择服务，并点击连接网络'
            self.show_msg("statusmsg", msg)
            # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)
        else:
            try:
                if self._isHexSend:
                    # if len(data) == 1:
                    #     return
                    # send_data = self.str_to_hex(data)
                    send_data = self.decode_to_hex(data)
                else:
                    send_data = data
                self.socket.send(send_data)

                if self._isHexDisplay:
                    send_data = self.encode_to_hex(send_data)


                msg = "sendto %s:%s|%s\n" % (self.opaddress[0], self.opaddress[1], send_data)
                self.show_msg("write", msg)
                # self.emit(QtCore.SIGNAL("signal_write_msg"), msg)

            except Exception as ret:
                # print ret
                msg = "发送失败:%s"%(ret.errno)
                self.show_msg("statusmsg", msg)
                # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)


    def close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """

        ##选择为tcp客户端
        try:
            self.socket.shutdown(2)
            self.socket.close()
            if self._link is True:
                msg = "已断开网络"
                self.show_msg("statusmsg", msg)
                self.show_msg("status")
                # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)
        except Exception as ret:
            if self._isDebug:
                print ret
            pass

        try:
            stopThreading.stop_thread(self.client_th)
        except Exception:
            pass

    # def __del__(self):
    #     del self.socket
    #     del self.socket_th
    #     del self.opaddress
    #     print "tcp--client __del__"