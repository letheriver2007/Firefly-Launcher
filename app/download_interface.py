import os
import sys
import shutil
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QTextEdit, QMainWindow, QPlainTextEdit
from PySide6.QtGui import QPixmap, Qt, QPainter, QPainterPath, QDesktopServices, QFont
from PySide6.QtCore import Qt, QUrl, QSize, QProcess, QThread, Signal
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (Pivot, qrouter, ScrollArea, SettingCardGroup,
                            CustomColorSettingCard, PushButton, setThemeColor, PrimaryPushSettingCard, HyperlinkCard,
                            Theme, setTheme, TitleLabel, SubtitleLabel, BodyLabel,IndeterminateProgressBar,
                            SwitchSettingCard, InfoBar, InfoBarPosition, MessageBoxBase, PlainTextEdit)
from src.common.config import cfg
from src.common.style_sheet import StyleSheet
from src.common.custom_message import MessageTool, MessageDownload, MessageLunarCore, MessageLunarCoreRes


class Download(ScrollArea):
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

        # 添加项 , 名字会隐藏(1)
        self.ToolInterface = SettingCardGroup('额外', self.scrollWidget)
        self.DownloadToolCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.ADD_TO,
            '代理工具',
            '本项目包含的额外工具(Fiddler、Mitmdump)'
        )
        self.LunarCoreInterface = SettingCardGroup('LunarCore', self.scrollWidget)
        self.LunarCoreRepoCard = HyperlinkCard(
            'https://github.com/Melledy/LunarCore',
            '打开',
            FIF.LINK,
            '项目仓库',
            '打开LunarCore本体的Github仓库'
        )
        self.LunarCoreDownloadCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            '项目下载',
            '下载LunarCore本体并编译'
        )
        self.LunarCoreResDownloadCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            '资源下载',
            '下载LunarCore资源文件'
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
        # 项绑定到栏目(2)
        self.ToolInterface.addSettingCard(self.DownloadToolCard)
        self.LunarCoreInterface.addSettingCard(self.LunarCoreRepoCard)
        self.LunarCoreInterface.addSettingCard(self.LunarCoreDownloadCard)
        self.LunarCoreInterface.addSettingCard(self.LunarCoreResDownloadCard)

        # 目前无法做到导航栏各个页面独立分组 , 故隐藏组标题(3)
        self.ToolInterface.titleLabel.setHidden(True)
        self.LunarCoreInterface.titleLabel.setHidden(True)

        # 栏绑定界面(4)
        self.addSubInterface(self.ToolInterface, 'ToolInterface','附加', icon=FIF.ADD_TO)
        self.addSubInterface(self.LunarCoreInterface, 'LunarCoreInterface','LunarCore', icon=FIF.ADD_TO)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(28)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.ToolInterface)
        self.pivot.setCurrentItem(self.ToolInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.ToolInterface.objectName())
        
    def __connectSignalToSlot(self):
        self.DownloadToolCard.clicked.connect(lambda: self.download_check('tool'))
        self.LunarCoreDownloadCard.clicked.connect(lambda: self.download_check('lunarcore'))
        self.LunarCoreResDownloadCard.clicked.connect(lambda: self.download_check('lunarcore_res'))

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

    def generate_download_url(self, extra):
        if cfg.chinaStatus.value:
            git_url = 'gitee.com'
            git_proxy = 'git clone --progress '
        elif cfg.proxyStatus.value:
            git_url = 'github.com'
            git_proxy = 'git -c http.proxy=http://127.0.0.1:7890 -c https.proxy=http://127.0.0.1:7890 clone --progress '
        else:
            git_url = 'github.com'
            git_proxy = 'git clone --progress '
        return f'{git_proxy}{extra}https://{git_url}/'

    def download_check(self, name, jar=False):
        if name == 'tool':
            w = MessageTool(self)
            check = './tool'
            command = self.generate_download_url('--branch tool ') + cfg.DOWNLOAD_COMMANDS_TOOL
        elif name == 'lunarcore':
            w = MessageLunarCore(self)
            check = './server/LunarCore'
            command = cfg.DOWNLOAD_COMMANDS_LUNARCORE
            jar = True
        elif name == 'lunarcore_res':
            w = MessageLunarCoreRes(self)
            check = './server/LunarCore/resources'
            command = cfg.DOWNLOAD_COMMANDS_LUNARCORE_RES

        if w.exec():
            if not os.path.exists(check):
                x = MessageDownload(self)
                x.show()
                x.start_download(command, jar)
                if x.exec():
                    InfoBar.success(
                        title='下载成功！',
                        content="",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=1000,
                        parent=self
                        )
                else:
                    InfoBar.error(
                        title='下载失败！',
                        content="",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self
                        )
            else:
                InfoBar.error(
                title=f'已存在{check}文件夹,无法下载！',
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
                )