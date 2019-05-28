#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/20 20:12
# @Author  : Aries
# @Site    : 
# @File    : TCPServer.py
# @Software: PyCharm
# 原文：https://blog.csdn.net/u010139869/article/details/79505892

import socket
import threading
import stopThreading
from PyQt4 import QtCore

class TcpServer_old(QtCore.QThread):
    # signal.signal()
    signal_write_msg = QtCore.SIGNAL("signal_write_msg")
    def __init__(self):
        super(TcpServer_old, self).__init__()
        self.tcp_socket = None
        self.sever_th = None
        self.client_th = None
        self.client_socket_list = list()

        self.link = False  # 用于标记是否开启了连接


    def server_start(self,port):
        """
        功能函数，TCP服务端开启的方法
        :return: None
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 取消主动断开连接四次握手后的TIME_WAIT状态
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设定套接字为非阻塞式
        self.tcp_socket.setblocking(False)
        try:
            # port = int(self.lineEdit_port.text())
            self.tcp_socket.bind(('', port))
        except Exception as ret:
            msg = '请检查端口号\n'
            self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
        else:
            self.tcp_socket.listen(128)
            self.sever_th = threading.Thread(target=self.tcp_server_concurrency)
            self.sever_th.start()
            msg = 'TCP服务端正在监听端口:%s\n' % str(port)
            self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
            # self.signal_write_msg.emit(msg)
            # print msg

    def tcp_server_concurrency(self):
        """
        功能函数，供创建线程的方法；
        使用子线程用于监听并创建连接，使主线程可以继续运行，以免无响应
        使用非阻塞式并发用于接收客户端消息，减少系统资源浪费，使软件轻量化
        :return:None
        """
        while True:
            try:
                client_socket, client_address = self.tcp_socket.accept()
            except Exception as ret:
                pass
            else:
                client_socket.setblocking(False)
                # 将创建的客户端套接字存入列表,client_address为ip和端口的元组
                self.client_socket_list.append((client_socket, client_address))
                msg = '客户端IP:%s端口:%s已连接\n' % client_address

                self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
            # 轮询客户端套接字列表，接收数据
            for client, client_addr in self.client_socket_list:
                try:
                    recv_msg = client.recv(1024)
                except Exception as ret:
                    pass
                else:
                    if recv_msg:
                        # receive_data = recv_msg.decode('utf-8')
                        receive_data = recv_msg.encode('hex')
                        # receive_data = ' '.join([hex(ord(c)).replace('0x', '') for c in recv_msg])
                        msg = "from %s:%s|%s\n" % (client_addr[0], client_addr[1], receive_data)
                        self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
                        # print msg
                    else:
                        msg = "客户端IP:%s端口:%s已断开连接\n" % (client_addr[0], client_addr[1])
                        self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
                        client.close()
                        self.client_socket_list.remove((client, client_addr))


    def client_start(self, ip, port):
        """
        功能函数，TCP客户端连接其他服务端的方法
        :return:
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.address = (ip, port)
        except Exception as ret:
            msg = '请检查目标IP，目标端口\n'
            self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
        else:
            try:
                msg = '正在连接目标服务器\n'
                # self.signal_write_msg.emit(msg)
                self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
                self.tcp_socket.connect( self.address)
            except Exception as ret:
                msg = '无法连接目标服务器\n'+ret.message
                self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
            else:
                self.client_th = threading.Thread(target=self.tcp_client_concurrency)
                self.client_th.start()
                msg = 'TCP客户端已连接IP:%s端口:%s\n' %  self.address
                self.emit(QtCore.SIGNAL("signal_write_msg"), msg)

    def tcp_client_concurrency(self):
        """
        功能函数，用于TCP客户端创建子线程的方法，阻塞式接收
        :return:
        """
        while True:
            recv_msg = self.tcp_socket.recv(1024)
            if recv_msg:
                msg = recv_msg.decode('utf-8')
                msg = "from %s:%s:|%s\n" %( self.address[0],  self.address[1], msg)
                self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
            else:
                self.tcp_socket.close()
                self.reset()
                msg = '从服务器断开连接\n'
                self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
                break

    def send(self,send_data,isser=False):
        """
        功能函数，用于TCP服务端和TCP客户端发送消息
        :return: None
        """
        if self.link is False:
            msg = '请选择服务，并点击连接网络\n'
            self.signal_write_msg.emit(msg)
        else:
            try:
                # send_data = (str(self.textEdit_send.toPlainText())).encode('utf-8')
                if isser:
                    # 向所有连接的客户端发送消息
                    for client, client_addr in self.client_socket_list:
                        client.send(send_data)
                    msg = "sendto %s:%s|%s\n" % (client_addr[0], client_addr[1], send_data)
                    self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
                else:
                    self.tcp_socket.send(send_data)
                    msg = "sendto %s:%s|%s\n" % ( self.address[0],  self.address[1], send_data)
                    self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
            except Exception as ret:
                msg = '发送失败:%s\n'
                self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
    def setisHex(self,isHex):
        self.isHex=isHex
    def ser_close(self,isser):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        ##选择为tcp服务端
        if isser :
            try:
                # for client, address in self.client_socket_list:
                #     client.close()
                self.tcp_socket.close()
                if self.link is True:
                    msg = '已断开网络\n'
                    self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
            except Exception as ret:
                pass
        ##选择为tcp客户端
        else:
            try:
                self.tcp_socket.close()
                if self.link is True:
                    msg = '已断开网络\n'
                    self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
            except Exception as ret:
                pass
        try:
            stopThreading.stop_thread(self.sever_th)
        except Exception:
            pass
        try:
            stopThreading.stop_thread(self.client_th)
        except Exception:
            pass




if __name__ == '__main__':
    port = 8125     # 指定端口
    # main(8125)
    ser = TcpServer_old()
    ser.tcp_server_start(port)
    ser.link = True

