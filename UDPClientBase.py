#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/6/5 21:19
# @Author  : linjinting
# @Site    : 
# @Software: CommunicationTool
# @File    : UDPClientBase.py
# @Function:

import socket
import threading
import stopThreading
from communicationBase import communicationBase

class UDPClientBase(communicationBase):
    def __init__(self):
        super(UDPClientBase, self).__init__()

        # self.open()


    def open(self):
        """
        开启UDP客户端方法
        :return:
        """
        print "UDPClient::open"

        self.socket = self._socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(3)
        try:
            self.opaddress = (self._opip, self._opport)
            if self._islocaladdress:
                self.setAddress = (self._ip, self._port)
                # local_port = random.randint(49152, 65535)
                self.socket.bind(self.setAddress)
        except Exception as ret:
            msg = "请检查IP，端口"
            self.show_msg("statusmsg",msg)
            # self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
            return -2
        else:
            msg = "UDP客户端已启动"
            self.show_msg("statusmsg", msg)
            # self.emit(QtCore.SIGNAL("signal_show_status"), msg)
            self.socket_th = threading.Thread(target=self.udp_concurrency)
            self.socket_th.start()
            return 2

    def udp_concurrency(self):
        while True:
            try:
                recv_msg, client_addr = self.socket.recvfrom(1024)
                if self._isHexDisplay:
                    recv_msg = self.encode_to_hex(recv_msg)

                msg = "from %s:%s|%s\n" % (client_addr[0], client_addr[1], recv_msg)
                self.show_msg("write", msg)
                # self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
            except self._socket.timeout:
                print "timeout"
                continue

            except Exception, e:
                if e.errno == 10054:
                    print 10054
                    continue
                else:
                    print e
                    break
        print "upd client revc exit"

    def send(self,data):
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


            self.socket.sendto(send_data, self.opaddress)
            msg = "sendto %s:%s|%s\n" % (self.opaddress[0], self.opaddress[1], send_data)
            self.show_msg("write", msg)
            # self.emit(QtCore.SIGNAL("signal_write_msg"), msg)


        except Exception as ret:
            msg = "failed sendto %s:%s|%s\n" % (self.opaddress[0], self.opaddress[1], ret)
            self.show_msg("statusmsg", msg)
            # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)

    def close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        try:

            # self.socket.shutdown(2)
            self.socket.close()
            msg = "已断开网络"
            self.show_msg("statusmsg", msg)
            self.show_msg("status")
            # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)
            # self.emit(QtCore.SIGNAL("signal_show_status"), "")
        except Exception as ret:
            # if self._isDebug:
            print ret
            pass


        try:
            stopThreading.stop_thread(self.socket_th)
        except Exception:
            pass

    # def __del__(self):
    #     del self.socket
    #     del self.socket_th
    #     del self.opaddress
    #     print "udp--client __del__"

if __name__ == '__main__':
    c = UDPClientBase()
    c.setopAddress("127.0.0.1",2500)
    c.open()