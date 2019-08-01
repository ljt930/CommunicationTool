#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/6/5 21:05
# @Author  : linjinting
# @Site    : 
# @Software: CommunicationTool
# @File    : UDPServerBase.py
# @Function:
import datetime
import threading
import stopThreading
import select
from communicationserverbase import CommunicationServerBase
from TrasitionBase.CharactersConversion import CharactersConversion as CC


class ClientConn():
    def __init__(self):
        self.key = ""
        self.address = ()
        self.time_stamp = datetime.datetime.now()


class UDPServerBase(CommunicationServerBase):
    def __init__(self):
        super(UDPServerBase, self).__init__()
        self.client_socket_list = list()
        self.socket = None



    def open(self):
        """
        开启UDP服务端方法
        :return:
        """
        print("UDPServer::open")
        self.socket = self._socket.socket(self._socket.AF_INET, self._socket.SOCK_DGRAM)
        self.socket.settimeout(3)
        # self.socket.setsockopt()
        try:
            # port = int(self.lineEdit_port.text())
            # print self.address
            print(self._ip, self._port)
            self.socket.bind((self._ip, self._port))
        except self._socket.error as ret:

            msg = "请检查：[error %s]" % (ret.errno)
            self.show_msg("statusmsg", msg)
            # self.emit(QtCore.SIGNAL("signal_show_statusmsg"), msg)
            return -3

        else:
            # self.link = True
            self.socket_th = threading.Thread(target=self.udp_concurrency)
            self.socket_th.start()
            self.checked_client()
            # self.checked_timer = threading.Timer(1,self.checked_client)
            # self.checked_timer.start()
            msg = "UDP服务端正在监听端口:%s" % (self._port)
            self.show_msg("status", msg)
            # self.emit(QtCore.SIGNAL("signal_show_status"), msg)
            return 3

    def checked_client(self):
        """
        用于创建一个线程定期检测udp服务端，是否收到客户端数据。超时没收到数据则判断该客户端断开连接
        :return:
        """

        if self.client_conns:
            for key in list(self.client_conns.keys()):
                _conn = self.getCookie(key)

                stamp = _conn.time_stamp + datetime.timedelta(seconds=120)
                if stamp < datetime.datetime.now():
                    self.unsetCookie(key)
        # 开启定时器线程
        self.checked_timer = threading.Timer(120, self.checked_client)
        self.checked_timer.start()

    def udp_concurrency(self):
        """
        用于创建一个线程持续监听UDP通信
        :return:
        """
        inputs = [self.socket]

        while True:
            try:
                r_list, w_list, e_list = select.select(inputs, [], [], )
            except Exception as ret:
                print(ret)
                self.client_conns = dict()
                break
            else:
                # print w_list
                for e in e_list: continue

                try:
                    recv_msg, client_address = self.socket.recvfrom(1024)

                except Exception as ret:
                    print(ret)

                else:
                    self.new_data(recv_msg, client_address)

        print("server Thread exit")

    def new_data(self, recv_msg, client_address):
        """
        接收到新的数据后，用于处理数据方法
        :param recv_msg: 接收到的数据
        :param client_address: 数据源地址
        :return:
        """

        _key = CC.strip("[UDP]", client_address)
        _conn = self.getCookie(_key)
        if _conn:
            # 如果是已经存在的客户端连接，则更新其时间戳标志
            _conn.time_stamp = datetime.datetime.now()
        else:
            _conn = ClientConn()
            _conn.address = client_address
            _conn.key = _key

            self.setCookie(_key, _conn)

        msg = "收到客户端信息-IP:%s端口:%s" % (client_address[0], client_address[1])
        self.show_msg("statusmsg", msg)

        if self._isHexDisplay:
            recv_msg = CC.encode_to_hex(recv_msg)

        msg = "from %s:%s|%s" % (client_address[0], client_address[1], recv_msg)
        self.show_msg("write", msg)

        # udp收到信息自动回复
        if self._isAutoRecv:
            self._socket.sendto(recv_msg, (client_address[0], client_address[1]))


    #       odl
    # def udp_concurrency(self):
    #     """
    #     用于创建一个线程持续监听UDP通信
    #     :return:
    #     """
    #     while True:
    #         try:
    #             # print self.address
    #             recv_msg, client_addr = self.socket.recvfrom(1024)
    #             # if not recv_msg :
    #             #     print "exit"
    #             #     break
    #             if (self.socket,client_addr) not in self.client_socket_list:
    #                 # print client_addr
    #                 self.client_socket_list.append((self.socket,client_addr))
    #                 self.show_msg("addclient")
    #                 # self.emit(QtCore.SIGNAL("signal_addclient"))
    #
    #
    #             if self._isHexDisplay:
    #                 recv_msg = self.encode_to_hex(recv_msg)
    #
    #             msg = "from %s:%s|%s" % (client_addr[0], client_addr[1], recv_msg)
    #             self.show_msg("write", msg)
    #             # self.emit(QtCore.SIGNAL("signal_write_msg"), msg,client_addr)
    #         except self._socket.timeout:
    #             # print "time out"
    #             continue
    #         except Exception,e:
    #             print e
    #             break
    #
    #         #udp收到信息自动回复
    #         if self._isAutoRecv:
    #             self.socket.sendto(recv_msg, (client_addr[0], client_addr[1]))
    #
    #     print "server Thread exit"


    def send(self, data, keys=()):
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
                send_data = data

            if self._isHexDisplay:
                send_data = CC.encode_to_hex(send_data)

            for key in keys:
                _conn = self.getCookie(key)
                res = self.socket_send(send_data, _conn)
                # self.address = client_addr
                if res == 0:
                    if self._isHexDisplay:
                        show_data = CC.encode_to_hex(send_data)
                    else:
                        show_data = send_data

                    msg = "sendto %s:%s|%s" % (_conn.address[0], _conn.address[1], show_data)
                    self.show_msg("write", msg)
                    # self.emit(QtCore.SIGNAL("signal_write_msg"), msg)
        except Exception as ret:
            print(ret)


    def socket_send(self, send_data, _conn):
        """

        :rtype: object
        """
        try:
            self.socket.sendto(send_data, _conn.address)
            return 0
        except self._socket.error as ret:
            msg = "failed sendto %s:%s|%s" % (_conn.address[0], _conn.address[1], ret)
            self.show_msg("statusmsg", msg)
            return -1

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
                print(ret)
            pass

        self.checked_timer.cancel()

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


if __name__ == '__main__':
    conn = ClientConn()
    print(conn.key)
    print(conn.time_stamp)
