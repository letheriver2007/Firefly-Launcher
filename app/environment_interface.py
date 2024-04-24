from PySide6.QtWidgets import QWidget, QLabel, QStackedWidget, QVBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import (Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, InfoBar, FluentIcon,
                            HyperlinkButton, InfoBarPosition, PrimaryPushButton, InfoBarIcon)
from app.model.style_sheet import StyleSheet
from app.model.setting_card import SettingCard, SettingCardGroup
from app.model.download_process import SubDownloadCMD
from app.setting_interface import Setting


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
        self.MongoDBDownloadCard = PrimaryPushSettingCard(
            self.tr('下载'),
            FluentIcon.DOWNLOAD,
            'MongoDB',
            self.tr('下载MongoDB安装包')
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
        self.EnvironmentDownloadInterface.addSettingCard(self.EnvironmentRepoCard)
        self.EnvironmentDownloadInterface.addSettingCard(self.GitDownloadCard)
        self.EnvironmentDownloadInterface.addSettingCard(self.JavaDownloadCard)
        self.EnvironmentDownloadInterface.addSettingCard(self.MongoDBDownloadCard)

        # 栏绑定界面
        self.addSubInterface(self.EnvironmentDownloadInterface, 'EnvironmentDownloadInterface', self.tr('下载'),
                             icon=FluentIcon.DOWNLOAD)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.EnvironmentDownloadInterface)
        self.pivot.setCurrentItem(self.EnvironmentDownloadInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.EnvironmentDownloadInterface.objectName())

    def __connectSignalToSlot(self):
        SubDownloadCMDSelf = SubDownloadCMD(self)
        self.GitDownloadCard.clicked.connect(self.handleRestartInfo)
        self.GitDownloadCard.clicked.connect(lambda: SubDownloadCMDSelf.handleDownloadStarted('git'))
        self.JavaDownloadCard.clicked.connect(lambda: SubDownloadCMDSelf.handleDownloadStarted('java'))
        self.MongoDBDownloadCard.clicked.connect(lambda: SubDownloadCMDSelf.handleDownloadStarted('mongodb'))

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
