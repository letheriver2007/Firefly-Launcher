import os
import subprocess
from PySide6.QtWidgets import QWidget, QLabel, QStackedWidget, QVBoxLayout
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, InfoBar, FluentIcon,
                            HyperlinkButton, InfoBarPosition, PrimaryPushButton, InfoBarIcon)
from app.model.style_sheet import StyleSheet
from app.model.setting_card import SettingCard, SettingCardGroup
from app.model.download_process import SubDownloadCMD
from app.setting_interface import Setting
from app.model.config import Info


class HyperlinkCard_Environment(SettingCard):
    def __init__(self, title, content=None, icon=FluentIcon.LINK):
        super().__init__(icon, title, content)
        self.linkButton_git = HyperlinkButton('https://git-scm.com/download/win', 'Git', self)
        self.linkButton_jar = HyperlinkButton('https://www.oracle.com/java/technologies/javase-downloads.html', 'Java',
                                              self)
        self.linkButton_mongodb = HyperlinkButton('https://www.mongodb.com/try/download/community', 'MongoDB', self)
        self.hBoxLayout.addWidget(self.linkButton_git, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_jar, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_mongodb, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


class PrimaryPushSettingCard_MongoDB(SettingCard):
    mongodb_installer = Signal()
    mongodb_portable = Signal()

    def __init__(self, title, content, icon=FluentIcon.DOWNLOAD):
        super().__init__(icon, title, content)
        self.button_installer = PrimaryPushButton(self.tr('安装包'), self)
        self.button_portable = PrimaryPushButton(self.tr('便携版'), self)
        self.hBoxLayout.addWidget(self.button_installer, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_portable, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_installer.clicked.connect(self.mongodb_installer)
        self.button_portable.clicked.connect(self.mongodb_portable)


class Environment(ScrollArea):
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
        self.EnvironmentInterface = SettingCardGroup(self.scrollWidget)
        self.MongoDBCard = PrimaryPushSettingCard(
            self.tr('打开'),
            FluentIcon.FIT_PAGE,
            'MongoDB',
            self.tr('打开便携版MongoDB数据库')
        )
        self.EnvironmentDownloadInterface = SettingCardGroup(self.scrollWidget)
        self.EnvironmentRepoCard = HyperlinkCard_Environment(
            self.tr('项目仓库'),
            self.tr('打开各环境仓库')
        )
        self.GitDownloadCard = PrimaryPushSettingCard(
            self.tr('下载'),
            FluentIcon.DOWNLOAD,
            'Git',
            self.tr('下载Git安装包')
        )
        self.JavaDownloadCard = PrimaryPushSettingCard(
            self.tr('下载'),
            FluentIcon.DOWNLOAD,
            'Java',
            self.tr('下载Java安装包')
        )
        self.MongoDBDownloadCard = PrimaryPushSettingCard_MongoDB(
            'MongoDB',
            self.tr('下载MongoDB数据库')
        )

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 水平滚动条关闭
        self.setViewportMargins(20, 0, 20, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)  # 必须设置！！！

        # 使用qss设置样式
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # 项绑定到栏目
        self.EnvironmentInterface.addSettingCard(self.MongoDBCard)
        self.EnvironmentDownloadInterface.addSettingCard(self.EnvironmentRepoCard)
        self.EnvironmentDownloadInterface.addSettingCard(self.GitDownloadCard)
        self.EnvironmentDownloadInterface.addSettingCard(self.JavaDownloadCard)
        self.EnvironmentDownloadInterface.addSettingCard(self.MongoDBDownloadCard)

        # 栏绑定界面
        self.addSubInterface(self.EnvironmentInterface, 'EnvironmentInterface', self.tr('环境'), icon=FluentIcon.PLAY)
        self.addSubInterface(self.EnvironmentDownloadInterface, 'EnvironmentDownloadInterface', self.tr('下载'),
                             icon=FluentIcon.DOWNLOAD)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.EnvironmentInterface)
        self.pivot.setCurrentItem(self.EnvironmentInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.EnvironmentInterface.objectName())

    def __connectSignalToSlot(self):
        self.MongoDBCard.clicked.connect(self.handleMongoDBOpen)
        SubDownloadCMDSelf = SubDownloadCMD(self)
        self.GitDownloadCard.clicked.connect(self.handleRestartInfo)
        self.GitDownloadCard.clicked.connect(lambda: SubDownloadCMDSelf.handleDownloadStarted('git'))
        self.JavaDownloadCard.clicked.connect(lambda: SubDownloadCMDSelf.handleDownloadStarted('java'))
        self.MongoDBDownloadCard.mongodb_installer.connect(lambda: SubDownloadCMDSelf.handleDownloadStarted('mongodb_installer'))
        self.MongoDBDownloadCard.mongodb_portable.connect(lambda: SubDownloadCMDSelf.handleDownloadStarted('mongodb_portable'))

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

    def handleMongoDBOpen(self):
        if os.path.exists('tool/mongodb/mongod.exe'):
            subprocess.run('start cmd /c "cd tool/mongodb && mongod --dbpath data --port 27017"', shell=True)
            Info(self, "S", 1000, self.tr("数据库已开始运行!"))
        else:
            file_error = InfoBar(
                icon=InfoBarIcon.ERROR,
                title=self.tr('找不到数据库!'),
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            file_error_button = PrimaryPushButton(self.tr('前往下载'))
            file_error_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
            file_error.addWidget(file_error_button)
            file_error.show()
    
    def handleRestartInfo(self):
        restart_info = InfoBar(
            icon=InfoBarIcon.WARNING,
            title=self.tr('重启应用以使用Git命令!'),
            content='',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=-1,
            parent=self
        )
        restart_button = PrimaryPushButton(self.tr('重启'))
        restart_button.clicked.connect(Setting.restart_application)
        restart_info.addWidget(restart_button)
        restart_info.show()
