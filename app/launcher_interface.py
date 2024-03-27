import os
import subprocess
from PySide6.QtWidgets import QWidget, QLabel, QStackedWidget, QVBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, InfoBar, InfoBarPosition
from app.model.style_sheet import StyleSheet
from app.model.setting_group import SettingCardGroup
from app.model.download_message import HyperlinkCard_Launcher, download_check


class Launcher(ScrollArea):
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
        self.LauncherDownloadInterface = SettingCardGroup(self.scrollWidget)
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
        self.ConfigInterface = SettingCardGroup(self.scrollWidget)
        self.settingConfigCard = PrimaryPushSettingCard(
            '打开文件',
            FIF.LABEL,
            '启动器设置',
            '自定义启动器配置'
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
        self.LauncherDownloadInterface.addSettingCard(self.LauncherRepoCard)
        self.LauncherDownloadInterface.addSettingCard(self.AudioDownloadCard)
        self.ConfigInterface.addSettingCard(self.settingConfigCard)

        # 栏绑定界面
        self.addSubInterface(self.LauncherDownloadInterface, 'LauncherDownloadInterface','下载', icon=FIF.DOWNLOAD)
        self.addSubInterface(self.ConfigInterface,'configInterface','配置', icon=FIF.EDIT)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.LauncherDownloadInterface)
        self.pivot.setCurrentItem(self.LauncherDownloadInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.LauncherDownloadInterface.objectName())

    def __connectSignalToSlot(self):
        self.AudioDownloadCard.clicked.connect(lambda: download_check(self, 'audio'))
        self.settingConfigCard.clicked.connect(lambda: self.open_file('config/config.json'))

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