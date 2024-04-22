import os
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, InfoBar, TitleLabel, SubtitleLabel,
                            BodyLabel, InfoBarPosition, HyperlinkButton, PrimaryPushButton, MessageBoxBase, FluentIcon)
from app.model.style_sheet import StyleSheet
from app.model.setting_card import SettingCard, SettingCardGroup
from app.model.download_process import SubDownloadCMD
from app.model.config import cfg, open_file, get_json


class HyperlinkCard_Tool(SettingCard):
    def __init__(self, title, content=None, icon=FluentIcon.LINK):
        super().__init__(icon, title, content)
        self.linkButton_fiddler = HyperlinkButton('https://www.telerik.com/fiddler#fiddler-classic', 'Fiddler', self)
        self.linkButton_mitmdump = HyperlinkButton('https://mitmproxy.org/', 'Mitmdump', self)
        self.hBoxLayout.addWidget(self.linkButton_fiddler, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_mitmdump, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


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


class MessageFiddler(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel(self.tr('选择需要使用Fiddler Scripts的服务端:    '))
        self.label1 = SubtitleLabel(self.tr('    目前支持的服务端列表:'))
        self.label2 = BodyLabel('        Yuanshen: Hutao-GS')
        self.label3 = BodyLabel('        StarRail: LunarCore')

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.label1)
        self.viewLayout.addWidget(self.label2)
        self.viewLayout.addWidget(self.label3)

        self.yesButton.setText('Yuanshen')
        self.cancelButton.setText('StarRail')


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
            self.tr('项目仓库'),
            self.tr('打开代理工具仓库')
        )
        self.DownloadFiddlerCard = PrimaryPushSettingCard(
            self.tr('下载'),
            FluentIcon.DOWNLOAD,
            'Fiddler',
            self.tr('下载代理工具Fiddler')
        )
        self.DownloadMitmdumpCard = PrimaryPushSettingCard(
            self.tr('下载'),
            FluentIcon.DOWNLOAD,
            'Mitmdump',
            self.tr('下载代理工具Mitmdump')
        )
        self.ProxyToolInterface = SettingCardGroup(self.scrollWidget)
        self.FiddlerCard = PrimaryPushSettingCard_Fiddler(
            self.tr('Fiddler(外部)'),
            self.tr('使用Fiddler Scripts代理')
        )
        self.mitmdumpCard = PrimaryPushSettingCard(
            self.tr('打开'),
            FluentIcon.VPN,
            self.tr('Mitmdump(外部)'),
            self.tr('使用Mitmdump代理')
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
        self.ProxyDownloadInterface.addSettingCard(self.DownloadMitmdumpCard)
        self.ProxyToolInterface.addSettingCard(self.FiddlerCard)
        self.ProxyToolInterface.addSettingCard(self.mitmdumpCard)
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
        self.DownloadMitmdumpCard.clicked.connect(lambda: SubDownloadCMDSelf.handleDownloadStarted('mitmdump'))
        self.FiddlerCard.clicked_script.connect(lambda: self.handleFiddler('script'))
        self.FiddlerCard.clicked_old.connect(lambda: self.handleFiddler('old'))
        self.mitmdumpCard.clicked.connect(self.handleMitmdump)
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

    def handleFiddler(self, mode):
        if mode == 'script':
            w = MessageFiddler(self)
            if w.exec():
                subprocess.run('del /f "%userprofile%\\Documents\\Fiddler2\\Scripts\\CustomRules.js" && '
                               'copy /y "src\\patch\\fiddler\\CustomRules-GI.js" "%userprofile%\\Documents\\Fiddler2\\Scripts\\CustomRules.js"',
                               shell=True)
                open_file(self, 'tool/Fiddler/Fiddler.exe')
            else:
                subprocess.run('del /f "%userprofile%\\Documents\\Fiddler2\\Scripts\\CustomRules.js" && '
                               'copy /y "src\\patch\\fiddler\\CustomRules-SR.js" "%userprofile%\\Documents\\Fiddler2\\Scripts\\CustomRules.js"',
                               shell=True)
                open_file(self, 'tool/Fiddler/Fiddler.exe')
        elif mode == 'old':
            open_file(self, 'tool/Fiddler/Fiddler.exe')

    def handleMitmdump(self):
        if os.path.exists('tool/Mitmdump'):
            subprocess.run('cd ./tool/Mitmdump && start /b Proxy.exe', shell=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            InfoBar.error(
                title=self.tr("找不到文件，请重新下载！"),
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
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

            InfoBar.success(
                title=self.tr('全局代理已更改！'),
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
        except Exception as e:
            InfoBar.error(
                title=self.tr('全局代理关闭失败！'),
                content=str(e),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
