import os
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, PopupTeachingTip, InfoBarPosition,
                            TitleLabel, SubtitleLabel, BodyLabel, HyperlinkButton, PrimaryPushButton, InfoBar,
                            MessageBoxBase, FluentIcon, FlyoutViewBase, TeachingTipTailPosition, InfoBarIcon, HyperlinkCard)
from app.model.style_sheet import StyleSheet
from app.model.setting_card import SettingCard, SettingCardGroup
from app.model.download_process import SubDownloadCMD
from app.model.config import cfg, get_json, Info


class PrimaryPushSettingCard_Fiddler(SettingCard):
    clicked_script = Signal()
    clicked_old = Signal()

    def __init__(self, title, content=None, icon=FluentIcon.VPN):
        super().__init__(icon, title, content)
        self.button_script = PrimaryPushButton(self.tr('脚本打开'), self)
        self.button_old = PrimaryPushButton(self.tr('原版打开'), self)
        self.hBoxLayout.addWidget(self.button_script, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_old, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_script.clicked.connect(self.clicked_script)
        self.button_old.clicked.connect(self.clicked_old)


class CustomFlyoutView_Fiddler(FlyoutViewBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

        self.gc_button = PrimaryPushButton('Grasscutter')
        self.ht_button = PrimaryPushButton('Hutao-GS')
        self.lc_button = PrimaryPushButton('LunarCore')
        self.gc_button.setFixedWidth(120)
        self.ht_button.setFixedWidth(120)
        self.lc_button.setFixedWidth(120)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(12)
        self.hBoxLayout.setContentsMargins(20, 16, 20, 16)
        self.hBoxLayout.addWidget(self.gc_button)
        self.hBoxLayout.addWidget(self.ht_button)
        self.hBoxLayout.addWidget(self.lc_button)

        self.gc_button.clicked.connect(lambda: self.handleFilddlerButton('gc'))
        self.ht_button.clicked.connect(lambda: self.handleFilddlerButton('ht'))
        self.lc_button.clicked.connect(lambda: self.handleFilddlerButton('lc'))

    def handleFilddlerButton(self, mode):
        status = Proxy.handleFiddlerOpen(self.parent)
        if status:
            if mode =='gc':
                subprocess.run('del /f "%userprofile%\\Documents\\Fiddler2\\Scripts\\CustomRules.js" && '
                                'copy /y "src\\patch\\fiddler\\CustomRules-GC.js" "%userprofile%\\Documents\\Fiddler2\\Scripts\\CustomRules.js"',
                                shell=True)
            elif mode == 'ht':
                subprocess.run('del /f "%userprofile%\\Documents\\Fiddler2\\Scripts\\CustomRules.js" && '
                                'copy /y "src\\patch\\fiddler\\CustomRules-HT.js" "%userprofile%\\Documents\\Fiddler2\\Scripts\\CustomRules.js"',
                                shell=True)
            elif mode == 'lc':
                subprocess.run('del /f "%userprofile%\\Documents\\Fiddler2\\Scripts\\CustomRules.js" && '
                                'copy /y "src\\patch\\fiddler\\CustomRules-LC.js" "%userprofile%\\Documents\\Fiddler2\\Scripts\\CustomRules.js"',
                                shell=True)


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
        self.ProxyRepoCard = HyperlinkCard(
            'https://www.telerik.com/fiddler#fiddler-classic',
            'Fiddler',
            FluentIcon.LINK,
            self.tr('项目仓库'),
            self.tr('打开代理工具仓库')
        )
        self.DownloadFiddlerCard = PrimaryPushSettingCard(
            self.tr('下载'),
            FluentIcon.DOWNLOAD,
            'Fiddler',
            self.tr('下载代理工具Fiddler')
        )
        self.ProxyToolInterface = SettingCardGroup(self.scrollWidget)
        self.FiddlerCard = PrimaryPushSettingCard_Fiddler(
            self.tr('Fiddler'),
            self.tr('使用Fiddler Scripts代理')
        )
        self.noproxyCard = PrimaryPushSettingCard(
            self.tr('重置'),
            FluentIcon.POWER_BUTTON,
            self.tr('重置代理'),
            self.tr('重置部分服务端未关闭的代理')
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
        self.ProxyDownloadInterface.addSettingCard(self.ProxyRepoCard)
        self.ProxyDownloadInterface.addSettingCard(self.DownloadFiddlerCard)
        self.ProxyToolInterface.addSettingCard(self.FiddlerCard)
        self.ProxyToolInterface.addSettingCard(self.noproxyCard)

        # 栏绑定界面
        self.addSubInterface(self.ProxyToolInterface, 'ProxyToolInterface', self.tr('启动'), icon=FluentIcon.PLAY)
        self.addSubInterface(self.ProxyDownloadInterface, 'ToolkitDownloadInterface', self.tr('下载'),
                             icon=FluentIcon.DOWNLOAD)

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
        SubDownloadCMDSelf = SubDownloadCMD(self)
        self.DownloadFiddlerCard.clicked.connect(lambda: SubDownloadCMDSelf.handleDownloadStarted('fiddler'))
        self.FiddlerCard.clicked_script.connect(self.handleFiddlerTip)
        self.FiddlerCard.clicked_old.connect(self.handleFiddlerOpen)
        self.noproxyCard.clicked.connect(self.handleProxyDisabled)

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

    def handleFiddlerOpen(self):
        if os.path.exists('tool/Fiddler/Fiddler.exe'):
            subprocess.run(['start', 'tool/Fiddler/Fiddler.exe'], shell=True)
            Info(self, "S", 1000, self.tr("文件已打开!"))
            return True
        else:
            file_error = InfoBar(
                icon=InfoBarIcon.ERROR,
                title=self.tr('找不到文件!'),
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
            return False

    def handleFiddlerTip(self):
        PopupTeachingTip.make(
            target=self.FiddlerCard.button_script,
            view=CustomFlyoutView_Fiddler(parent=self),
            tailPosition=TeachingTipTailPosition.RIGHT,
            duration=-1,
            parent=self
        )

    def handleProxyDisabled(self):
        try:
            if cfg.proxyStatus.value:
                port = get_json('./config/config.json', 'PROXY_PORT')
                subprocess.run(
                    'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f',
                    shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(
                    f'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "127.0.0.1:{port}" /f',
                    shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.run(
                    'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f',
                    shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(
                    'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "" /f',
                    shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            Info(self, 'S', 1000, self.tr("全局代理已更改！"))
        except Exception as e:
            Info(self, 'E', 3000, self.tr("全局代理关闭失败！"), str(e))
