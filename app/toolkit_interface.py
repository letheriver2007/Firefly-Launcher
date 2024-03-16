import os
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, InfoBar, InfoBarPosition
from app.component.style_sheet import StyleSheet
from app.component.setting_group import SettingCardGroup
from app.component.message_common import MessageFiddler, PrimaryPushSettingCard_Fiddler


class Toolkit(ScrollArea):
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

        # 添加项
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
        self.ProxyToolInterface.addSettingCard(self.FiddlerCard)
        self.ProxyToolInterface.addSettingCard(self.mitmdumpCard)

        # 栏绑定界面
        self.addSubInterface(self.ProxyToolInterface, 'ProxyToolInterface','代理', icon=FIF.CERTIFICATE)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.ProxyToolInterface)
        self.pivot.setCurrentItem(self.ProxyToolInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.ProxyToolInterface.objectName())
        
    def __connectSignalToSlot(self):
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