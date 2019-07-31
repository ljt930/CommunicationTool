#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/6/21 9:06
# @Author  : linjinting
# @Site    :
# @Software: CommunicationTool
# @File    : main.py
# @Function:
from PyQt4 import QtGui
import sys
import Communication_test_tool


def main():
    app = QtGui.QApplication(sys.argv)
    window = Communication_test_tool.Communication_test_tool()
    window.show()

    sys.exit(app.exec_())


main()
