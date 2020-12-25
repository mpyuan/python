# -*- coding: utf-8 -*-
# @Author: mapyuan
# @Date  :  2020/12/23

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

class MyWebView(QWebEngineView):
    def createWindow(self, QWebEnginePage_WebWindowType):
        print(QWebEnginePage_WebWindowType)
        if QWebEnginePage_WebWindowType == QWebEnginePage.WebBrowserTab:
            self.newWeb = MyWebView(self)
            # self.newWeb = MyWebView()  # 不认self为父，就会在新窗口显示，认self作父就能在当前窗口显示
            self.newWeb.setAttribute(Qt.WA_DeleteOnClose, True)  # 加上这个属性能防止Qt Qtwebengineprocess进程关不掉导致崩溃
            self.newWeb.setGeometry(QRect(0, 0, 300, 150))
            self.newWeb.show()
            return self.newWeb
        return super(MyWebView, self).createWindow(QWebEnginePage_WebWindowType)

def on_url_changed(url):
    print(url)
    view.setUrl(url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MyWebView()
    url = 'http://192.168.1.102:8099/backend/site/login'
    view.setUrl(QUrl(url))
    view.show()
    sys.exit(app.exec_())
    # window = MainWindow()
    # window.show()
    view = QWebEngineView()
    profile = QWebEngineProfile('name',view)
    profile.setHttpUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36')
    page = QWebEnginePage(profile)

    useragent = 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat'
    page.profile().setHttpUserAgent(useragent)
    print(profile.httpUserAgent())
    print(page.profile().httpUserAgent())
    print(page.url())
    view.urlChanged.connect(on_url_changed)


    # view.resize(800, 800)
    view.setPage(page)
    url = 'http://192.168.1.102:8099/backend/site/login'
    view.setUrl(QUrl(url))
    view.show()
    sys.exit(app.exec_())
