#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/7 22:38
# @Author  : Aries
# @Site    : 
# @File    : checkconn_pwfw.py
# @Software: PyCharm

import UDPClient,UDPClientBase

class CheckConnPWFW(object):
    def __init__(self):
        pass

    def check_psm70server(self):
        # msg = random.choice(self.HeartData)
        for udpconf in self.udpconf:
            ip = udpconf["ip"]
            port = udpconf["port"]
            udp_conn = UDPClientBase.UDPClientBase()
            udp_conn.setopAddress(ip,port)
            udp_conn.setHexSend(True)
            udp_conn.setHexDisplay(True)
            udp_conn.setTimeOut(3)
            for i in range(3):
                print(i)
                udp_conn.open()
                udp_conn.send(self.HeartData[0])
                istimeout = udp_conn.check_recv()
                if istimeout:
                    print("timeout")
                else:
                    break
            udp_conn.close()


    def getconf(self):
        import jsonParserOper
        jpo = jsonParserOper.jsonOper()
        confdict = jpo.getjsondict("address.json")
        if confdict:
            self.mysqlconf = confdict["mysql"]
            self.redisconf = confdict["redis"]
            self.urllist = confdict["url"]
            self.udpconf = confdict["udp"]
            self.HeartData = confdict["HeartData"]
        else:
            import  defaultconfcheck
            confdict = defaultconfcheck.conf
            self.mysqlconf = confdict["mysql"]
            self.redisconf = confdict["redis"]
            self.urllist = confdict["url"]
            self.udpconf = confdict["udp"]
            self.HeartData = confdict["HeartData"]

if __name__ == '__main__':
    cc = CheckConnPWFW()
    cc.getconf()
    cc.check_psm70server()

    # print(cc.HeartData)
