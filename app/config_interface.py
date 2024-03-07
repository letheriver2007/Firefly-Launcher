import os
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (Pivot, qrouter, ScrollArea, SettingCardGroup,
                            PrimaryPushSettingCard, InfoBar, InfoBarPosition)
from src.component.style_sheet import StyleSheet


class Config(ScrollArea):
    Nav = Pivot
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setObjectName(text.replace(' ', '-'))
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        # 栏定义
        self.pivot = self.Nav(self)
        self.stackedWidget = QStackedWidget(self)

        # 添加项 , 名字会隐藏
        self.LauncherInterface = SettingCardGroup('配置', self.scrollWidget)
        self.settingConfigCard = PrimaryPushSettingCard(
            '打开文件',
            FIF.LABEL,
            '启动器设置',
            '自定义启动器配置'
        )
        self.personalConfigCard = PrimaryPushSettingCard(
            '打开文件',
            FIF.LABEL,
            '个性化',
            '自定义个性化配置'
        )
        self.LunarCoreInterface = SettingCardGroup('LunarCore', self.scrollWidget)
        self.bannersConfigCard = PrimaryPushSettingCard(
            '打开文件',
            FIF.LABEL,
            'Banners',
            'LunarCore的跃迁配置'
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
        self.LauncherInterface.addSettingCard(self.settingConfigCard)
        self.LauncherInterface.addSettingCard(self.personalConfigCard)
        self.LunarCoreInterface.addSettingCard(self.bannersConfigCard)

        # 目前无法做到导航栏各个页面独立分组 , 故隐藏组标题
        self.LauncherInterface.titleLabel.setHidden(True)
        self.LunarCoreInterface.titleLabel.setHidden(True)

        # 栏绑定界面
        self.addSubInterface(self.LauncherInterface, 'LauncherInterface','启动器', icon=FIF.PLAY)
        self.addSubInterface(self.LunarCoreInterface, 'LunarCoreInterface','LunarCore', icon=FIF.TAG)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(28)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.LauncherInterface)
        self.pivot.setCurrentItem(self.LauncherInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.LauncherInterface.objectName())
        
    def __connectSignalToSlot(self):
        self.settingConfigCard.clicked.connect(lambda: self.open_file('config/config.json'))
        self.personalConfigCard.clicked.connect(lambda: self.open_file('config/auto.json'))
        self.bannersConfigCard.clicked.connect(lambda: self.open_file('server/lunarcore/data/banners.json'))

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