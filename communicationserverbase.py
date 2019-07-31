#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/6/19 9:42
# @Author  : linjinting
# @Site    :
# @Software: CommunicationTool
# @File    : communicationserverbase.py
# @Function:

import threading
from communicationbase import CommunicationBase


class CommunicationServerBase(CommunicationBase):
    def __init__(self):
        super(CommunicationServerBase, self).__init__()

        self.client_conns = dict()
        self.lock = threading.Lock()

    def setCookie(self, key, value):

        _conn = self.client_conns.get(key)
        if _conn:
            return -1

        with self.lock:
            self.client_conns[key] = value

        self.channel_change("client")
        return 0

    def unsetCookie(self, key):

        with self.lock:
            _conns = self.client_conns.pop(key)
        self.channel_change("client")
        return 0

    def getCookie(self, key):
        return self.client_conns.get(key)


if __name__ == '__main__':
    CSB = CommunicationServerBase()
    CSB.setCookie("ddd", "123123123123123")
    print CSB.getCookie("ddd")
