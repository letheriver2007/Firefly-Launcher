import os
import json
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, InfoBar, InfoBarPosition
from app.model.style_sheet import StyleSheet
from app.model.setting_group import SettingCardGroup
from app.model.toolkit_message import MessageFiddler, PrimaryPushSettingCard_Fiddler
from app.model.download_message import HyperlinkCard_Tool, download_check


class Proxy(ScrollArea):
    Nav = Pivot
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setObjectName(text)
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        # 栏定义
        self.pivot = self.Nav(self)
        self.stackedWidget = QStackedWidget(self)

        # 添加项
        self.ProxyDownloadInterface = SettingCardGroup(self.scrollWidget)
        self.ProxyRepoCard = HyperlinkCard_Tool(
            'https://www.telerik.com/fiddler#fiddler-classic',
            'Fiddler',
            'https://mitmproxy.org/',
            'Mitmdump',
            FIF.LINK,
            '项目仓库',
            '打开代理工具仓库'
        )
        self.DownloadFiddlerCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            'Fiddler',
            '下载代理工具Fiddler'
        )
        self.DownloadMitmdumpCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            'Mitmdump',
            '下载代理工具Mitmdump'
        )
        self.ProxyToolInterface = SettingCardGroup(self.scrollWidget)
        self.FiddlerCard = PrimaryPushSettingCard_Fiddler(
            '脚本打开',
            '原版打开',
            FIF.VPN,
            'Fiddler(外部)',
            '使用Fiddler Scripts代理'
        )
        self.mitmdumpCard = PrimaryPushSettingCard( 
            '打开',
            FIF.VPN,
            'Mitmdump(外部)',
            '使用Mitmdump代理'
        )

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)     # 水平滚动条关闭
        self.setViewportMargins(20, 0, 20, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)    # 必须设置！！！
        
        # 使用qss设置样式
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # 项绑定到栏目
        self.ProxyDownloadInterface.addSettingCard(self.ProxyRepoCard)
        self.ProxyDownloadInterface.addSettingCard(self.DownloadFiddlerCard)
        self.ProxyDownloadInterface.addSettingCard(self.DownloadMitmdumpCard)
        self.ProxyToolInterface.addSettingCard(self.FiddlerCard)
        self.ProxyToolInterface.addSettingCard(self.mitmdumpCard)

        # 栏绑定界面
        self.addSubInterface(self.ProxyDownloadInterface, 'ToolkitDownloadInterface','下载', icon=FIF.DOWNLOAD)
        self.addSubInterface(self.ProxyToolInterface, 'ProxyToolInterface','代理', icon=FIF.CERTIFICATE)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.ProxyDownloadInterface)
        self.pivot.setCurrentItem(self.ProxyDownloadInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.ProxyDownloadInterface.objectName())

    def __connectSignalToSlot(self):
        self.DownloadFiddlerCard.clicked.connect(lambda: download_check(self, 'fiddler'))
        self.DownloadMitmdumpCard.clicked.connect(lambda: download_check(self, 'mitmdump'))
        self.FiddlerCard.clicked_script.connect(lambda: self.proxy_fiddler('script'))
        self.FiddlerCard.clicked_old.connect(lambda: self.proxy_fiddler('old'))
        self.mitmdumpCard.clicked.connect(self.proxy_mitmdump)

    def addSubInterface(self, widget: QLabel, objectName, text, icon=None):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            icon=icon,
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())

    def open_file(self, file_path):
        if os.path.exists(file_path):
            subprocess.run(['start', file_path], shell=True)
        else:
            InfoBar.error(
                title="找不到文件，请重新下载！",
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
    
    def proxy_fiddler(self, mode):
        if mode =='script':
            w = MessageFiddler(self)
            if w.exec():
                self.open_file('src/patch/yuanshen/update.exe')
                self.open_file('tool/Fiddler/Fiddler.exe')
            else:
                self.open_file('src/patch/starrail/update.exe')
                self.open_file('tool/Fiddler/Fiddler.exe')
        elif mode == 'old':
            self.open_file('tool/Fiddler/Fiddler.exe')

    def proxy_mitmdump(self):
        if os.path.exists('tool/Mitmdump'):
            subprocess.run('cd ./tool/Mitmdump && start /b Proxy.exe', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            InfoBar.error(
                title="找不到文件，请重新下载！",
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )