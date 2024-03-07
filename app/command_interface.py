import os
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QApplication
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (Pivot, qrouter, ScrollArea, LineEdit, PrimaryPushButton,
                            PrimaryPushSettingCard, InfoBar, InfoBarPosition)
from app.component.style_sheet import StyleSheet
from app.component.common import PrimaryPushSettingCard_Giveall
from app.component.setting_group import SettingCardGroup


class Command(ScrollArea):
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

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)     # 水平滚动条关闭
        self.setViewportMargins(20, 0, 20, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)    # 必须设置！！！

        self.updateText = LineEdit()
        self.updateText.setFixedSize(950, 35)
        self.clearButton = PrimaryPushButton('清空')
        self.copyButton = PrimaryPushButton('复制')
        self.clearButton.setFixedSize(80, 35)
        self.copyButton.setFixedSize(80, 35)
        self.updateContainer = QWidget()
        
        # 使用qss设置样式
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # 栏绑定界面
        self.LunarCoreInterface = LunarCore('About Interface', self)
        self.addSubInterface(self.LunarCoreInterface, 'LunarCoreInterface','LunarCore', icon=FIF.COMMAND_PROMPT)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.LunarCoreInterface)
        self.pivot.setCurrentItem(self.LunarCoreInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.LunarCoreInterface.objectName())

        self.updateLayout = QHBoxLayout(self.updateContainer)
        self.updateLayout.addWidget(self.updateText, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(15)
        self.updateLayout.addWidget(self.clearButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(5)
        self.updateLayout.addWidget(self.copyButton, alignment=Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.updateContainer)

    def __connectSignalToSlot(self):
        self.LunarCoreInterface.giveallClicked.connect(self.handleGiveallClick)
        self.clearButton.clicked.connect(lambda: self.updateText.clear())
        self.copyButton.clicked.connect(self.copyToClipboard)

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
    
    def handleGiveallClick(self, text):
        self.updateText.clear()
        self.updateText.setText(text)
    
    def copyToClipboard(self):
        text = self.updateText.text()
        app = QApplication.instance()
        try:
            if text != '':
                clipboard = app.clipboard()
                clipboard.setText(text)
                InfoBar.success(
                    title='复制成功！',
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
            else:
                InfoBar.error(
                    title='复制失败！',
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
        except:
            InfoBar.error(
                title='复制失败！',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )


class LunarCore(ScrollArea):
    Nav = Pivot
    giveallClicked = Signal(str)
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
        self.CustomInterface = SettingCardGroup('代理', self.scrollWidget)
        self.giveallCard = PrimaryPushSettingCard_Giveall(
            '物品',
            '角色',
            FIF.TAG,
            '给予全部',
            '/giveall {materials | avatars}'
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
        self.CustomInterface.addSettingCard(self.giveallCard)

        # 栏绑定界面
        self.addSubInterface(self.CustomInterface, 'CustomInterface','自定义', icon=FIF.TAG)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.CustomInterface)
        self.pivot.setCurrentItem(self.CustomInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.CustomInterface.objectName())
        
    def __connectSignalToSlot(self):
        self.giveallCard.give_materials.connect(lambda: self.giveallClicked.emit('/giveall materials'))
        self.giveallCard.give_avatars.connect(lambda: self.giveallClicked.emit('/giveall avatars'))

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