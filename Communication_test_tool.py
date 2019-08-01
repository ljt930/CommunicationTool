#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/5/27 16:53
# @Author  : linjinting
# @Site    :
# @Software: CommunicationTool
# @File    : Communication_test_tool.py
# @Function:

import sys
# from PyQt4 import QtCore, QtGui
from PyQt5 import QtWidgets,QtGui
from UI.UI_networkmain import Ui_MainWindow
from TrasitionBase.CharactersConversion import CharactersConversion
import TCPServer
import TCPClient
import UDPServer
import UDPClient
import threading
import stopThreading


# 修改默认编码为"utf-8"
# default_encoding = "utf-8"
# if (default_encoding != sys.getdefaultencoding()):
#     reload(sys)
#     sys.setdefaultencoding(default_encoding)


class Communication_test_tool(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Communication_test_tool, self).__init__()
        self.setupUi(self)
        # ChannelStat状态 0 无连接或无监听，1监听中，2连接中，-1监听失败，-2连接失败
        self.ChannelStat = 0
        self.isDebug = False
        self.channel = None
        self.channelType = None
        self.checkbox_flag = False
        self.client_socket_dict = dict()

        self.initsingle()
        self.inistatusBar()
        self.initwidget()
        self.createSocket()

    def initsingle(self):
        self.pushButton_listen.clicked.connect(self.server_op)
        self.pushButton_client.clicked.connect(self.client_op)
        self.pushButton_send.clicked.connect(self.send_data)
        self.pushButton_test.clicked.connect(self.testnet)
        self.pushButton_clear_recv.clicked.connect(self.clear_recv)
        self.pushButton_clear_send.clicked.connect(self.clear_send)
        self.pushButton_stopdisaply.clicked.connect(self.stop_disaply)
        self.pushButton_allselect.clicked.connect(self.select_all_client)

        self.checkBox_ishex_send.stateChanged.connect(self.setHexSend)
        self.checkBox_ishex_recv.stateChanged.connect(self.setHexRecv)
        self.checkBox_replysourcedata.stateChanged.connect(self.setAutoRecv)
        self.checkBox_auotsend.stateChanged.connect(self.auto_send)

        self.comboBox_net.currentIndexChanged.connect(self.createSocket)


    def initwidget(self):
        self.pushButton_send.setEnabled(False)
        self.checkBox_auotsend.setEnabled(False)
        self.initwidget_server()

        self.listWidget_clientlist.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)

    def inistatusBar(self):
        self.label_channelstat = QtWidgets.QLabel()
        # self.lineEdit_ip.setMinimumSize(QtCore.QSize(350, 0))
        self.statusBar().addPermanentWidget(self.label_channelstat)

    def initwidget_server(self):
        self.widget_setting_client.hide()
        self.checkBox_islocalport.hide()
        self.pushButton_listen.show()
        self.groupBox_CurrentConnection.show()

    def initwidget_client(self):
        self.widget_setting_client.show()
        self.checkBox_islocalport.show()
        self.pushButton_listen.hide()
        self.groupBox_CurrentConnection.hide()

    def createSocket(self):
        """
        功能函数，根据选择不同的网络通道，创建self.channel
        :return:
        """
        self.channel = None
        if self.comboBox_net.currentIndex() == 0:
            self.channel = TCPServer.TCPServer()
            self.channelType = "[TCP]"
            self.initwidget_server()
            self.channel.signal_client_change.connect(self.show_clientlist)

        if self.comboBox_net.currentIndex() == 1:
            self.channel = TCPClient.TCPClient()
            self.channelType = "[TCP]"
            self.initwidget_client()
            self.channel.signal_client_disconn.connect(self.show_client_disconn)

        if self.comboBox_net.currentIndex() == 2:
            self.channel = UDPServer.UDPServer()
            self.channelType = "[UDP]"
            self.initwidget_server()
            self.channel.signal_client_change.connect(self.show_clientlist)

        if self.comboBox_net.currentIndex() == 3:
            self.channel = UDPClient.UDPClient()
            self.channelType = "[UDP]"
            self.initwidget_client()

        if self.isDebug:
            self.channel.setDebug()

        self.channel.signal_show_status.connect(self.show_status)
        self.channel.signal_show_statusmsg.connect(self.show_statusmsg)
        self.channel.signal_write_msg.connect(self.show_revc_msg)


        # self.channel.signal_client_disconn.connect(self.show_client_disconn)

        # self.server_op()
        # self.connect(self._channel, QtCore.SIGNAL("signal_show_stat"), self.showstat)
        # self._channel.setAddress("",12345)
        # self._channel.open()


    def testnet(self):
        pass
        # if self.checkBox_auotsend.isChecked():
        #     self.checkBox_auotsend.setChecked(False)
        # else:
        #     self.checkBox_auotsend.setChecked(True)


    def server_op(self):
        ip = self.lineEdit_ip.text()
        port = int(self.lineEdit_port.text())

        if self.ChannelStat <= 0:
            self.channel.setAddress(ip, port)
            self.ChannelStat = self.channel.open()

        else:
            self.channel.close()
            self.ChannelStat = 0

        if self.ChannelStat > 0:
            self.pushButton_listen.setText("停止")
            self.setWidgetStatus_open()
        else:
            self.pushButton_listen.setText("启动")
            self.setWidgetStatus_close()
            self.checkBox_auotsend.setChecked(False)


    def client_op(self):

        opip = self.lineEdit_opip.text()
        opport = int(self.lineEdit_opport.text())

        if self.ChannelStat <= 0:
            self.channel.setopAddress(opip, opport)
            if self.checkBox_islocalport.isChecked():
                ip = self.lineEdit_ip.text()
                port = int(self.lineEdit_port.text())
                self.channel.setAddress(ip, port)

            self.ChannelStat = self.channel.open()
        else:
            self.channel.close()
            self.ChannelStat = 0

        if self.ChannelStat > 0:
            self.pushButton_client.setText("停止")
            self.setWidgetStatus_open()

        else:
            self.pushButton_client.setText("连接")
            self.setWidgetStatus_close()

    def setWidgetStatus_open(self):
        self.pushButton_send.setEnabled(True)
        self.checkBox_auotsend.setEnabled(True)
        self.comboBox_net.setEnabled(False)

    def setWidgetStatus_close(self):
        self.pushButton_send.setEnabled(False)
        self.checkBox_auotsend.setEnabled(False)
        self.comboBox_net.setEnabled(True)
        self.listWidget_clientlist.clear()


    def send_data(self):
        data = self.textEdit_send.toPlainText()
        client_list = list()

        if self.listWidget_clientlist.selectedItems():
            for item in self.listWidget_clientlist.selectedItems():
                client_key = item.text()
                client_list.append(client_key)

        if self.ChannelStat > 0:
            if len(data) == 0:

                # print self.checkBox_auotsend.isChecked()
                return
            self.channel.send(data, client_list)


    def select_all_client(self):
        self.listWidget_clientlist.selectAll()
        print(self.listWidget_clientlist.selectedItems())


    def clear_send(self):
        if self.checkBox_auotsend.isChecked():
            return
        self.textEdit_send.clear()


    def stop_disaply(self):
        if self.ChannelStat > 0:
            text = self.pushButton_stopdisaply.text()
            if text == "暂停显示":
                self.channel.setStopDisplay(True)
                self.pushButton_stopdisaply.setText("恢复显示")
            else:
                self.channel.setStopDisplay(False)
                self.pushButton_stopdisaply.setText("暂停显示")


    def clear_recv(self):
        self.textEdit_recv.clear()

    def show_clientlist(self):
        self.listWidget_clientlist.clear()
        self.client_socket_dict = dict()
        # print self.channel.client_socket_list
        conns = self.channel.client_conns

        if conns:
            for key in list(conns.keys()):
                self.listWidget_clientlist.addItem(key)

    def show_client_disconn(self):
        self.ChannelStat = 0
        self.pushButton_client.setText("连接")
        self.setWidgetStatus_close()

    def show_status(self, msg):
        # msg = msg.decode("utf-8")
        # self.inistatusBar()

        self.label_channelstat.setText(msg)
        self.statusBar().showMessage(msg, 5000)

    def show_statusmsg(self, msg):

        # msg = msg.decode("utf-8")
        self.statusBar().showMessage(msg, 5000)

    def show_revc_msg(self, msg):
        try:
            msg = msg.decode('utf-8')
        except BaseException:
            pass

        self.textEdit_recv.insertPlainText(msg)
        self.textEdit_recv.insertPlainText("\n")
        self.textEdit_recv.moveCursor(QtGui.QTextCursor.End)

    def auto_send(self):
        # self.checkBox_auotsend.setChecked(True)
        data = self.textEdit_send.toPlainText()

        if self.checkbox_flag:
            return
        if self.ChannelStat > 0:
            if len(data) == 0:
                self.checkbox_flag = True
                self.checkBox_auotsend.nextCheckState()
                self.checkbox_flag = False
            else:
                self.send_data()
        if self.checkBox_auotsend.isChecked():
            self.pushButton_send.setEnabled(False)
            self.textEdit_send.setEnabled(False)
            self.pushButton_disconn.setEnabled(False)
        else:
            self.pushButton_send.setEnabled(True)
            self.textEdit_send.setEnabled(True)
            self.pushButton_disconn.setEnabled(True)
            return

        if self.checkBox_auotsend.isChecked():
            time_ = int(self.lineEdit_interval.text()) / 1000
            # print('当前线程数为{}'.format(threading.activeCount()))
            self.send_th = send_th = threading.Timer(time_, self.auto_send)
            send_th.start()

        # self.checkbox_test()

        # print "auto_send:::!2313"

    def checkbox_test(self):
        print((self.checkBox_auotsend.nextCheckState()))
        if self.checkBox_auotsend.isChecked():
            self.checkBox_auotsend.nextCheckState()
        print((self.checkBox_auotsend.isChecked()))

    def setAutoRecv(self):
        self.channel.setAutoRecv(self.checkBox_replysourcedata.isChecked())

    def setHexSend(self, value):
        # if self.checkBox_ishex_recv.isChecked():
        self.channel.setHexSend(self.checkBox_ishex_send.isChecked())

    def setHexRecv(self, value):
        # if self.checkBox_ishex_recv.isChecked():
        self.channel.setHexDisplay(self.checkBox_ishex_recv.isChecked())

    def closeEvent(self, event):
        print("__del__")
        if self.checkBox_auotsend.isChecked():
            self.checkBox_auotsend.setCheckable(False)
        try:
            self.channel.close()
            del self.channel
        except BaseException:
            pass
        try:
            stopThreading.stop_thread(self.send_th)
        except Exception:
            pass
        event.accept()
        # sys.exit(100)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Communication_test_tool()
    window.show()
    app.exec_()

    sys.exit(100)
