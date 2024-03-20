import os
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, HyperlinkCard, InfoBar, InfoBarPosition
from app.model.config import cfg
from app.model.style_sheet import StyleSheet
from app.model.setting_group import SettingCardGroup
from app.model.download_message import (MessageDownload, HyperlinkCard_Tool, download_check,
                                       HyperlinkCard_Environment, MessageLauncher, MessageGit, MessageJava, MessageMongoDB, MessageFiddler,
                                       MessageMitmdump, HyperlinkCard_Launcher, MessageAudio)


class ToolkitDownload(ScrollArea):
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
        self.LauncherInterface = SettingCardGroup(self.scrollWidget)
        self.LauncherRepoCard = HyperlinkCard_Launcher(
            'https://github.com/letheriver2007/Firefly-Launcher',
            'Firefly-Launcher',
            'https://github.com/letheriver2007/Firefly-Launcher-Res',
            'Firefly-Launcher-Res',
            FIF.LINK,
            '项目仓库',
            '打开Firefly-Launcher相关项目仓库'
        )
        self.AudioDownloadCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            'Firefly-Launcher-Audio',
            '下载流萤音频文件'
        )
        self.EnvironmentInterface = SettingCardGroup(self.scrollWidget)
        self.EnvironmentRepoCard = HyperlinkCard_Environment(
            'https://git-scm.com/download/win',
            'Git',
            'https://www.oracle.com/java/technologies/javase-downloads.html',
            'Java',
            'https://www.mongodb.com/try/download/community',
            'MongoDB',
            FIF.LINK,
            '项目仓库',
            '打开各环境仓库'
        )
        self.GitDownloadCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            'Git',
            '下载Git安装包'
        )
        self.JavaDownloadCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            'Java',
            '下载Java安装包'
        )
        self.MongoDBDownloadCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            'MongoDB',
            '下载MongoDB安装包'
        )
        self.ToolInterface = SettingCardGroup(self.scrollWidget)
        self.ToolRepoCard = HyperlinkCard_Tool(
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

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)     # 水平滚动条关闭
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)    # 必须设置！！！
        
        # 使用qss设置样式
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # 项绑定到栏目
        self.LauncherInterface.addSettingCard(self.LauncherRepoCard)
        self.LauncherInterface.addSettingCard(self.AudioDownloadCard)
        self.EnvironmentInterface.addSettingCard(self.EnvironmentRepoCard)
        self.EnvironmentInterface.addSettingCard(self.GitDownloadCard)
        self.EnvironmentInterface.addSettingCard(self.JavaDownloadCard)
        self.EnvironmentInterface.addSettingCard(self.MongoDBDownloadCard)
        self.ToolInterface.addSettingCard(self.ToolRepoCard)
        self.ToolInterface.addSettingCard(self.DownloadFiddlerCard)
        self.ToolInterface.addSettingCard(self.DownloadMitmdumpCard)

        # 栏绑定界面
        self.addSubInterface(self.LauncherInterface, 'LauncherInterface','启动器', icon=FIF.TAG)
        self.addSubInterface(self.EnvironmentInterface, 'EnvironmentInterface','环境', icon=FIF.TAG)
        self.addSubInterface(self.ToolInterface, 'ToolInterface','代理', icon=FIF.TAG)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.addSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.LauncherInterface)
        self.pivot.setCurrentItem(self.LauncherInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.LauncherInterface.objectName())
        
    def __connectSignalToSlot(self):
        self.AudioDownloadCard.clicked.connect(lambda: download_check(self, 'audio'))
        self.GitDownloadCard.clicked.connect(lambda: download_check(self, 'git'))
        self.JavaDownloadCard.clicked.connect(lambda: download_check(self, 'java'))
        self.MongoDBDownloadCard.clicked.connect(lambda: download_check(self, 'mongodb'))
        self.DownloadFiddlerCard.clicked.connect(lambda: download_check(self, 'fiddler'))
        self.DownloadMitmdumpCard.clicked.connect(lambda: download_check(self, 'mitmdump'))

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
