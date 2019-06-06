#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/6/5 21:05
# @Author  : linjinting
# @Site    : 
# @Software: CommunicationTool
# @File    : UDPServerBase.py
# @Function:
import socket
import threading
import stopThreading
from communicationBase import communicationBase

class UDPServerBase(communicationBase):
    def __init__(self):
        super(UDPServerBase,self).__init__()
        self.client_socket_list = list()
        self.socket = None

    def open(self):
        """
        开启UDP服务端方法
        :return:
        """
        print "UDPServer::open"
        self.socket = self._socket.socket(self._socket.AF_INET, self._socket.SOCK_DGRAM)
        self.socket.settimeout(3)
        # self.socket.setsockopt()
        try:
            # port = int(self.lineEdit_port.text())
            # print self.address
            print self._ip, self._port
            self.socket.bind((self._ip, self._port))
        except Exception as ret:

            msg = "请检查：[error %s]"%(ret.errno)
            self.show_msg("statusmsg", msg)
            # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)
            return -1

        else:
            # self.link = True
            self.socket_th = threading.Thread(target=self.udp_concurrency)
            self.socket_th.start()
            msg = "UDP服务端正在监听端口:%s" %(self._port)
            self.show_msg("status", msg)
            # self.emit(QtCore.SIGNAL("signal_show_status"), msg)
            return 1

    def udp_concurrency(self):
        """
        用于创建一个线程持续监听UDP通信
        :return:
        """
        while True:
            try:
                # print self.address
                recv_msg, client_addr = self.socket.recvfrom(1024)
                # if not recv_msg :
                #     print "exit"
                #     break
                if (self.socket,client_addr) not in self.client_socket_list:
                    # print client_addr
                    self.client_socket_list.append((self.socket,client_addr))
                    self.show_msg("addclient")
                    # self.emit(QtCore.SIGNAL("signal_addclient"))


                if self._isHexDisplay:
                    recv_msg = self.encode_to_hex(recv_msg)

                msg = "from %s:%s|%s\n" % (client_addr[0], client_addr[1], recv_msg)
                self.show_msg("write", msg)
                # self.emit(QtCore.SIGNAL("signal_write_msg"), msg,client_addr)
            except socket.timeout:
                # print "time out"
                continue
            except Exception,e:
                print e
                break

            #udp收到信息自动回复
            if self._isAutoRecv:
                self._socket.sendto(recv_msg, (client_addr[0], client_addr[1]))

        print "server Thread exit"


    def send(self,data,cl=()):
        # if self.link is False:
        #     msg = '请选择服务，并点击连接网络\n'
        #     self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
        # else:
        try:
            if self._isHexSend:
                # if len(data) == 1:
                #     return
                send_data = self.decode_to_hex(data)
            else:
                send_data = data

            if self._isHexDisplay:
                send_data = self.encode_to_hex(send_data)


            for socket__,client_addr in self.client_socket_list:
                # self.address = client_addr
                self.socket.sendto(send_data, client_addr)
                if self._isHexDisplay:
                    show_data = self.encode_to_hex(send_data)
                else:
                    show_data = send_data

                msg = "sendto %s:%s|%s\n" % (client_addr[0], client_addr[1], show_data)
                self.show_msg("write", msg)
                # self.emit(QtCore.SIGNAL("signal_write_msg"), msg)


        except Exception as ret:
            msg = "failed sendto %s:%s|%s" % (client_addr[0], client_addr[1],ret)
            self.show_msg("statusmsg", msg)
            # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)

    # def nterior_client(self):
    #     self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     try:
    #         # self.address = (ip, port)
    #         port = random.randint(49152, 65535)
    #         self.udp_socket.bind(('', port))
    #     except Exception as ret:
    #         return -3
    #     else:
    #         socket._closedsocket()
    #         return 3
    #     pass

    def close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        try:

            self.socket.shutdown(2)
            self.socket.close()
            msg = "已断开网络"
            self.show_msg("statusmsg", msg)
            self.show_msg("status")
            # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)
            # self.emit(QtCore.SIGNAL("signal_show_status"), "")
        except Exception as ret:
            if self._isDebug:
                print ret
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
    #     print "udp--server __del__"
