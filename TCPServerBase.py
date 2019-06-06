#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/5/28 11:28
# @Author  : linjinting
# @Site    : 
# @Software: CommunicationTool
# @File    : TCPServer.py
# @Function: TCPServer


import threading
import stopThreading
from communicationBase import communicationBase

class TCPServerBase(communicationBase):
    def __init__(self):
        super(TCPServerBase, self).__init__()
        # communicationBase.__init__(self)

        self.client_socket_list = list()
        self.socket = None
        self.client_count = 0

    def open(self):
        """
        功能函数，TCP服务端开启的方法
        :return: None
        """
        print "TCPServer::open"
        self.socket = self._socket.socket(self._socket.AF_INET, self._socket.SOCK_STREAM)
        # 取消主动断开连接四次握手后的TIME_WAIT状态
        self.socket.setsockopt(self._socket.SOL_SOCKET, self._socket.SO_REUSEADDR, 1)
        # 设定套接字为非阻塞式
        self.socket.setblocking(False)
        try:
            # port = int(self.lineEdit_port.text())
            self.socket.bind((self._ip, self._port))
        except Exception as ret:
            msg = "监听失败，请检查端口号:%s"% (self._port)
            self.show_msg("statusmsg", msg)
            # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)
            return -1
        else:
            self.socket.listen(128)
            self.socket_th = threading.Thread(target=self.tcp_server_concurrency)
            self.socket_th.start()
            msg = 'TCP服务端正在监听端口:%s' % self._port
            self.show_msg("status", msg)
            # self.emit(QtCore.SIGNAL("signal_show_status"), msg)
            return 1

    def tcp_server_concurrency(self):
        """
        功能函数，供创建线程的方法；
        ，使主线程可以继续运行，以免无响应
        使用非阻塞式并发用于接收客使用子线程用于监听并创建连接户端消息，减少系统资源浪费，使软件轻量化
        :return:None
        """

        while True:
            try:
                client_socket, client_address = self.socket.accept()
                print "accept"
            except Exception as ret:
                print ret
                break
                # if self._isDebug:
                #     print ret
                pass
            else:
                # client_socket.setblocking(False)
                # 将创建的客户端套接字存入列表,client_address为ip和端口的元组
                self.client_socket_list.append((client_socket, client_address))
                self.client_count +=1
                client_th = threading.Thread(target=self.clientsocket_concurrency,args=(client_socket, client_address))
                client_th.start()
                msg = '客户端-%sIP:%s端口:%s,已连接' % (self.client_count,client_address[0],client_address[1])
                self.show_msg("statusmsg", msg)
                self.show_msg("addclient")
                # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)
                # self.emit(QtCore.SIGNAL("signal_addclient"))

        print "tcp_server_concurrency"

    def clientsocket_concurrency(self,client,client_addr):
        """
        功能函数，供创建线程的方法；
        使用子线程用于监听TCP通讯信息，使主线程可以继续运行，以免无响应
        使用非阻塞式并发用于接收客户端消息，减少系统资源浪费，使软件轻量化
        :return:None
        """
        while True:
            try:
                recv_msg = client.recv(1024)
                print "recv"
            except Exception as ret:
                if 9 == ret.errno:
                    print "Error 9"
                    break
                if self._isDebug:
                    print "CLIENT"+ str(ret)
                # break
            else:
                if recv_msg:
                    # receive_data = recv_msg.decode('utf-8')
                    # receive_data = recv_msg.encode('hex')
                    if self._isAutoRecv:
                        client.send(recv_msg)

                    if self._isHexDisplay:
                        recv_data = self.encode_to_hex(recv_msg)
                    else:
                        recv_data = recv_msg

                    msg = "from %s:%s|%s\n" % (client_addr[0], client_addr[1], recv_data)
                    self.show_msg("write", msg)
                    # self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
                    # print msg
                else:
                    msg = "客户端-%sIP:%s端口:%s,已断开连接" % (self.client_count,client_addr[0], client_addr[1])
                    self.show_msg("statusmsg",msg)

                    # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)
                    client.close()
                    self.client_socket_list.remove((client, client_addr))
                    self.show_msg("addclient")
                    # self.emit(QtCore.SIGNAL("signal_addclient"))
                    break

        print "client:%s thread exit"%(self.client_count)
        self.client_count -= 1

    def send(self,data,cl=()):
        """
        功能函数，用于TCP服务端
        :return: None
        """
        if self.client_socket_list:
            try:
                # send_data = (str(self.textEdit_send.toPlainText())).encode('utf-8')
                if cl:
                    client_socket_list = cl
                else:
                    client_socket_list = self.client_socket_list

                if self._isHexSend:
                    send_data = self.decode_to_hex(data)
                else:
                    send_data = data



                # 向所有连接的客户端发送消息
                for client, client_addr in client_socket_list:
                    client.send(send_data)

                    if self._isHexDisplay:
                        show_data = self.encode_to_hex(send_data)
                    else:
                        show_data = send_data

                    msg = "sendto %s:%s|%s\n" % (client_addr[0], client_addr[1], show_data)

                    self.show_msg("write", msg)
                    # self.emit(QtCore.SIGNAL("signal_write_msg"), msg)

            except Exception as ret:
                msg = "发送失败:%s"%(ret)
                self.show_msg("statusmsg", msg)
                # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)

        else:
            msg = "未发现已连接的客户端，无法发送"
            self.show_msg("statusmsg", msg)
            # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)


    def close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """

        try:
            for client, address in self.client_socket_list:
            #     try:
            #     client.shutdown(2)
                client.close()
            #     except Exception as ret:
            #         print ret
            #         pass
            # self.socket.shutdown(2)
            self.socket.close()
            msg = "已断开网络"
            self.show_msg("statusmsg",msg)
            self.show_msg("status")
            # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)
            # self.emit(QtCore.SIGNAL("signal_show_status"), "")
        except Exception as ret:
            print ret.strerror.decode("gbk")
            # if self._isDebug:
            #     print ret
            pass

        try:
            stopThreading.stop_thread(self.socket_th)
        except Exception:
            pass

    # def __del__(self):
    #     del self.socket
    #     del self.socket_th
    #     del self.address
    #     del self.client_socket_list
    #     print "tcp--server __del__"

if __name__ == '__main__':
    tcps = TCPServerBase()
    tcps.setAddress("127.0.0.1",5566)
    tcps.open()