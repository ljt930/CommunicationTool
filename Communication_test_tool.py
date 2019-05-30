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
from PyQt4 import QtCore, QtGui
from UI.UI_networkmain import Ui_MainWindow
from TrasitionBase.CharactersConversion import CharactersConversion
import TCPServer,TCPClient,UDPServer,UDPClient


# 修改默认编码为"utf-8"
default_encoding = "utf-8"
if (default_encoding != sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class Communication_test_tool(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Communication_test_tool,self).__init__()

        self.setupUi(self)

        # self.inistatusBar()
        self.createSocket()
        self.initsingle()

    def inistatusBar(self):
        self.label_channelstat = QtGui.QLabel()
        # self.lineEdit_ip.setMinimumSize(QtCore.QSize(350, 0))
        self.statusBar().addWidget(self.label_channelstat)
        self.label_channelstat2 = QtGui.QLabel()
        self.statusBar().addWidget(self.label_channelstat2)

    def initsingle(self):
        self.connect(self.pushButton_listen, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("start()"))
        self.connect(self.pushButton_client, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("stop()"))
        # self.connect(self.pushButton_send, QtCore.SIGNAL("clicked()"),
        #              self, QtCore.SLOT("sendmsg()"))
        # self.connect(self.pushButton_test, QtCore.SIGNAL("clicked()"),
        #              self, QtCore.SLOT("testnet()"))
        # self.connect(self.pushButton_clear_recv, QtCore.SIGNAL("clicked()"),
        #              self, QtCore.SLOT("clearrecv()"))
        # self.connect(self.pushButton_clear_send, QtCore.SIGNAL("clicked()"),
        #              self, QtCore.SLOT("clearsend()"))
        # self.connect(self.comboBox_net,QtCore.SLOT("currentIndexChanged()"),self, QtCore.SLOT("combobox_change()"))
        self.comboBox_net.currentIndexChanged.connect(self.createSocket)
        # self.checkBox_ishex_recv.stateChanged.connect(self.sethexrecvshow)

    def createSocket(self):

        if self.comboBox_net.currentIndex() == 0:
            self._channel = TCPServer.TCPServer()
        if self.comboBox_net.currentIndex() == 1:
            self._channel = TCPClient.TCPClient()
        if self.comboBox_net.currentIndex() == 2:
            self._channel = UDPServer.UDPServer()
        if self.comboBox_net.currentIndex() == 3:
            self._channel = UDPClient.UDPClient()

        self.connect(self._channel, QtCore.SIGNAL("signal_show_stat"),self.show_stat)
        self.connect(self._channel, QtCore.SIGNAL("signal_write_msg"), self.show_revc_msg)
        # self.connect(self._channel, QtCore.SIGNAL("signal_show_stat"), self.showstat)
        # self._channel.setAddress("",12345)
        # self._channel.open()

    @QtCore.pyqtSlot()
    def start(self):
        self._channel.setAddress("127.0.0.1", 3344)
        self._channel.open()

    @QtCore.pyqtSlot()
    def stop(self):
        # self._channel.setAddress("", 12345)
        self._channel.close()

    def show_stat(self,msg):

        msg = msg.decode("utf-8")
        self.inistatusBar()

        self.label_channelstat.setText(msg)
        # self.statusBar().showMessage(msg)

    def show_revc_msg(self, msg):

        msg=msg.decode('utf-8')
        self.textEdit_recv.insertPlainText(msg)
        self.textEdit_recv.moveCursor(QtGui.QTextCursor.End)




if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Communication_test_tool()
    window.show()
    sys.exit(app.exec_())