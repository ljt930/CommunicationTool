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
import select
from communicationbase import CommunicationBase
from TrasitionBase.CharactersConversion import CharactersConversion as CC


class UDPClientBase(CommunicationBase):
    def __init__(self):
        super(UDPClientBase, self).__init__()
        # self.iswait = False
        # self.istimeout = False
        # self.open()

    def open(self):
        """
        开启UDP客户端方法
        :return:
        """
        print("UDPClient::open")

        self.socket = self._socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.socket.settimeout(3)
        try:
            self.opaddress = (self._opip, self._opport)

            if self._islocaladdress:
                self.setAddress = (self._ip, self._port)
                self.socket.bind(self.setAddress)

        except self._socket.error as ret:
            msg = "请检查IP，端口:%s" % ret.errno
            self.show_msg("statusmsg", msg)
            # self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
            return -4
        else:
            msg = "UDP客户端已启动"
            self.show_msg("statusmsg", msg)
            # self.emit(QtCore.SIGNAL("signal_show_status"), msg)
            self.socket_th = threading.Thread(target=self.udp_concurrency)
            self.socket_th.start()
            return 4

    def udp_concurrency(self):
        """
        用于创建一个线程持续监听UDP通信,接收UDP数据，使用select方法
        :return:
        """
        inputs = [self.socket]
        # timeout = 3
        self.iswait = True
        self.istimeout = False
        while True:
            try:
                r_list, w_list, e_list = select.select(inputs, [], [],self._timeout)
                if r_list == []:
                    self.istimeout = True
                    break
            except Exception as ret:
                print(ret)
                break
            else:
                # print w_list
                for e in e_list:
                    continue

                try:
                    recv_msg, client_address = self.socket.recvfrom(1024)

                except Exception as ret:
                    # print(ret)
                    pass

                else:
                    if self._isHexDisplay:
                        show_data = CC.encode_to_hex(recv_msg)
                    else:
                        show_data = recv_msg.decode()

                    msg = "from %s:%s|%s" % (
                        client_address[0], client_address[1], show_data)
                    self.show_msg("write", msg)

        print("upd client revc exit")
        self.iswait = False
        # while True:
        #     try:
        #         recv_msg, client_addr = self.socket.recvfrom(1024)
        #         if self._isHexDisplay:
        #             recv_msg = CC.encode_to_hex(recv_msg)
        #
        #         msg = "from %s:%s|%s" % (client_addr[0], client_addr[1], recv_msg)
        #         self.show_msg("write", msg)
        #         # self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
        #     except self._socket.timeout:
        #         print "timeout"
        #         continue
        #
        #     except self._socket.error, e:
        #         if e.errno == 10054:
        #             print 10054
        #             continue
        #         else:
        #             print e
        #             break

    def send(self, data, cl=()):
        # if self.link is False:
        #     msg = '请选择服务，并点击连接网络\n'
        #     self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
        # else:
        try:
            if self._isHexSend:
                # if len(data) == 1:
                #     return
                send_data = CC.decode_to_hex(data)
            else:
                send_data = data.encode()
            self.socket.sendto(send_data, self.opaddress)

            if self._isHexDisplay:
                show_data = CC.encode_to_hex(send_data)
            else:
                show_data = data


            msg = "sendto %s:%s|%s" % (
                self.opaddress[0], self.opaddress[1], show_data)
            self.show_msg("write", msg)
            # self.emit(QtCore.SIGNAL("signal_write_msg"), msg)

        except Exception as ret:
            msg = "failed sendto %s:%s|%s" % (
                self.opaddress[0], self.opaddress[1], ret)
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
            print(ret)
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

    def check_recv(self):
        while True:
            if self.iswait :
                # print("check")
                pass
            else:
                break

        # print("check recv ok")
        if self.istimeout:
            return True
        else:
            return False

if __name__ == '__main__':
    c = UDPClientBase()
    c.setopAddress("127.0.0.1", 2500)
    c.open()

    c.send("11111111111111")
    c.close()
