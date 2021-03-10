# -*- coding: utf-8 -*-
# @Author: mapyuan
# @Date  :  2020/12/23

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MyQWebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self,info):

        print(info.firstPartyUrl())
        print(info.requestMethod())

        pass


# 创建主窗口
class MainWindow(QMainWindow):
    def closeEvent(self, *args, **kwargs):
        print(self)
        print(*args)
        print(**kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置窗口标题
        self.setWindowTitle('简易浏览器')
        # 设置窗口大小900*600
        self.resize(1300, 700)
        self.show()

        # 创建tabwidget（多标签页面）
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_Tab)

        self.setCentralWidget(self.tabWidget)

        # 第一个tab页面
        self.webview = WebEngineView(self)  # self必须要有，是将主窗口作为参数，传给浏览器

        self.webview.load(QUrl("https://www.baidu.com/"))
        # self.webview.load(QUrl("http://192.168.1.102:8099/backend/site/login"))
        # self.webview.load(QUrl("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx636a8419238f974e&redirect_uri=https%3A%2F%2Fgzl.yitong111.com%2Ffrontend%2Fsite%2Fadd-user&response_type=code&scope=snsapi_userinfo&state=769ed0a09a33c9cb306b58b589ff6750&uin=MTU5NzA1MjcwNQ%3D%3D&key=abfa9467dbd5851e5c89936aeb3907bdb04d2567a190547c482ecae09dd6534f710de62282cdd3958c73474c20b567d72210515ba9803eff6de664727e95b722e493ba4e462f8defbf85c862d07651e212dac4a82982b9c2b264456996a67065c0f622388f24187f051b6c244f2b90a9a67dc8617b1cbbceedba9f0c502c056a&version=63010043&pass_ticket=IjzkjgFeyizqCAm3Nt9dlI2pF1kW6IaVwVGGY2cCCfS2LSZ7t3MGVOVt2%2FedOu3y"))

        self.create_tab(self.webview)

        # 使用QToolBar创建导航栏，并使用QAction创建按钮
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(16, 16))
        # 添加导航栏到窗口中
        self.addToolBar(navigation_bar)

        # QAction类提供了抽象的用户界面action，这些action可以被放置在窗口部件中
        # 添加前进、后退、停止加载和刷新的按钮
        back_button = QAction(QIcon('icons/houtui.png'), 'Back', self)
        next_button = QAction(QIcon('icons/qianjin.png'), 'Forward', self)
        stop_button = QAction(QIcon('icons/close.png'), 'stop', self)
        reload_button = QAction(QIcon('icons/shuaxin.png'), 'reload', self)

        # 绑定事件
        back_button.triggered.connect(self.webview.back)
        next_button.triggered.connect(self.webview.forward)
        stop_button.triggered.connect(self.webview.stop)
        reload_button.triggered.connect(self.webview.reload)

        # 将按钮添加到导航栏上
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)

        # 添加URL地址栏
        self.urlbar = QLineEdit()
        # 让地址栏能响应回车按键信号
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

        # 让浏览器相应url地址的变化
        self.webview.urlChanged.connect(self.renew_urlbar)

    # 显示地址
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.webview.setUrl(q)

    # 响应输入的地址
    def renew_urlbar(self, q):
        # 将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    # 创建tab页面
    def create_tab(self, webview):
        self.tab = QWidget()
        self.tabWidget.addTab(self.tab, "新建页面")
        self.tabWidget.setCurrentWidget(self.tab)

        # 渲染到页面
        self.Layout = QHBoxLayout(self.tab)
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.Layout.addWidget(webview)

    # 关闭tab页面
    def close_Tab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)
        else:
            self.close()  # 当只有1个tab时，关闭主窗口


# 创建浏览器，重写重写createwindow方法实现页面连接的点击跳转
class WebEngineView(QWebEngineView):

    def __init__(self, mainwindow, parent=None):
        #useragent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat'
        useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        #useragent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI micromessenger/7.0.5 WindowsWechat'
        #useragent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1316.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat'
        super(WebEngineView, self).__init__(parent)
        self.mainwindow = mainwindow
        self.page().profile().setHttpUserAgent(useragent)
        # self.page().profile().setHttpAcceptLanguage('zh-CN,zh')
        self.page().profile().setHttpAcceptLanguage('zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4')
        interceptor = MyQWebEngineUrlRequestInterceptor(self.mainwindow)
        self.page().profile().setUrlRequestInterceptor(interceptor)
        self.page().profile().setRequestInterceptor(interceptor)
        # self.page().profile().settings().setDefaultTextEncoding('utf-8')
        # print('httpAcceptLanguage',self.page().profile().httpAcceptLanguage())

        # 网页加载完后输出网页源代码
        self.page().loadFinished.connect(self.getHtmlText)

    def getHtmlText(self):
        # pass
        # self.page().toHtml(lambda text: print(text))
        # self.page().runJavaScript('''function getname(){
        #     alert(window.navigator.webdriver);
        #     for(var i in window){
        #         document.write(i,':',window[i],'<br />')
        #     }
        # };
        # getname();
        # ''')
        # print(self.page().profile().httpAcceptLanguage())
        print(self.page().profile().storageName())
        print(self.page().profile().persistentStoragePath())
        print(self.page().profile().settings().defaultTextEncoding())
        # print(self.page().profile().settings().fontFamily())
        # print(self.page().profile().settings().fontSize())
        print(self.page().profile().settings().defaultTextEncoding())

        pass

    # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView(self.mainwindow)
        self.mainwindow.create_tab(new_webview)
        return new_webview


# 程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 创建主窗口
    browser = MainWindow()
    browser.show()
    # 运行应用，并监听事件
    sys.exit(app.exec_())