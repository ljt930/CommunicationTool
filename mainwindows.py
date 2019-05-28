#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/20 20:32
# @Author  : Aries
# @Site    : 
# @File    : mainwindows.py
# @Software: PyCharm
import sys
import struct
import random
from PyQt4 import QtCore, QtGui
from UI.UI_networkmain import Ui_MainWindow
from TrasitionBase.CharactersConversion import CharactersConversion
import TCPServerOld,UDPServer_old
import time

# 修改默认编码为"utf-8"
default_encoding = "utf-8"
if (default_encoding != sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """b
    #方法二：先把ui文件转换成py文件。
    再通过继承 ui中的类Ui_MainWindow，直接初始化
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.initsingle()
        # self.isStartSer = False
        self.isser=True
        self.isHex = None
        self.netSer = None
        self.netCli = None
        self.CC = CharactersConversion()
        self.getconf()
        self.initWidget()


    def closeEvent(self, *args, **kwargs):

        print "main exit"

    def initWidget(self):
        self.pushButton_client.setEnabled(False)
        self.widget_setting_client.hide()
        self.checkBox_islocalport.hide()
        self.pushButton_send.setEnabled(False)
        # self.pushButton_client.hide()
        # self.lineEdit_objip.hide()
        # self.lineEdit_objport.hide()
        # self.label_optip.hide()
        # self.label_opport.hide()


        # self.pushButton_listen.hide()
        # self.lineEdit_ip.hide()
        # self.lineEdit_port.hide()
        # self.label_ip.hide()
        # self.label_port.hide()

        # self.pushButton_send.hide()
        # self.checkBox_ishex.hide()
        # self.comboBox_net.hide()

    def initsingle(self):
        self.connect(self.pushButton_listen, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("startorstop()"))
        self.connect(self.pushButton_client, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("connordisconn()"))
        self.connect(self.pushButton_send, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("sendmsg()"))
        self.connect(self.pushButton_test, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("testnet()"))
        self.connect(self.pushButton_clear_recv, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("clearrecv()"))
        self.connect(self.pushButton_clear_send, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("clearsend()"))
        # self.connect(self.comboBox_net,QtCore.SLOT("currentIndexChanged()"),self, QtCore.SLOT("combobox_change()"))
        self.comboBox_net.currentIndexChanged.connect(self.combobox_change)
        self.checkBox_ishex_recv.stateChanged.connect(self.sethexrecvshow)
    # @QtCore.pyqtSlot(str)
    def sethexrecvshow(self):
        print "sethex"
        if self.netSer is not None:
            self.netSer.setisHex(self.checkBox_ishex_recv.isChecked())
        if self.netCli is not None:
            self.netCli.setisHex(self.checkBox_ishex_recv.isChecked())

    def combobox_change(self):
        if self.comboBox_net.currentIndex() == 0 or self.comboBox_net.currentIndex() == 2:
            self.widget_setting_client.hide()
            self.checkBox_islocalport.hide()
            self.pushButton_listen.setEnabled(True)
        self.pushButton_send.setEnabled(False)
        if self.comboBox_net.currentIndex() == 1 or self.comboBox_net.currentIndex() == 3:
            self.widget_setting_client.show()
            self.checkBox_islocalport.show()
            self.pushButton_listen.setEnabled(False)
            self.pushButton_client.setEnabled(True)



    @QtCore.pyqtSlot()
    def testnet(self):
        self.tesRedis()
        self.testMysql()
        self.test_url()
        self.testUdp()


    def testUdp(self):

        msg = random.choice(self.HeartData)
        for udpconf in self.udpconf:
            ip = udpconf["ip"]
            port = udpconf["port"]
            self.netUDP = UDPServer_old.UDPServer_old()
            self.connect(self.netUDP, QtCore.SIGNAL("signal_write_msg"), self.show_revc_msg)
            self.connect(self.netUDP, QtCore.SIGNAL("signal_send_msg"), self.show_send_msg)
            self.netUDP.udp_client_test(ip, port, msg)
            # time.sleep(1)
            del self.netUDP


    def test_url(self):
        import testURL
        turl = testURL.testURL()
        self.connect(turl, QtCore.SIGNAL("signal_write_msg"), self.show_revc_msg)
        self.connect(turl, QtCore.SIGNAL("signal_send_msg"), self.show_send_msg)
        turl.testconnecturl(self.urllist)

    def testMysql(self):
        import mysql_test
        myconn = mysql_test.mysqlConn()
        self.connect(myconn, QtCore.SIGNAL("signal_write_msg"), self.show_revc_msg)
        self.connect(myconn, QtCore.SIGNAL("signal_send_msg"), self.show_send_msg)
        myconn.mysqlconn_test(self.mysqlconf)


    def tesRedis(self):
        import redisConnectManager
        rcm = redisConnectManager.RedisConnManger()
        self.connect(rcm, QtCore.SIGNAL("signal_write_msg"), self.show_revc_msg)
        self.connect(rcm, QtCore.SIGNAL("signal_send_msg"), self.show_send_msg)
        rcm.check_redis(self.redisconf)

    def open(self,obj):
        obj.open()
        pass
    @QtCore.pyqtSlot()
    def startorstop(self):
        if self.netSer == None :
            self.startServer()
            self.pushButton_send.setEnabled(True)
        else:
            self.stopServer()
            self.pushButton_listen.setText(u"启动")
            self.pushButton_send.setEnabled(False)

    @QtCore.pyqtSlot()
    def connordisconn(self):
        if self.netCli == None:
            self.startClient()
            self.pushButton_send.setEnabled(True)
        else:
            self.disconn()
            self.pushButton_client.setText(u"连接")
            self.pushButton_send.setEnabled(False)

    @QtCore.pyqtSlot()
    def sendmsg(self):
        try:
            # print self.textEdit_send.toPlainText()
            msg = str(self.textEdit_send.toPlainText())
        except:
            self.show_send_msg("error")
            return
        # msg = "a5a50001000001000000000000000000000000006600a3a3"
        # print msg
        # self.isHex = self.checkBox_ishex.isChecked()
        if self.checkBox_ishex_send.isChecked():
            msg = self.dataSwitch(msg)


        if self.netCli is not None:
            self.netCli.send(msg)

        if self.netSer is not None:
            self.netSer.send(msg,True)

    @QtCore.pyqtSlot()
    def clearrecv(self):
        self.textEdit_recv.clear()

    @QtCore.pyqtSlot()
    def clearsend(self):
        self.textEdit_send.clear()

    def startServer(self):
        # print "1111"
        # s = self.lineEdit_port.text()
        try:
            ip = str(self.lineEdit_ip.text())
            port = int(self.lineEdit_port.text())
        except:
            self.show_revc_msg(u"请输入正确的ip或端口号")
            return

        if self.comboBox_net.currentIndex() == 0:
            self.netSer = TCPServerOld.TcpServer_old()

        if self.comboBox_net.currentIndex() == 2:
            self.netSer = UDPServer_old.UDPServer_old()

        self.connect(self.netSer, QtCore.SIGNAL("signal_write_msg"), self.show_revc_msg)
        self.connect(self.netSer, QtCore.SIGNAL("signal_send_msg"), self.show_send_msg)
        # if self.checkBox_ishex.isChecked():
        #     self.netSer.setisHex(True)
        self.netSer.link = True
        self.isser = True
        # self.netSer.communication.open()

        self.netSer.server_start(port)
        self.pushButton_listen.setText(u"停止")

    def startClient(self):
        # print "1111"
        # s = self.lineEdit_port.text()
        try:
            ip = str(self.lineEdit_objip.text())
            port = int(self.lineEdit_objport.text())
        except:
            self.show_revc_msg(u"请输入正确的ip或端口号")
            return
        if self.comboBox_net.currentIndex() == 1:
            self.netCli = TCPServerOld.TcpServer_old()

        if self.comboBox_net.currentIndex() == 3:
            self.netCli = UDPServer_old.UDPServer_old()

        self.connect(self.netCli, QtCore.SIGNAL("signal_write_msg"), self.show_revc_msg)
        self.connect(self.netCli, QtCore.SIGNAL("signal_send_msg"), self.show_send_msg)
        # if self.checkBox_ishex.isChecked():
        #     self.netCli.setisHex(True)
        self.netCli.link = True
        self.isser = False
        self.netCli.client_start(ip,port)

        self.pushButton_client.setText(u"断开")

    def stopServer(self):
        self.netSer.ser_close(self.isser)
        self.netSer.link = False

        del self.netSer
        self.netSer = None


    def disconn(self):
        self.netCli.ser_close(self.isser)
        self.netCli.link = False
        self.netCli = None

    def show_revc_msg(self, msg):
        # print msg
        # if self.checkBox_ishex_recv.isChecked():
        #     msg_list = msg.split("|")
        #     msg = msg.encode('hex')
        # else:
        msg=msg.decode('utf-8')
        self.textEdit_recv.insertPlainText(msg)
        self.textEdit_recv.moveCursor(QtGui.QTextCursor.End)

    def show_send_msg(self, msg):
        # print msg
        msg=msg.decode('utf-8')
        self.textEdit_send.insertPlainText(msg)
        self.textEdit_send.moveCursor(QtGui.QTextCursor.End)

    def dataSwitch(self,data):
        str1 = ''
        str2 = ''
        while data:
            str1 = data[0:2]
            s = int(str1, 16)
            str2 += struct.pack('B', s)
            data = data[2:]
        return str2

    def getconf(self):
        import jsonParserOper
        jpo = jsonParserOper.jsonOper()
        confdict = jpo.getjsondict("address.json")
        self.mysqlconf = confdict["mysql"]
        self.redisconf = confdict["redis"]
        self.urllist = confdict["url"]
        self.udpconf = confdict["udp"]
        self.HeartData = confdict["HeartData"]
        # print confdict


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())